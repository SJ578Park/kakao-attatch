# 버전 지원

## 현재 검증 기준

현재는 아래 환경을 기준으로 문서화한다.

```text
지원 수준: macOS verified, Windows unverified
확인일: 2026-06-03
호스트 OS: macOS 13.7.8
KakaoTalk client: KakaoTalk for Mac 26.1.4
수집 adapter: kakaocli direct SQLCipher DB read
첨부 adapter: DB attachment JSON + fresh URL downloader + optional cache watcher
UI automation: kmsg는 send/read 보조용, archive source of truth 아님
이전 첨부 동작 probe: 2026-05-21
```

KakaoTalk for Mac 26.1.4 외 버전은 “동작 가능성이 있음”으로만 보고, 직접 재검증 전에는 지원된다고 말하지 않는다.

## 버전 caveat

KakaoTalk 업데이트로 아래 항목이 바뀔 수 있다.

- local database path
- SQLCipher key derivation
- table names
- column names
- attachment JSON shape
- URL expiry behavior
- macOS Accessibility behavior

## 버전 확인 명령

```bash
mdls -name kMDItemVersion /Applications/KakaoTalk.app
defaults read /Applications/KakaoTalk.app/Contents/Info CFBundleShortVersionString
```

둘 다 실패하면 아래처럼 기록한다.

```text
KakaoTalk version: not verified on this host
```

## 지원 기록 형식

```text
Checked at: YYYY-MM-DD
Host OS: macOS <version>
KakaoTalk app version: <version or not verified>
kakaocli version/commit: <version or not verified>
DB read test: pass/fail
Selected-chat message query: pass/fail
Fresh attachment download probe: pass/fail/not run
Notes: <redacted operational notes only>
```

## 호환성 매트릭스

- macOS 13.7.8 + KakaoTalk for Mac 26.1.4 + `kakaocli`: 현재 검증 기준.
- macOS + 다른 KakaoTalk for Mac 버전: 재검증 필요.
- macOS + `kmsg`: UI send/read/reminder 자동화에 유용하지만 search focus, recent chat state에 취약할 수 있음.
- Windows + KakaoTalk PC: 미검증. 별도 probe 필요.
- Mobile KakaoTalk: 범위 밖.

## 업데이트 후 재검증 체크리스트

1. Full Disk Access가 DB read를 허용하는지 확인한다.
2. `~/.kakaocli/config.json`의 DB 경로가 실제 파일을 가리키는지 확인한다.
3. `NTChatRoom` read-only query를 실행한다.
4. 선택 채팅방의 `NTChatMessage` read-only query를 실행한다.
5. 필수 필드가 존재하는지 확인한다: chat id, message/log id, author, type, body, attachment JSON, sent timestamp.
6. allowlist 채팅방에서 테스트 첨부파일을 하나 보내거나 받은 뒤 `attachment` JSON 구조를 확인한다.
7. fresh URL 다운로드 가능 여부와 HTTP status count를 기록한다.
8. raw URL, 원문 메시지, key, 전체 DB path는 기록하지 않는다.
9. 동작이 바뀌면 이 파일을 업데이트한다.

## 알려진 첨부 동작

로컬 probe에서 관측한 내용:

- 새 이미지/스프레드시트 첨부는 DB `attachment.url`에서 HTTP 200으로 다운로드 가능한 사례가 있었다.
- 오래된 URL은 DB에 metadata가 남아 있어도 HTTP 410을 반환할 수 있다.
- `localFilePath`는 fresh attachment에서 비어 있는 경우가 많다.

운영 결론: 첨부파일은 자주 확인해야 한다. 오래된 첨부파일 복구를 보장하지 않는다.

## English Summary

Verified baseline: macOS 13.7.8, KakaoTalk for Mac 26.1.4, `kakaocli` direct SQLCipher DB reads, checked on 2026-06-03.

Any other KakaoTalk version requires revalidation because DB paths, key derivation, table/column names, attachment JSON shape, URL expiry behavior, and Accessibility behavior can change.

Windows support is not verified.
