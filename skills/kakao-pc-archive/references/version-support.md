# Version Support

## 현재 검증된 범위

이 workflow는 다음처럼 설명합니다.

```text
지원 수준: macOS 검증, Windows 미검증
카카오톡 클라이언트: KakaoTalk for Mac
검증된 카카오톡 버전: 26.1.4 build 1163, 26.4.1 build 1181
텍스트 수집: kakaocli 0.4.1 direct SQLCipher DB read
첨부파일 수집: DB attachment JSON + fresh URL downloader + optional cache watcher
UI 자동화: kmsg 0.3.0 send/read only, archive source of truth 아님
마지막 첨부파일 동작 probe: 2026-05-21
```

## 버전 주의사항

카카오톡은 버전에 따라 local database path, SQLCipher key derivation, table name, field name, attachment JSON shape, URL expiry behavior, UI accessibility behavior가 바뀔 수 있습니다.

따라서 다른 환경에서 “동작한다”고 말하기 전에 반드시 local version을 기록합니다.

```bash
mdls -name kMDItemVersion /Applications/KakaoTalk.app
defaults read /Applications/KakaoTalk.app/Contents/Info CFBundleShortVersionString
```

위 명령이 동작하지 않으면 다음처럼 기록합니다.

```text
KakaoTalk version: not verified on this host
```

## Compatibility matrix

- macOS + KakaoTalk for Mac 26.1.4/26.4.1 + `kakaocli 0.4.1`: 현재 확인된 접근.
- macOS + `kmsg 0.3.0`: send/read/reminder에는 유용하지만 search focus와 recent chat 상태에 민감.
- Windows + KakaoTalk PC: 미검증. 별도 probe 필요.
- Mobile KakaoTalk: 범위 밖.

## 업데이트 후 재검증 checklist

KakaoTalk 업데이트 후 아래를 확인합니다.

1. Full Disk Access로 DB read가 가능한지.
2. `~/.kakaocli/config.json`의 DB path가 존재하는지.
3. read-only selected-chat query가 성공하는지.
4. 필수 필드가 있는지: chat id, message/log id, author, message type, body, attachment JSON, sent timestamp.
5. allowlisted room에서 test attachment를 송수신합니다.
6. attachment JSON field와 즉시 다운로드 동작을 확인합니다.
7. raw URL 대신 HTTP status count만 기록합니다.
8. 동작이 바뀌면 이 파일을 업데이트합니다.

## 확인된 첨부파일 동작

관측된 local behavior:

- 신규/미읽음 이미지와 spreadsheet 첨부는 DB `attachment.url`에서 HTTP 200을 반환할 수 있었습니다.
- 오래된 URL은 metadata가 DB에 남아 있어도 HTTP 410을 반환할 수 있었습니다.
- fresh attachment의 `localFilePath`는 비어 있는 경우가 많았습니다.

운영 결론: active room은 1-3시간 주기로 fresh capture를 돌립니다. 오래된 첨부파일 복구를 보장하지 않습니다.

---

# English Summary

Verified scope:

- macOS only.
- KakaoTalk for Mac `26.1.4` build `1163`.
- KakaoTalk for Mac `26.4.1` build `1181`.
- `kakaocli 0.4.1`.
- `kmsg 0.3.0`.

KakaoTalk updates can break DB access, field names, attachment JSON shape, URL expiry, or UI automation. Revalidate after every KakaoTalk update.
