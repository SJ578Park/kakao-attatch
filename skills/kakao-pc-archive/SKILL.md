---
name: kakao-pc-archive
description: "Collect selected KakaoTalk PC messages and attachments from local KakaoTalk data."
---

# Kakao PC Archive

선택한 카카오톡 PC/Mac 채팅방의 텍스트와 첨부파일 메타데이터를 로컬에서 확인하거나 아카이브할 때 사용한다.

## 기본 경계

- 기본 검증 경로: Intel Mac x86_64 + KakaoTalk for Mac 26.1.4 build 1163 + `kakaocli 0.4.1` direct DB read.
- 재현 확인 경로: Apple Silicon arm64 + KakaoTalk for Mac 26.4.1 build 1181 + `kakaocli 0.4.1` direct DB read.
- 텍스트 수집은 UI 자동화가 아니라 read-only DB 조회를 우선한다.
- 첨부파일 보존은 시간 민감하다. 새 `attachment.url`이 만료되기 전에 빠르게 확인하고 HTTP status를 기록한다.
- `kmsg`는 UI send/read/reminder 보조용이다. archive source of truth로 쓰지 않는다.
- Windows는 DB 위치, key derivation, schema, attachment shape를 따로 검증하기 전까지 research-only다.

## 실행 전 확인

1. `references/version-support.md`에서 지원 버전과 재검증 절차를 읽는다.
2. 대상 채팅방이 명시적으로 allowlist에 들어 있는지 확인한다.
3. 로컬 config가 git 밖에 있는지 확인한다.
4. archive DB, logs, media output이 git ignore 대상인지 확인한다.
5. SQLCipher key, raw URL, 원문 메시지, 로컬 계정 hash, media path를 공유 로그에 출력하지 않는다.

## 텍스트 데이터 확인

1. 로컬 `~/.kakaocli/config.json`에서 `databasePath`, `key` 존재 여부만 확인한다.
2. `kakaocli query "<SQL>" --db "$databasePath" --key "$key"` 형태로 read-only query를 실행한다.
3. `NTChatRoom`에서 채팅방 목록을 확인한다.
4. allowlist에 들어간 채팅방만 `NTChatMessage`에서 최근 메시지를 조회한다.
5. `chatId`, `logId`, `msgId`, `authorId`, `type`, `message`, `attachment`, `sentAt`, `localFilePath` 컬럼을 확인한다.
6. 공유 결과에는 pass/fail, 컬럼 존재 여부, count만 남긴다.

## 첨부파일 확인

1. 선택 채팅방의 새 메시지에서 `attachment` JSON을 파싱한다.
2. `localFilePath`가 읽히면 먼저 복사한다.
3. fresh remote URL은 즉시 다운로드 시도한다.
4. HTTP 410은 만료로 기록하고 fatal error로 취급하지 않는다.
5. 활성 채팅방은 1-3시간 간격으로 확인한다.
6. raw URL은 로그에 남기지 않는다.

## 스케줄링

- macOS 반복 실행: LaunchAgent 권장.
- 간단한 실험: cron 가능.
- 활성 채팅방 첨부파일: 1-3시간 권장.
- 일 1회 수집은 만료된 첨부파일을 놓칠 수 있다.

## 자동 답장

자동 답장은 별도 단계다. 규칙이 검증되고 사용자가 명시적으로 승인하기 전까지는 draft-only로 둔다.

## English Summary

Use this skill for selected KakaoTalk PC/Mac local archive workflows. The primary verified baseline is Intel Mac x86_64 with KakaoTalk for Mac 26.1.4 build 1163 using `kakaocli 0.4.1` direct SQLCipher DB reads. The same read-only DB probes were reproduced on Apple Silicon arm64 with KakaoTalk for Mac 26.4.1 build 1181.

Text collection should use read-only DB queries. Attachment preservation is freshness-sensitive; run every 1-3 hours for active rooms and record HTTP status without logging raw URLs.

## References

- `references/version-support.md`: supported KakaoTalk/client assumptions and version reporting.
- `references/macos-operations.md`: setup, permissions, commands, schedules, and troubleshooting.
- `references/github-private-distribution.md`: GitHub distribution notes.
