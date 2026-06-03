# Platform Support

## 요약

현재 구현은 macOS 전용으로 설명해야 합니다.

archive schema나 selected chat 정책은 나중에 cross-platform으로 확장할 수 있지만, 지금 검증된 DB 접근 경로는 KakaoTalk for Mac, `kakaocli`, SQLCipher, macOS container path, macOS 권한 모델에 의존합니다.

## 검증된 환경

현재 확인된 조합:

- Ghost-Pearl
  - macOS host
  - KakaoTalk for Mac `26.1.4` build `1163`
  - `~/.local/bin/kakaocli 0.4.1`
  - `~/.local/bin/kmsg 0.3.0`
  - `~/.kakaocli/config.json` 존재
- Silver-Pearl
  - macOS host
  - KakaoTalk for Mac `26.4.1` build `1181`
  - `kakaocli 0.4.1`
  - `kmsg 0.3.0`

위 버전은 “동작 확인된 범위”이지 “앞으로 모든 카카오톡 버전에서 보장”을 뜻하지 않습니다.

## macOS 동작 조건

현재 경로:

- `kakaocli`가 KakaoTalk for Mac의 로컬 SQLCipher DB를 read-only로 읽습니다.
- DB 경로와 key는 로컬 `~/.kakaocli/config.json`에서 읽습니다.
- DB read에는 Full Disk Access가 필요할 수 있습니다.
- `kmsg send/read` 같은 UI 기능은 macOS Accessibility permission이 필요합니다.
- Ghost-Pearl처럼 `kakaocli`가 PATH에 없으면 `~/.local/bin/kakaocli` 절대경로를 사용합니다.

KakaoTalk for Mac data area:

```text
~/Library/Containers/com.kakao.KakaoTalkMac/Data/Library/Application Support/com.kakao.KakaoTalkMac
~/Library/Containers/com.kakao.KakaoTalkMac/Data/Library/Caches
```

## 버전 확인 방법

```bash
defaults read /Applications/KakaoTalk.app/Contents/Info CFBundleShortVersionString
defaults read /Applications/KakaoTalk.app/Contents/Info CFBundleVersion
mdls -name kMDItemVersion /Applications/KakaoTalk.app
kakaocli --version
kmsg --version
```

카카오톡 업데이트 후에는 다음을 다시 확인해야 합니다.

1. `~/.kakaocli/config.json`의 `databasePath`가 존재하는지.
2. `kakaocli query`가 read-only query를 실행하는지.
3. `NTChatMessage`에서 text, sent timestamp, attachment JSON을 읽을 수 있는지.
4. 신규 첨부파일 URL이 바로 다운로드 가능한지.
5. 오래된 URL이 410 등으로 만료될 때 실패 상태가 정상 기록되는지.

## Windows

Windows support는 현재 구현에서 검증되지 않았습니다.

공개 reference에는 KakaoTalk for Windows local data path가 아래처럼 언급되지만:

```text
%LOCALAPPDATA%\Kakao\KakaoTalk\users\<hash>\
```

현재 Mac 구현이 Windows에서도 동일하게 동작한다는 뜻은 아닙니다. Windows는 별도 probe가 필요합니다.

- database filename derivation
- SQLCipher key derivation
- table names
- attachment metadata shape
- cache naming
- UI automation path

## 권장 구조

코드화할 때는 다음처럼 나눕니다.

- `core`: normalized archive schema, selected chat policy, run logging
- `adapters/macos-kakaocli`: current verified Mac collector
- `adapters/windows-kakao`: future Windows probe
- `media`: attachment downloader/cache watcher experiments
- `rules`: future conditional reply engine

Windows probe가 local test account에서 chat list와 selected message read를 확인하기 전까지 Windows 지원을 표시하지 않습니다.

---

# English Summary

Current support is macOS-only.

Verified versions:

- KakaoTalk for Mac `26.1.4` build `1163`
- KakaoTalk for Mac `26.4.1` build `1181`
- `kakaocli 0.4.1`
- `kmsg 0.3.0`

This does not guarantee future KakaoTalk versions. Revalidate DB path, SQLCipher access, table fields, attachment JSON, and fresh attachment URL behavior after every KakaoTalk update.
