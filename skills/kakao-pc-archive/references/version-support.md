# Version Support

## Current Verified Shape

Report this workflow as:

```text
Support level: macOS verified, Windows unverified
KakaoTalk client: KakaoTalk for Mac
Collection adapter: kakaocli direct SQLCipher DB read
Attachment adapter: DB attachment JSON + fresh URL downloader + optional cache watcher
UI automation: kmsg for send/read only, not archive source of truth
Last local behavior probe: 2026-05-21
```

## Version Caveat

KakaoTalk can change local database paths, SQLCipher key derivation, table names, field names, attachment JSON shape, URL expiry behavior, and UI accessibility behavior between client versions.

Agents must record the local version before claiming support:

```bash
mdls -name kMDItemVersion /Applications/KakaoTalk.app
defaults read /Applications/KakaoTalk.app/Contents/Info CFBundleShortVersionString
```

If neither command works, record:

```text
KakaoTalk version: not verified on this host
```

## Compatibility Matrix

- macOS + KakaoTalk for Mac + `kakaocli`: verified approach in current workspace.
- macOS + `kmsg`: useful for UI send/read/reminder automation; fragile around search focus and recent chat state.
- Windows + KakaoTalk PC: not verified. Treat as separate probe.
- Mobile KakaoTalk: out of scope.

## Revalidation Checklist

Run this after KakaoTalk updates:

1. Confirm Full Disk Access still allows DB reads.
2. Confirm `~/.kakaocli/config.json` still points to an existing DB.
3. Run a read-only selected-chat query.
4. Confirm required fields exist: chat id, message/log id, author, message type, body, attachment JSON, sent timestamp.
5. Send or receive a test attachment in an allowlisted room.
6. Confirm attachment JSON fields and immediate download behavior.
7. Record HTTP status counts, not raw URLs.
8. Update this file if behavior changes.

## Known Attachment Behavior

Observed local behavior:

- Fresh unread/new image and spreadsheet attachments can return HTTP 200 from DB `attachment.url`.
- Older URLs can return HTTP 410 even when metadata remains in the DB.
- `localFilePath` is often empty for fresh attachments.

Operational conclusion: run frequent fresh capture. Do not promise recovery of old attachments.
