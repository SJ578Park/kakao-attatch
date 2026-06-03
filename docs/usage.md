# 사용법

이 문서는 공개 저장소에 넣을 수 있는 수준의 운영 절차만 담습니다. 실제 메시지, 채팅방 이름, user id, attachment URL, SQLCipher key는 기록하지 않습니다.

## 1. 동작 환경 확인

먼저 KakaoTalk for Mac 버전을 확인합니다.

```bash
defaults read /Applications/KakaoTalk.app/Contents/Info CFBundleShortVersionString
defaults read /Applications/KakaoTalk.app/Contents/Info CFBundleVersion
mdls -name kMDItemVersion /Applications/KakaoTalk.app
```

현재 이 workflow가 확인된 버전은 다음입니다.

- KakaoTalk for Mac `26.1.4` build `1163`
- KakaoTalk for Mac `26.4.1` build `1181`
- `kakaocli 0.4.1`
- `kmsg 0.3.0`

다른 버전에서는 먼저 read-only query와 첨부파일 fresh download를 재검증해야 합니다.

## 2. 로컬 설정 확인

`kakaocli`는 로컬 설정에서 DB 경로와 key를 읽습니다.

```bash
test -f ~/.kakaocli/config.json && echo "config exists"
```

`~/.kakaocli/config.json`에는 보통 다음 값이 있습니다.

```json
{
  "databasePath": "...",
  "key": "..."
}
```

이 파일은 절대 commit하지 않습니다.

## 3. 텍스트 데이터 확인

가장 안전한 기본 원칙은 read-only query입니다.

```bash
kakaocli query "<SQL>" --db "$databasePath" --key "$key"
```

에이전트나 스크립트에서는 local config를 읽고 key를 로그에 남기지 않습니다.

```bash
python3 - <<'PY'
import json
import pathlib
import subprocess

cfg_path = pathlib.Path.home() / ".kakaocli/config.json"
cfg = json.loads(cfg_path.read_text())

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
result = subprocess.run(cmd, text=True, capture_output=True, timeout=30)
if result.returncode != 0:
    raise SystemExit(result.stderr or result.stdout)
print(result.stdout)
PY
```

주의:

- 이 출력에는 실제 메시지 본문이 포함될 수 있습니다.
- 공유용 로그에는 row count, HTTP status, 성공/실패 수만 남깁니다.
- raw message output은 저장소에 commit하지 않습니다.

## 4. selected chat만 수집

모든 채팅방을 기본 수집하지 않습니다.

권장 순서:

1. 채팅방 목록이나 metadata를 로컬에서만 확인합니다.
2. 수집할 방만 `selected_chats` 또는 local config allowlist에 넣습니다.
3. 이후 message sync는 enabled selected chat만 대상으로 실행합니다.

## 5. 첨부파일 확인과 만료

카카오톡 DB에는 첨부파일 metadata와 URL이 남아 있을 수 있습니다. 하지만 파일 URL은 오래 지나면 만료될 수 있습니다.

현재 관측된 동작:

- 신규/미읽음 상태의 이미지와 엑셀 파일은 DB `attachment.url`에서 HTTP 200으로 다운로드 가능했습니다.
- 오래된 이미지/파일 URL은 HTTP 410으로 만료될 수 있었습니다.
- `localFilePath`는 비어 있는 경우가 많았습니다.

운영 규칙:

- active room은 1-3시간 주기로 첨부파일 후보를 확인합니다.
- fresh URL은 가능한 빨리 다운로드를 시도합니다.
- HTTP 410은 정상적인 만료 상태로 기록합니다.
- 오래된 첨부파일 복구를 보장하지 않습니다.
- raw URL은 로그에 남기지 않습니다.

## 6. 권장 run log

공유 가능한 run log는 다음 정도로 제한합니다.

```text
started_at
finished_at
selected_chat_count
new_message_count
attachment_candidates
download_success_count
download_failure_count
failure_status_breakdown
```

## 7. `kmsg` 사용 범위

`kmsg`는 UI 자동화 도구입니다.

사용해도 되는 경우:

- 메시지 발송 테스트
- reminder 전송
- confirmation 이후 답장 자동화

주 수집 경로로 쓰지 않는 이유:

- 검색창 focus 상태에 민감합니다.
- macOS Accessibility 권한과 실행 방식에 영향을 받습니다.
- 첨부파일 보존에는 DB/URL/cache watcher가 더 적합합니다.

---

# English Summary

Use read-only `kakaocli query` for text inspection. Do not commit local config, SQLCipher keys, raw message output, attachment URLs, downloaded media, or archive DB files.

Verified versions:

- KakaoTalk for Mac `26.1.4` build `1163`
- KakaoTalk for Mac `26.4.1` build `1181`
- `kakaocli 0.4.1`
- `kmsg 0.3.0`

Attachments are freshness-sensitive. New attachment URLs may return HTTP 200 for a short time, while older URLs may return HTTP 410. Run attachment collection every 1-3 hours for active chats and record only counts/statuses in shared logs.
