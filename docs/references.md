# References

## Primary Project Reference

- `silver-flight-group/kakaocli`
  - <https://github.com/silver-flight-group/kakaocli>
  - Purpose: KakaoTalk CLI for macOS. Reads local SQLCipher DB and uses macOS Accessibility APIs for UI actions.
  - Important limitation: macOS only.

## Crypto / Database Reference

- `sqlcipher/sqlcipher`
  - <https://github.com/sqlcipher/sqlcipher>
  - Purpose: SQLite-compatible encrypted database library.
  - Relevance: `kakaocli` uses SQLCipher to open KakaoTalk's encrypted local DB.

## Key-Derivation Reference

- blluv KakaoTalk Mac DB derivation gist
  - <https://gist.github.com/blluv/8418e3ef4f4aa86004657ea524f2de14>
  - Relevance: The local `kakaocli` source comments cite this as the basis for database name and key derivation.

## Windows Research References

- Kakao DevTalk thread mentioning Windows local KakaoTalk user data path
  - <https://devtalk.kakao.com/t/pc-chat-data/116661>
  - Relevance: Mentions paths such as `%localappdata%\Kakao\KakaoTalk\users\<hash>\`.

- DFRWS paper on encrypted DB files in Windows messengers
  - <https://dfrws.org/sites/default/files/session-files/2019_EU_paper-digital_forensic_analysis_of_encrypted_database_files_in_instant_messaging_applications_on_windows_operating_systems_case_study_with_kakaotalk_nateon_and_qq_messenger.pdf>
  - Relevance: Historical forensic reference for KakaoTalk on Windows. It should not be treated as proof that the current Windows client works the same way.

## Notes

These references are for private research and implementation planning. Respect KakaoTalk terms, local laws, and user consent requirements.

This repository intentionally avoids copying private paths, keys, raw messages, or raw attachment URLs into docs.

## Internal Skill References

- `skills/kakao-pc-archive/SKILL.md`
- `skills/kakao-pc-archive/references/version-support.md`
- `skills/kakao-pc-archive/references/macos-operations.md`
- `skills/kakao-pc-archive/references/github-private-distribution.md`

## Local Implementation Notes

The current verified approach is based on local macOS KakaoTalk DB reads through `kakaocli`:

```bash
kakaocli query "<SQL>" --db "$databasePath" --key "$key"
```

Known KakaoTalk Mac message table shape includes `NTChatRoom` and `NTChatMessage`. Useful message fields include chat/message identifiers, author, message type, message body, `attachment`, `supplement`, `extra`, `sentAt`, and `localFilePath`.

Attachment JSON fields vary by message type. The collector should parse known fields and preserve unknown JSON for later classification.
