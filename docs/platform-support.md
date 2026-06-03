# 동작 환경과 버전 지원

## 현재 결론

현재 구현은 **macOS KakaoTalk for Mac 전용으로 기록**되어 있습니다. 다만 검증 수준은 환경별로 다릅니다.

검증 기준:

```text
확인일: 2026-06-03
기본 검증 호스트:
  - Intel Mac: x86_64, Intel Core i5, macOS 13.7.8, KakaoTalk for Mac 26.1.4 build 1163
  - 수집 adapter: kakaocli 0.4.1 direct SQLCipher DB read
  - 텍스트 확인: NTChatRoom / NTChatMessage read-only query
  - 첨부 확인: NTChatMessage.attachment JSON + fresh URL download attempt
Apple Silicon 재검증 호스트:
  - Apple Silicon Mac: arm64, Apple M4, macOS 26.4.1, KakaoTalk for Mac 26.4.1 build 1181
  - 통과: kakaocli auth --user-id, DB 파일 탐색, SQLCipher open, NTChatRoom / NTChatMessage 테이블 확인
  - 미통과/미확인: userId 자동탐색, kakaocli query, 외부 sqlcipher 직접 query, fresh attachment URL download
UI 자동화: kmsg 0.3.0은 send/read 보조용, archive source of truth 아님
```

기본 검증 기준은 Intel Mac 환경입니다. Apple Silicon Mac에서는 DB 파일과 주요 테이블 open까지만 재현되었습니다. 메시지 query와 첨부 URL 다운로드까지 통과하기 전에는 Apple Silicon 환경을 완전 지원으로 표시하지 않습니다.

이 기능은 카카오톡 버전에 영향을 받을 수 있습니다. KakaoTalk for Mac이 업데이트되면 다음 요소가 바뀔 수 있습니다.

- 로컬 DB 위치
- SQLCipher key derivation 방식
- DB 파일명
- `NTChatRoom`, `NTChatMessage` 테이블 존재 여부
- 메시지 컬럼명
- `attachment` JSON 구조
- 첨부 URL 만료 시간과 HTTP 응답 정책
- macOS Accessibility 동작

따라서 **KakaoTalk for Mac 26.1.4 build 1163 외 버전에서는 지원을 주장하기 전에 재검증**해야 합니다. 26.4.1 build 1181은 DB open 부분 재검증 기록으로만 취급합니다.

## macOS

현재 경로:

- `kakaocli`가 KakaoTalk for Mac 로컬 SQLCipher DB를 read-only로 읽습니다.
- DB 경로와 key는 로컬 `~/.kakaocli/config.json`에서 읽습니다.
- DB 읽기에는 Full Disk Access가 필요할 수 있습니다.
- UI 기능(send/read/harvest 등)은 macOS Accessibility 권한에 의존합니다.

알려진 KakaoTalk Mac 데이터 영역:

```text
~/Library/Containers/com.kakao.KakaoTalkMac/Data/Library/Application Support/com.kakao.KakaoTalkMac
~/Library/Containers/com.kakao.KakaoTalkMac/Data/Library/Caches
```

공개 문서에는 실제 계정 hash가 포함된 전체 경로를 쓰지 않습니다.

## Windows

Windows KakaoTalk PC는 아직 검증되지 않았습니다.

공개 자료상 Windows 로컬 데이터 경로로 아래 형태가 언급되지만, 현재 macOS 구현이 Windows에서도 동작한다는 뜻은 아닙니다.

```text
%LOCALAPPDATA%\Kakao\KakaoTalk\users\<hash>\
```

Windows에서 별도로 확인해야 할 항목:

- DB 위치
- 암호화/키 유도 방식
- 테이블명과 컬럼명
- 첨부 JSON 구조
- cache/download 폴더 구조
- Task Scheduler 기반 주기 실행
- UI 자동화 가능 여부

## 버전 재검증 절차

KakaoTalk 업데이트 후에는 아래를 다시 확인합니다.

1. KakaoTalk 앱 버전을 기록합니다.
2. `~/.kakaocli/config.json`에 `databasePath`, `key`, `userId` 중 어떤 값이 있는지 확인합니다.
3. `kakaocli auth`가 실패하면 `kakaocli auth --user-id <local_user_id>`로 DB open을 확인합니다.
4. DB 파일이 존재하고 `NTChatRoom` / `NTChatMessage` 테이블이 보이는지 확인합니다.
5. `kakaocli query` 또는 collector가 실제 read-only query를 실행할 수 있는지 확인합니다.
6. `NTChatRoom`에서 채팅방 목록을 조회합니다.
7. 선택한 채팅방의 `NTChatMessage`를 조회합니다.
8. 새 첨부파일을 하나 받아 `attachment` JSON 구조와 즉시 다운로드 가능 여부를 확인합니다.
9. 결과는 pass/fail과 HTTP status count만 기록합니다.
10. 원문 메시지, key, raw URL, 계정별 DB path는 기록하지 않습니다.

## English Summary

The primary verified baseline is an Intel Mac (x86_64, Intel Core i5, macOS 13.7.8) running KakaoTalk for Mac 26.1.4 build 1163. Apple Silicon arm64 / Apple M4 with KakaoTalk for Mac 26.4.1 build 1181 was rechecked only up to `kakaocli auth --user-id`, database open, and `NTChatRoom` / `NTChatMessage` table visibility. Automatic user ID detection, `kakaocli query`, external SQLCipher queries, and fresh attachment URL download were not fully verified on that environment.

KakaoTalk updates may change DB paths, key derivation, table names, columns, attachment JSON shape, URL expiry behavior, or Accessibility behavior. Revalidate before claiming support on another KakaoTalk version.

Windows support is not verified.
