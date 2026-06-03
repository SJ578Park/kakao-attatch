# AGENTS.md - KakaoTalk Archive Skill Package

이 저장소는 선택한 KakaoTalk PC/Mac 채팅방의 텍스트와 첨부파일 메타데이터를 다루기 위한 OpenClaw/Codex skill 패키지다.

## 역할

이 저장소를 사용하는 agent는 local-first, privacy-sensitive archive workflow로 취급한다.

주요 작업:

- 선택한 KakaoTalk for Mac 채팅방 메시지를 로컬 DB에서 read-only로 확인한다.
- 첨부파일 metadata와 fresh URL 다운로드 가능 여부를 기록한다.
- KakaoTalk/client 버전을 기록한 뒤 지원 여부를 말한다.
- raw chat data, media, DB files, keys, user IDs, raw URLs를 git에 넣지 않는다.

## 시작 순서

작업 전 아래 파일을 읽는다.

1. `README.md`
2. `SECURITY.md`
3. `docs/platform-support.md`
4. `docs/text-data-check.md`
5. `docs/attachment-collection.md`
6. `skills/kakao-pc-archive/SKILL.md`
7. `skills/kakao-pc-archive/references/version-support.md`

## 공개 저장소 기준

현재 저장소는 public으로 공개될 수 있다. 따라서 문서와 예시는 공개 가능한 수준으로만 작성한다.

- 실제 DB path, key, account hash를 쓰지 않는다.
- 원문 메시지와 raw attachment URL을 쓰지 않는다.
- 다운로드된 첨부파일을 커밋하지 않는다.
- 동작 버전과 미검증 범위를 명확히 쓴다.
- 공개 references는 URL만 남기고 private local note는 넣지 않는다.
- 내부 호스트명이나 개인 장비명 대신 `Intel Mac`, `Apple Silicon Mac`처럼 외부인이 이해할 수 있는 환경명으로 쓴다.

## 금지 사항

- 전체 채팅방 수집을 기본값으로 두지 않는다.
- SQLCipher key, raw message body, raw attachment URL, full account-specific DB path를 출력하지 않는다.
- local config, archive DB, logs, media output을 커밋하지 않는다.
- 사용자가 명시적으로 승인하기 전까지 실제 카카오톡 메시지를 자동 전송하지 않는다.
- Windows는 별도 probe 전까지 지원된다고 말하지 않는다.

## 지원 문구

새 검증 결과가 없으면 아래 문구를 사용한다.

```text
Intel Mac x86_64 + macOS 13.7.8 + KakaoTalk for Mac 26.1.4 build 1163 + kakaocli 0.4.1 direct SQLCipher DB read가 기본 검증 기준이다. Apple Silicon arm64 + Apple M4 + KakaoTalk for Mac 26.4.1 build 1181은 해당 장비에서 safe probe 통과 후 confirmed로 승격한다.
Windows KakaoTalk support는 research-only다.
첨부파일 보존은 best-effort이며 URL 만료 전에 주기적으로 확인해야 한다.
```

## 배포 전 체크

1. `git status --short` 확인.
2. `skills/kakao-pc-archive/references/github-private-distribution.md`의 secret scan 실행.
3. public 상태에서 공개 가능한 내용만 stage했는지 확인.
4. raw data, local config, media, DB 파일이 staging에 없는지 확인.

## English Summary

Agents should treat this repository as a public-safe, local-first KakaoTalk archive skill package. Do not commit raw chats, DB files, SQLCipher keys, account-specific paths, raw attachment URLs, logs, or media.
