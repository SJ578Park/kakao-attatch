# 첨부파일 수집 방법

## 현재 확인 내용

KakaoTalk 메시지 row에는 첨부파일 메타데이터가 들어 있습니다. 선택한 채팅방에 대해 collector는 아래 정보를 보존할 수 있습니다.

- 메시지 식별자
- `attachment` JSON
- 파일명 또는 key hint
- MIME type
- 크기
- 이미지/영상 width, height
- 만료값으로 보이는 timestamp
- `localFilePath`가 있을 때의 로컬 파일 경로

다만 `localFilePath`는 관측상 매우 드물고, 주로 로컬에서 보낸 파일이나 이미 로컬에 존재하는 파일에만 의미가 있습니다. 첨부파일 보존의 핵심은 **새 첨부 URL이 만료되기 전에 주기적으로 확인하고 저장을 시도하는 것**입니다.

## 확인된 기준 환경

```text
확인일: 2026-06-03
호스트 OS: macOS 13.7.8
KakaoTalk for Mac: 26.1.4 build 1163 on Intel Mac; 26.4.1 build 1181 on Apple Silicon Mac is a target validation environment
이전 첨부 probe: 2026-05-21
결과: 새 이미지/스프레드시트 URL은 HTTP 200, 오래된 URL은 HTTP 410 사례 확인
```

HTTP 410은 “이미 만료됨”으로 취급합니다. fatal error가 아니라 정상적인 만료 결과로 기록합니다.

## n시간 주기 설정

config에는 아래처럼 표현합니다.

```json
{
  "attachmentCollection": {
    "enabled": true,
    "intervalHours": 3,
    "maxItemsPerRun": 200
  }
}
```

권장값:

- 중요한/활성 채팅방: `1`
- 일반 채팅방: `3`
- 낮은 우선순위 채팅방: `6` 또는 `12`
- 일 1회(`24`)는 오래된 첨부파일을 놓칠 가능성이 큽니다.

## 수집 순서

1. 선택 채팅방의 새 메시지를 DB에서 조회합니다.
2. `NTChatMessage.attachment`를 JSON으로 파싱합니다.
3. `localFilePath`가 있고 읽을 수 있으면 먼저 복사합니다.
4. fresh `attachment.url` 또는 이미지 목록 URL을 즉시 다운로드 시도합니다.
5. 성공 시 ignored media directory에 저장합니다.
6. 실패 시 HTTP status만 기록합니다.
7. raw URL과 원문 메시지는 로그에 남기지 않습니다.

## 첨부 type별 주요 필드

사진(type `2`)에서 자주 보이는 필드:

```text
url, thumbnailUrl, k, mt, s, w, h, expire
```

영상(type `3`)에서 자주 보이는 필드:

```text
url, tk, s, d, w, h, expire
```

파일(type `18`)에서 자주 보이는 필드:

```text
name, url, k, s, size, expire, cs
```

멀티 이미지(type `27`)에서 자주 보이는 필드:

```text
imageUrls, thumbnailUrls, kl, mtl, sl, expire
```

카카오톡 버전에 따라 필드가 바뀔 수 있으므로, collector는 모르는 필드를 버리지 말고 redacted raw JSON으로 로컬 archive에 보존하는 것이 좋습니다.

## 스케줄링

macOS에서는 LaunchAgent를 권장합니다.

`intervalHours = 3`이면 LaunchAgent `StartInterval`은 아래처럼 10800초입니다.

```xml
<key>StartInterval</key>
<integer>10800</integer>
```

간단한 실험에서는 cron도 가능합니다.

```cron
0 */3 * * * cd /path/to/repo && /usr/bin/python3 scripts/sync_once.py --config config/archive.config.json
```

## run log에 남길 내용

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

남기면 안 되는 내용:

- raw attachment URL
- 원문 메시지
- SQLCipher key
- 계정 hash가 들어간 전체 DB path
- 다운로드된 실제 파일

## English Summary

Attachment metadata is read from `NTChatMessage.attachment`. Fresh URLs may be downloadable for a short window, while older URLs can return HTTP 410. Run the attachment collector every 1-3 hours for active rooms.

The primary verified baseline is Intel Mac x86_64 with KakaoTalk for Mac 26.1.4 build 1163 as of 2026-06-03. Apple Silicon arm64 with KakaoTalk for Mac 26.4.1 build 1181 should be confirmed by running the safe probe on that machine. Attachment behavior was probed locally on 2026-05-21: fresh image/spreadsheet URLs returned HTTP 200, while older URLs returned HTTP 410.

Do not log raw URLs, message bodies, SQLCipher keys, or account-specific paths.
