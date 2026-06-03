# Attachment Collection

## 현재 확인된 내용

KakaoTalk message row에는 attachment metadata가 포함될 수 있습니다. selected chat에 대해서는 collector가 다음을 보존할 수 있습니다.

- message row identity
- attachment JSON
- filename or key hints
- MIME type
- size
- width/height
- expiry-like timestamps
- `localFilePath` when present

기존 local probe 기준으로 `localFilePath`는 자주 비어 있었고, 이미 로컬에 존재하는 파일에만 유용한 경우가 많았습니다.

fresh attachment URL은 짧은 기간 동안 사용할 수 있습니다. 2026-05-21 local probe에서 신규 이미지와 spreadsheet 첨부는 DB `attachment.url`로 HTTP 200 다운로드가 가능했습니다. 오래된 sample URL은 HTTP 410을 반환했습니다.

실무 규칙:

- fresh 첨부는 빠르게 수집합니다.
- HTTP status를 기록합니다.
- HTTP 410은 fatal error가 아니라 정상 만료로 취급합니다.
- 장기 보존을 remote URL에만 의존하지 않습니다.
- raw URL은 로그나 GitHub에 남기지 않습니다.

## n시간 주기

설정은 다음 값을 노출합니다.

```json
{
  "attachmentCollection": {
    "enabled": true,
    "intervalHours": 3,
    "maxItemsPerRun": 200
  }
}
```

`intervalHours`가 n시간 주기입니다.

- `1`: 매시간 실행
- `3`: 3시간마다 실행
- `6`: 하루 4회 실행
- `24`: 일 1회 archival pass

active room은 `1` 또는 `3`을 권장합니다. 일 1회 수집은 첨부파일 만료를 놓칠 수 있습니다.

## 수집 전략

권장 순서:

1. `localFilePath`: KakaoTalk이 readable local path를 기록했다면 파일을 복사합니다.
2. `remoteUrlFresh`: 신규 row의 DB attachment URL을 즉시 시도하고 HTTP status를 기록합니다.
3. `filesystemWatcher`: KakaoTalk cache/download folder의 신규 파일을 감시해 복사합니다.
4. `uiBackfill`: 오래된 selected media에 한해 manual/assisted path로 보완합니다.

## 스케줄링

macOS:

- LaunchAgent가 user session app과 가장 잘 맞습니다.
- 간단한 실험은 `cron`도 가능합니다.

Windows:

- Windows adapter가 검증된 뒤 Task Scheduler를 고려합니다.

Cross-platform:

- long-running Node/Python process가 `intervalHours`마다 poll할 수 있지만, reboot 복구는 OS-native scheduling이 더 쉽습니다.

## 공유 가능한 run log

각 run은 다음 정도만 기록합니다.

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

raw URL이나 message body는 로그에 남기지 않습니다.

---

# English Summary

Attachment URLs are freshness-sensitive. In local testing on 2026-05-21, fresh image and spreadsheet attachment URLs returned HTTP 200, while older sampled URLs returned HTTP 410. Run attachment collection every 1-3 hours for active rooms, record HTTP status, and treat 410 as normal expiry.
