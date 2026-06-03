# 보안 정책

이 저장소는 public으로 공개될 수 있으므로, 실제 운영 데이터는 절대 포함하지 않는다.

## 절대 커밋하지 않을 것

- `~/.kakaocli/config.json`
- SQLCipher key
- Kakao user ID
- 계정 hash가 포함된 전체 DB path
- 원문 메시지
- raw attachment URL
- 다운로드된 첨부파일
- export된 SQLite archive
- private 채팅방 이름/내용이 들어간 log
- `.env`, token, password

## 커밋 가능한 것

- redacted setup note
- schema definition
- local config를 읽는 코드
- 가짜 값만 들어간 config example
- support matrix와 known limitations
- 공개 GitHub/reference URL
- 공개 가능한 skill 문서

## 운영 규칙

- KakaoTalk 데이터는 read-only로 읽는다.
- 채팅방은 allowlist 기반으로만 수집한다.
- raw archive file은 로컬에만 둔다.
- media는 git ignore된 local data directory에 저장한다.
- log에는 count와 status만 남긴다.
- 실제 카카오톡 메시지 전송은 human confirmation 후에만 한다.

## English Summary

Never commit local KakaoTalk configs, SQLCipher keys, user IDs, account-specific DB paths, raw message bodies, raw attachment URLs, downloaded media, exported archives, or private logs. Public commits should contain only sanitized docs, schemas, examples, and code.
