# Security Policy

## Never Commit

- `~/.kakaocli/config.json`
- SQLCipher keys
- Kakao user IDs
- full local DB paths with account hashes
- raw message bodies
- raw attachment URLs
- downloaded media
- exported SQLite archives
- logs containing private chat names or content

## Safe to Commit

- redacted setup notes
- schema definitions
- code that reads local config
- config examples with fake values
- support matrix and known limitations
- public GitHub references

## Operational Rules

- Read KakaoTalk data in read-only mode.
- Use an explicit allowlist for chats.
- Keep raw archive files local by default.
- Store media under a local data directory that is ignored by git.
- Log counts and statuses, not message bodies.
- Require human confirmation before sending messages to real chats.

