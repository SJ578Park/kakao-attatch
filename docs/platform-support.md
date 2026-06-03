# Platform Support

## Summary

The current implementation should be described as macOS-only.

The surrounding archive logic can be designed to be cross-platform, but the verified DB access path depends on `kakaocli`, Swift, SQLCipher, KakaoTalk for Mac's local container paths, and macOS Accessibility APIs.

## macOS

Current path:

- `kakaocli` reads the local SQLCipher-encrypted KakaoTalk Mac database in read-only mode.
- DB path and key are read from local `~/.kakaocli/config.json`.
- UI functions such as send/harvest depend on macOS Accessibility permission.
- Full Disk Access is needed for DB reads.

Known KakaoTalk Mac data area:

```text
~/Library/Containers/com.kakao.KakaoTalkMac/Data/Library/Application Support/com.kakao.KakaoTalkMac
~/Library/Containers/com.kakao.KakaoTalkMac/Data/Library/Caches
```

## Windows

Windows support is not verified in the current implementation.

Known public references indicate that KakaoTalk for Windows stores local user data under paths like:

```text
%LOCALAPPDATA%\Kakao\KakaoTalk\users\<hash>\
```

However, the current Mac implementation does not prove that Windows can use the same:

- database filename derivation
- SQLCipher key derivation
- table names
- attachment metadata shape
- cache naming
- UI automation path

## Recommendation

Split the code into:

- `core`: normalized archive schema, selected chat policy, run logging
- `adapters/macos-kakaocli`: current verified Mac collector
- `adapters/windows-kakao`: future Windows probe
- `media`: attachment downloader/cache watcher experiments
- `rules`: future conditional reply engine

Do not advertise Windows support until a Windows probe can list chats and read selected messages from a local test account.

## Version Reporting Rule

Every shared runbook or handoff should include:

- checked date
- host OS version
- KakaoTalk app version
- collector adapter name
- last DB read test result
- last attachment probe result

Do not infer support from an old successful run after KakaoTalk updates. Re-run the checks in `skills/kakao-pc-archive/references/version-support.md`.
