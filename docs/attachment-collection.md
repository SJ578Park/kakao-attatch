# Attachment Collection

## Current Finding

KakaoTalk message rows include attachment metadata. For selected chats, the collector can preserve:

- message row identity
- attachment JSON
- filename or key hints
- MIME type
- size
- width/height
- expiry-like timestamps
- `localFilePath` when present

Prior local probes showed that `localFilePath` is rare and mostly useful for files that already exist locally.

Fresh attachment URLs can be usable for a short window. In a 2026-05-21 local probe, newly received image and spreadsheet attachments returned HTTP 200 directly from DB `attachment.url`. Older sampled URLs returned HTTP 410. The practical rule is:

- collect fresh attachments quickly
- record exact HTTP status
- treat HTTP 410 as normal expiry, not a fatal sync error
- never depend only on remote URLs for long-term preservation

## n-Hour Schedule

The config should expose:

```json
{
  "attachmentCollection": {
    "enabled": true,
    "intervalHours": 3,
    "maxItemsPerRun": 200
  }
}
```

`intervalHours` is the n-hour setting. For example:

- `1`: run every hour
- `3`: run every 3 hours
- `6`: run four times per day
- `24`: daily archival pass

## Collection Strategy

Recommended order:

1. `localFilePath`: copy the local file if KakaoTalk already records a readable local path.
2. `remoteUrlFresh`: try DB attachment URLs immediately for new rows, record exact HTTP status, and treat failures as normal.
3. `filesystemWatcher`: watch KakaoTalk cache/download folders and copy newly created files.
4. `uiBackfill`: optional manual/assisted path for selected old media only.

## Scheduling Options

macOS:

- LaunchAgent is the most native recurring option.
- `cron` is acceptable for simple local experiments.

Windows:

- Use Task Scheduler once a Windows adapter exists.

Cross-platform:

- A long-running Node/Python process can poll every `intervalHours`, but OS-native scheduling is easier to recover after reboot.

## Run Log

Each run should record:

```text
started_at
finished_at
selected_chat_count
new_message_count
attachment_candidates
download_success_count
download_failure_count
failure_status_breakdown
```

Do not log raw URLs or message bodies.
