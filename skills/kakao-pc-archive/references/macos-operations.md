# macOS Operations

## Required Local Pieces

- KakaoTalk for Mac installed and logged in.
- `kakaocli` installed.
- SQLCipher support available through `kakaocli`.
- `~/.kakaocli/config.json` with:
  - `databasePath`
  - `key`
- Full Disk Access for the process reading KakaoTalk container data.
- Accessibility permission only when using UI actions such as `kmsg send/read`.

## Known KakaoTalk Data Areas

```text
~/Library/Containers/com.kakao.KakaoTalkMac/Data/Library/Application Support/com.kakao.KakaoTalkMac
~/Library/Containers/com.kakao.KakaoTalkMac/Data/Library/Caches
```

Do not commit full account-specific paths if they contain hashes or local usernames.

## Safe Query Pattern

Use explicit `--db` and `--key` values from local config. Do not log either value.

```bash
kakaocli query "<SQL>" --db "$databasePath" --key "$key"
```

For agents, prefer a helper that:

- reads local config
- redacts secrets from errors
- times out bounded queries
- parses JSON output
- fails closed if selected chats are empty

## Selected Chat Policy

Do not ingest all rooms by default.

Minimum workflow:

1. Probe chat metadata.
2. Add selected rooms to `selected_chats`.
3. Sync only rows where the chat is enabled.
4. Keep raw archive output outside git.

## Attachment Loop

Recommended cadence for active rooms:

```text
every 1-3 hours
```

Per run:

1. Find new attachment candidates in selected chats.
2. Copy `localFilePath` if readable.
3. Try fresh `attachment.url` once or with a small retry budget.
4. Store downloaded files under ignored `data/media` or another local-only path.
5. Record HTTP status and size.
6. Mark 410 as expired.
7. Avoid logging message bodies and raw URLs.

## Scheduling

Prefer LaunchAgent on macOS because it survives reboot and fits user-session apps better than headless cron.

The LaunchAgent should:

- run as the logged-in user
- set a minimal PATH
- write logs under ignored `logs/`
- never include SQLCipher keys in the plist
- call a wrapper script that reads local config

## kmsg Notes

`kmsg` can send/read KakaoTalk via UI automation, but it is not the archive source of truth.

Known operational caveats:

- Accessibility can differ between SSH direct execution and LaunchAgent execution.
- Room search can fail if the KakaoTalk UI is not in a focusable state.
- Prefer `--chat-id` when `kmsg chats` can see the room.

Use `kmsg` for:

- reminders
- manual bridge tests
- reply automation after confirmation

Avoid `kmsg` for:

- bulk archive collection
- attachment preservation
- claims of reliable DB sync
