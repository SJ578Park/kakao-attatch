# AGENTS.md - Kakao PC Archive Skill Package

This private repository documents a reusable OpenClaw/Codex skill for selected KakaoTalk PC archive collection.

## Role

Agents using this repository should treat it as a local-first, privacy-sensitive archive workflow.

Primary tasks:

- Read selected KakaoTalk for Mac messages through local DB access.
- Preserve attachment metadata and fresh downloadable media when possible.
- Record KakaoTalk/client version assumptions before claiming support.
- Keep raw chat data, media, DB files, keys, user IDs, and raw URLs out of git.

## Startup

Before operating the workflow:

1. Read `README.md`.
2. Read `SECURITY.md`.
3. Read `skills/kakao-pc-archive/SKILL.md`.
4. Read `skills/kakao-pc-archive/references/version-support.md`.
5. Confirm the target chats are explicitly allowlisted.

## Hard Boundaries

- Do not ingest all chats by default.
- Do not print SQLCipher keys, raw message bodies, raw attachment URLs, or full account-specific DB paths.
- Do not commit local config, archive DBs, logs, or downloaded media.
- Do not send KakaoTalk replies automatically unless the operator has explicitly approved that exact behavior.
- Treat Windows support as unverified until a Windows adapter probe proves DB path, key derivation, schema, and attachment behavior.

## Verified Support Statement

Use this wording unless newer evidence is recorded:

```text
macOS KakaoTalk collection is the verified path through kakaocli direct SQLCipher DB reads.
Windows KakaoTalk support is planned/research-only.
Attachment preservation is best-effort and freshness-sensitive.
```

## Release Checklist

Before pushing or sharing:

1. Run `git status --short`.
2. Run the secret scan pattern in `skills/kakao-pc-archive/references/github-private-distribution.md`.
3. Confirm the repo is private.
4. Invite collaborators with the minimum necessary permission.
