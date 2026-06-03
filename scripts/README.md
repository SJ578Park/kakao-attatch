# Scripts

No executable scripts are included in this sanitized draft yet.

Recommended future scripts:

```text
sync-once.js              # Run one selected-chat message sync.
collect-attachments.js    # Process pending attachment candidates.
watch-media-cache.js      # Copy new files from watched KakaoTalk cache folders.
make-launchagent.js       # Generate a macOS LaunchAgent using intervalHours.
make-task-scheduler.ps1   # Generate a Windows Task Scheduler task after Windows support exists.
```

Before adding scripts, make sure they read secrets from local config and never print SQLCipher keys, raw URLs, or message bodies.

