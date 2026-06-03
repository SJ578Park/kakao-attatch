---
name: kakao-pc-archive
description: "Collect selected KakaoTalk PC messages and attachments from local KakaoTalk data."
---

# Kakao PC Archive

Use when operating, extending, or documenting local KakaoTalk PC archive collection.

## Boundaries

- Verified path: macOS KakaoTalk + `kakaocli` direct DB reads.
- Current text collection should use read-only DB access, not UI automation.
- Attachment preservation is freshness-sensitive. Try fresh DB `attachment.url` values quickly, then record status.
- `kmsg` is for UI send/read automation and reminders, not the primary archive collector.
- Windows support is research-only until a Windows probe verifies DB path, key derivation, schema, and attachment shape.

## Before Running

1. Load support status from `references/version-support.md`.
2. Confirm the target chat is explicitly allowlisted.
3. Confirm local config exists outside git.
4. Confirm output paths are ignored by git.
5. Never print SQLCipher keys, raw URLs, raw message bodies, local account hashes, or media paths in shared logs.

## macOS Collection Workflow

1. Read `~/.kakaocli/config.json` locally for `databasePath` and `key`.
2. Query KakaoTalk DB through `kakaocli query "<SQL>" --db "$databasePath" --key "$key"`.
3. Sync chat metadata lightly.
4. Ingest messages only from enabled selected chats.
5. Parse attachment JSON best-effort.
6. Copy local files when `localFilePath` is present.
7. Attempt fresh remote URL download quickly, recording HTTP status without logging the URL.
8. Write run logs with counts and status breakdowns only.

## Scheduling

- macOS recurring jobs: prefer LaunchAgent.
- Simple experiments: cron is acceptable.
- Recommended attachment interval: 1-3 hours for active rooms.
- Daily-only collection can miss attachments because older URLs may expire.

## Reply Automation

Keep reply automation draft-only unless the user explicitly approves sending. Real sends require human confirmation until a rule has been tested and scoped.

## References

- `references/version-support.md`: supported KakaoTalk/client assumptions and version reporting.
- `references/macos-operations.md`: setup, permissions, commands, schedules, and troubleshooting.
- `references/github-private-distribution.md`: private GitHub repo and collaborator distribution.
