# Kakao PC Archive Notes

Private repository draft for documenting local KakaoTalk PC data collection.

This package is intentionally documentation-first. It records the current Mac implementation, the platform gap for Windows, the intended n-hour attachment/media collection loop, and a reusable OpenClaw skill bundle without including private chat data, SQLCipher keys, raw attachment URLs, or local account identifiers.

## Current Status

- macOS: practical path exists through `kakaocli`, which reads KakaoTalk for Mac's local SQLCipher database and uses macOS Accessibility APIs for UI actions.
- Windows: not implemented or verified in the current code. Treat as a separate research/implementation track.
- Attachments: DB metadata can be collected. Fresh attachment URLs may be downloadable for a short window, but older URLs can return HTTP 410. Run the attachment collector frequently and treat URL download as best-effort.
- Scope: selected chats only. Do not ingest all rooms by default.

## Repository Layout

```text
.
├── README.md
├── SECURITY.md
├── config
│   └── archive.config.example.json
├── docs
│   ├── architecture.md
│   ├── attachment-collection.md
│   ├── conditional-reply.md
│   ├── platform-support.md
│   └── references.md
├── skills
│   └── kakao-pc-archive
│       ├── SKILL.md
│       └── references
│           ├── github-private-distribution.md
│           ├── macos-operations.md
│           └── version-support.md
└── scripts
    └── README.md
```

## Minimum Safe Workflow

1. Keep the repository private.
2. Copy `config/archive.config.example.json` to a local ignored config file.
3. Configure selected chat names or IDs only.
4. Set `attachmentCollection.intervalHours` to the desired n-hour interval.
5. Run collection locally and store raw data outside git.
6. Commit only sanitized docs, schemas, and code.

## Agent Skill

Install or copy `skills/kakao-pc-archive` into an agent's skills directory when that agent needs to operate or extend this workflow.

The skill intentionally separates:

- verified macOS DB collection through `kakaocli`
- experimental attachment preservation
- `kmsg` UI automation for send/read operations only
- future Windows research
- private GitHub distribution notes

## Can This Reply Automatically?

Yes, but replying is a second phase.

The current phase should focus on reliable local collection and normalized storage. Once the archive is stable, a rule engine can detect specific conditions and draft replies. Actual external sending should stay confirmation-gated until the rules are well tested.
