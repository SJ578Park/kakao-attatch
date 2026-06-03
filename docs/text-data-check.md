# 텍스트 데이터 확인 방법

이 문서는 KakaoTalk for Mac 로컬 DB에서 선택한 채팅방의 텍스트 데이터를 확인하는 절차입니다.

## 확인된 기준 환경

```text
확인일: 2026-06-03
검증 호스트:
  - Intel Mac: x86_64, Intel Core i5, macOS 13.7.8, KakaoTalk for Mac 26.1.4 build 1163
  - Apple Silicon Mac: arm64, Apple M4, macOS 26.4.1, KakaoTalk for Mac 26.4.1 build 1181
수집 도구: kakaocli 0.4.1
Intel Mac DB 접근: local SQLCipher DB read-only query
Apple Silicon DB 접근: auth --user-id 기반 DB open, NTChatRoom / NTChatMessage query 통과
```

기본 검증 기준은 Intel Mac입니다. Apple Silicon 26.4.1 build 1181에서도 `kakaocli auth --user-id` 후 `NTChatRoom` / `NTChatMessage` query가 통과했습니다. 자동 userId 탐색이 실패할 수 있으므로 필요하면 local userId를 명시해 auth를 먼저 실행합니다.

## 사전 조건

- KakaoTalk for Mac이 설치되어 있고 로그인되어 있어야 합니다.
- `kakaocli`가 설치되어 있어야 합니다.
- `~/.kakaocli/config.json`에 `databasePath`, `key`, `userId` 중 필요한 값이 있어야 합니다.
- DB를 읽는 프로세스에 Full Disk Access가 필요할 수 있습니다.
- 공유 로그에 DB 경로, 키, 원문 메시지, raw 첨부 URL을 출력하지 않아야 합니다.

## 1. 카카오톡 버전 확인

```bash
mdls -name kMDItemVersion /Applications/KakaoTalk.app
defaults read /Applications/KakaoTalk.app/Contents/Info CFBundleShortVersionString
```

기록 예시:

```text
KakaoTalk for Mac: 26.1.4 build 1163
Apple Silicon partial probe: 26.4.1 build 1181
```

버전이 다르면 이 문서의 결과를 그대로 가정하지 말고 아래 query를 다시 검증합니다.

## 2. 로컬 설정 확인

`~/.kakaocli/config.json`에 다음 값이 있는지만 확인합니다.

```text
databasePath: present
key: present
userId: present or manually supplied
```

실제 값을 문서나 로그에 남기지 않습니다.

자동 userId 탐색이 실패하면 아래처럼 로컬 userId를 명시해 DB open만 먼저 확인합니다.

```bash
kakaocli auth --user-id "<local_user_id>"
```

이 명령이 통과해도 메시지 query가 통과한 것은 아닙니다.

## 3. 채팅방 목록 확인

채팅방 목록을 먼저 조회하고, 필요한 방만 allowlist에 추가합니다.

예시 SQL:

```sql
select id, name, lastLogId
from NTChatRoom
order by lastUpdatedAt desc
limit 20;
```

실행 형태:

```bash
kakaocli query "<SQL>" --db "$databasePath" --key "$key"
```

이 단계가 실패하면 해당 환경은 `db_open: pass`, `selected_chat_query: fail`로 기록합니다. query가 통과하면 `selected_chat_query: pass`로 승격합니다.

## 4. 선택 채팅방 메시지 확인

선택한 채팅방에 대해 최근 메시지 몇 건만 확인합니다.

예시 SQL:

```sql
select chatId, logId, msgId, authorId, type, message, attachment, sentAt, localFilePath
from NTChatMessage
where chatId = <selected_chat_id>
order by sentAt desc
limit 20;
```

확인할 항목:

- `chatId`, `logId`, `msgId`가 메시지 식별자로 사용 가능한지
- `message`에 텍스트가 들어오는지
- `type`별로 텍스트/이미지/파일 메시지가 구분되는지
- `attachment`가 JSON 문자열 형태인지
- `sentAt` timestamp가 예상 범위인지
- `localFilePath`가 비어 있는 경우가 많은지

## 5. 공유 가능한 결과만 기록

공유 문서에는 아래처럼 요약만 남깁니다.

```text
checked_at: 2026-06-03
host: Intel Mac x86_64 or Apple Silicon Mac arm64
kakaotalk_version: 26.1.4 build 1163
db_open: pass
selected_chat_query: pass
message_columns: chatId/logId/msgId/authorId/type/message/attachment/sentAt/localFilePath
raw_message_logged: no
raw_url_logged: no
```

Apple Silicon partial probe 예시:

```text
checked_at: 2026-06-03
host: Apple Silicon Mac arm64, Apple M4
kakaotalk_version: 26.4.1 build 1181
db_open: pass
selected_chat_query: pass
attachment_json_parse: pass
attachment_url_download: pass on sampled URLs
```

## English Summary

Use `kakaocli 0.4.1` to read the KakaoTalk for Mac local SQLCipher database in read-only mode. The primary verified baseline is Intel Mac x86_64 with KakaoTalk for Mac 26.1.4 build 1163. Apple Silicon arm64 / Apple M4 with KakaoTalk for Mac 26.4.1 build 1181 was rechecked through `kakaocli auth --user-id`, database open, and `NTChatRoom` / `NTChatMessage` queries as of 2026-06-03.

Before claiming support on another version, verify the KakaoTalk app version, local `kakaocli` config presence, `NTChatRoom` query, and selected `NTChatMessage` query. Do not log DB paths, keys, raw message bodies, or raw attachment URLs.
