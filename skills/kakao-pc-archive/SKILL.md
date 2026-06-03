---
name: kakao-pc-archive
description: "Collect selected KakaoTalk PC messages and attachments from local KakaoTalk data."
---

# Kakao PC Archive

KakaoTalk PC archive collection을 운영, 확장, 문서화할 때 사용합니다. 한글 설명을 우선하고 필요한 경우 뒤에 영어 요약을 덧붙입니다.

## 경계

- 검증 경로: macOS KakaoTalk + `kakaocli 0.4.1` direct DB read.
- 확인된 KakaoTalk for Mac: `26.1.4` build `1163`, `26.4.1` build `1181`.
- 텍스트 수집은 UI 자동화가 아니라 read-only DB 접근을 우선합니다.
- 첨부파일은 freshness-sensitive입니다. DB `attachment.url`은 만료 전에 빠르게 확인하고 HTTP status를 기록합니다.
- `kmsg 0.3.0`은 send/read UI 자동화와 reminder용입니다. archive source of truth가 아닙니다.
- Windows는 DB path, key derivation, schema, attachment shape probe 전까지 research-only입니다.

## 실행 전 확인

1. Load support status from `references/version-support.md`.
2. Confirm the target chat is explicitly allowlisted.
3. Confirm local config exists outside git.
4. Confirm output paths are ignored by git.
5. Never print SQLCipher keys, raw URLs, raw message bodies, local account hashes, or media paths in shared logs.

## macOS collection workflow

1. Read `~/.kakaocli/config.json` locally for `databasePath` and `key`.
2. Query KakaoTalk DB through `kakaocli query "<SQL>" --db "$databasePath" --key "$key"`.
3. Sync chat metadata lightly.
4. Ingest messages only from enabled selected chats.
5. Parse attachment JSON best-effort.
6. Copy local files when `localFilePath` is present.
7. Attempt fresh remote URL download quickly, recording HTTP status without logging the URL.
8. Write run logs with counts and status breakdowns only.

## 스케줄링

- macOS recurring jobs: prefer LaunchAgent.
- Simple experiments: cron is acceptable.
- Recommended attachment interval: 1-3 hours for active rooms.
- Daily-only collection can miss attachments because older URLs may expire.

## Reply automation

Keep reply automation draft-only unless the user explicitly approves sending. Real sends require human confirmation until a rule has been tested and scoped.

## References

- `references/version-support.md`: supported KakaoTalk/client assumptions and version reporting.
- `references/macos-operations.md`: setup, permissions, commands, schedules, and troubleshooting.
- `references/github-distribution.md`: public/private GitHub repo and collaborator distribution.

English summary: Use this skill for macOS-only KakaoTalk PC local archive work. Verified versions are KakaoTalk for Mac 26.1.4/26.4.1 with kakaocli 0.4.1. Revalidate after KakaoTalk updates.
