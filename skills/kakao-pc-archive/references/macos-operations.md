# macOS Operations

## 필요한 로컬 구성

- KakaoTalk for Mac 설치 및 로그인.
- 검증된 KakaoTalk for Mac 버전:
  - Intel Mac x86_64: `26.1.4` build `1163` full text/attachment baseline
  - Apple Silicon arm64 + Apple M4: `26.4.1` build `1181` partial DB-open probe only
- `kakaocli 0.4.1` 설치.
- `kmsg 0.3.0` 설치. 단, archive source가 아니라 UI send/read 용도.
- `~/.kakaocli/config.json`:
  - `databasePath`
  - `key`
  - `userId` 또는 로컬에서 수동 확인 가능한 user id
- KakaoTalk container data를 읽는 process에 Full Disk Access 필요 가능.
- `kmsg send/read` 같은 UI action에는 Accessibility permission 필요.

## KakaoTalk data area

```text
~/Library/Containers/com.kakao.KakaoTalkMac/Data/Library/Application Support/com.kakao.KakaoTalkMac
~/Library/Containers/com.kakao.KakaoTalkMac/Data/Library/Caches
```

계정 hash나 local username이 포함된 전체 경로는 commit하지 않습니다.

## 안전한 auth/query pattern

먼저 DB open을 확인합니다. 자동 userId 탐색이 실패하면 로컬 userId를 명시합니다.

```bash
kakaocli auth --user-id "$localUserId"
```

이 단계는 DB 파일과 주요 테이블을 열 수 있는지만 확인합니다. 실제 메시지 아카이브 지원을 주장하려면 read-only query까지 통과해야 합니다.

local config에서 `--db`, `--key` 값을 읽어 명시적으로 전달합니다. 두 값은 로그에 남기지 않습니다.

```bash
kakaocli query "<SQL>" --db "$databasePath" --key "$key"
```

에이전트는 다음 성격의 helper를 선호합니다.

- local config를 읽습니다.
- error에서 secret을 redaction합니다.
- bounded query에 timeout을 겁니다.
- JSON output을 parsing합니다.
- selected chat이 비어 있으면 fail closed합니다.
- `auth`만 통과하고 `query`가 실패하면 partial support로 기록합니다.

## 텍스트 데이터 확인

직접 확인용 read-only query 예시:

```bash
python3 - <<'PY'
import json
import pathlib
import subprocess

cfg = json.loads((pathlib.Path.home() / ".kakaocli/config.json").read_text())
sql = """
select chatId, logId, authorId, type, message, attachment, sentAt
from NTChatMessage
order by sentAt desc
limit 20
"""
binary = pathlib.Path.home() / ".local/bin/kakaocli"
if not binary.exists():
    binary = "kakaocli"
cmd = [str(binary), "query", sql, "--db", cfg["databasePath"], "--key", cfg["key"]]
p = subprocess.run(cmd, text=True, capture_output=True, timeout=30)
if p.returncode != 0:
    raise SystemExit(p.stderr or p.stdout)
print(p.stdout)
PY
```

이 출력은 실제 메시지를 포함할 수 있으므로 공유하지 않습니다.

## selected chat policy

모든 방을 기본 수집하지 않습니다.

최소 workflow:

1. chat metadata를 로컬에서만 probe합니다.
2. selected room만 `selected_chats`에 넣습니다.
3. enabled selected chat row만 sync합니다.
4. raw archive output은 git 밖에 둡니다.

## 첨부파일 loop

active room 권장 주기:

```text
1-3시간마다
```

각 run:

1. selected chat의 신규 attachment candidate를 찾습니다.
2. `localFilePath`가 readable이면 복사합니다.
3. fresh `attachment.url`을 즉시 시도합니다.
4. 다운로드 파일은 ignored `data/media` 또는 local-only path에 저장합니다.
5. HTTP status와 size만 기록합니다.
6. 410은 expired로 표시합니다.
7. message body와 raw URL은 로그에 남기지 않습니다.

## Scheduling

macOS에서는 LaunchAgent를 선호합니다. user-session app과 잘 맞고 reboot 이후 복구가 쉽습니다.

LaunchAgent는 다음을 지켜야 합니다.

- logged-in user로 실행.
- 최소 PATH 설정.
- ignored `logs/` 아래에 로그 기록.
- plist에 SQLCipher key를 넣지 않음.
- local config를 읽는 wrapper script 호출.

## kmsg Notes

`kmsg`는 UI automation으로 KakaoTalk send/read를 할 수 있지만 archive source of truth가 아닙니다.

운영 caveat:

- Accessibility 상태는 SSH direct execution과 LaunchAgent execution에서 다를 수 있습니다.
- KakaoTalk UI가 focus 가능한 상태가 아니면 room search가 실패할 수 있습니다.
- `kmsg chats`에서 room이 보이면 `--chat-id`를 선호합니다.

`kmsg` 사용처:

- reminders
- manual bridge tests
- reply automation after confirmation

`kmsg`를 피할 곳:

- bulk archive collection
- attachment preservation
- claims of reliable DB sync

---

# English Summary

Use `kakaocli 0.4.1` for read-only local DB inspection. The primary baseline is Intel Mac x86_64 with KakaoTalk for Mac 26.1.4 build 1163. Apple Silicon arm64 / Apple M4 with KakaoTalk for Mac 26.4.1 build 1181 is currently partial: `auth --user-id` can open the DB and list key tables, but message query and fresh attachment URL download were not fully verified. Use `kmsg 0.3.0` only for UI send/read automation. Run attachment checks every 1-3 hours for active rooms because fresh URLs may expire.
