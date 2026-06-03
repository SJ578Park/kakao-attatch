# KakaoTalk Archive Skills

카카오톡 PC/Mac의 로컬 데이터를 읽어 선택한 채팅방의 텍스트와 첨부파일 메타데이터를 아카이브하기 위한 OpenClaw/Codex skill 문서 패키지입니다.

현재 저장소는 **문서와 skill 중심**입니다. 실제 채팅 원문, DB 파일, SQLCipher 키, 로컬 계정 ID, 원본 첨부 URL, 다운로드된 파일은 포함하지 않습니다.

## 현재 공개 상태

이 저장소는 우선 public으로 공개해두고, 필요한 사용자 확인 후 private 전환할 수 있는 구조로 관리합니다.

public 상태에서 지켜야 할 기준:

- 실제 카카오톡 DB 경로, 키, 사용자 ID를 커밋하지 않습니다.
- 채팅 원문, 첨부 URL, 다운로드된 첨부파일을 커밋하지 않습니다.
- 예시는 모두 가짜 값이나 구조 설명만 사용합니다.
- 동작 확인 버전과 한계를 명시합니다.

## 동작 확인 환경

현재 확인된 기준 환경:

```text
확인일: 2026-06-03
호스트 OS: macOS 13.7.8
KakaoTalk for Mac: 26.1.4
수집 방식: kakaocli direct SQLCipher DB read
텍스트 확인: NTChatRoom / NTChatMessage read-only query
첨부파일 확인: NTChatMessage.attachment JSON + fresh URL download attempt
Windows: 미검증
Mobile KakaoTalk: 범위 밖
```

카카오톡 업데이트에 따라 DB 위치, 암호화 키 유도 방식, 테이블/컬럼명, 첨부 JSON 구조, URL 만료 정책이 바뀔 수 있습니다. 따라서 위 버전 외 환경에서는 먼저 `docs/platform-support.md`와 `skills/kakao-pc-archive/references/version-support.md`의 재검증 절차를 실행해야 합니다.

## 핵심 방식

- 텍스트 데이터: KakaoTalk for Mac 로컬 SQLCipher DB를 `kakaocli`로 read-only 조회합니다.
- 첨부파일: 메시지 DB의 `attachment` JSON에서 URL/파일명/MIME/크기/만료값을 읽고, URL이 살아 있을 때 주기적으로 저장을 시도합니다.
- `localFilePath`: 일부 파일에만 존재하므로 주 수집 경로로 보면 안 됩니다.
- `kmsg`: UI 자동화/전송/보조 확인용입니다. 텍스트 아카이브의 주 수집 경로가 아닙니다.
- 수집 범위: 선택한 채팅방 allowlist만 대상으로 합니다. 전체 채팅방 수집을 기본값으로 두지 않습니다.

## 텍스트 데이터 확인 방법

자세한 절차는 `docs/text-data-check.md`를 봅니다.

요약:

1. `~/.kakaocli/config.json`에 `databasePath`, `key`가 있는지 로컬에서 확인합니다.
2. `kakaocli query`로 채팅방 목록을 read-only 조회합니다.
3. 수집할 채팅방만 allowlist에 추가합니다.
4. `NTChatMessage`에서 해당 채팅방의 최근 메시지 몇 건만 조회해 컬럼 구조와 timestamp를 확인합니다.
5. 공유 로그에는 원문 메시지, 키, DB 경로, raw URL을 남기지 않습니다.

## 첨부파일 수집 사용법

자세한 절차는 `docs/attachment-collection.md`를 봅니다.

첨부파일 URL은 시간이 지나면 만료될 수 있습니다. 2026-05-21 로컬 probe에서는 새 이미지/스프레드시트 첨부 URL은 HTTP 200으로 다운로드 가능했고, 오래된 URL은 HTTP 410이 반환되었습니다.

권장 주기:

- 중요한/활성 채팅방: 1시간마다
- 일반 채팅방: 3시간마다
- 낮은 우선순위: 6-12시간마다

`attachmentCollection.intervalHours` 값으로 주기를 표현합니다.

## 저장소 구조

```text
.
├── AGENTS.md
├── README.md
├── SECURITY.md
├── config
│   └── archive.config.example.json
├── docs
│   ├── architecture.md
│   ├── attachment-collection.md
│   ├── conditional-reply.md
│   ├── platform-support.md
│   ├── references.md
│   └── text-data-check.md
├── skills
│   └── kakao-pc-archive
│       ├── SKILL.md
│       └── references
│           ├── github-private-distribution.md
│           ├── macos-operations.md
│           └── version-support.md
└── scripts
    └── README.md
```

## 다른 Agent에 설치

로컬 OpenClaw/Codex 스타일 skill 디렉터리에 복사합니다.

```bash
cp -R skills/kakao-pc-archive ~/.openclaw/agents/<agent-name>/agent/codex-home/skills/
```

각 사용자/머신은 자기 환경에서 로컬 설정을 만들어야 합니다. 원 운영자의 `~/.kakaocli/config.json`, SQLCipher 키, DB 경로, archive DB, 다운로드된 파일을 공유하지 않습니다.

## English Summary

This repository is a documentation-first OpenClaw/Codex skill package for archiving selected KakaoTalk PC/Mac conversations and attachment metadata from local data.

Verified baseline as of 2026-06-03:

- macOS 13.7.8
- KakaoTalk for Mac 26.1.4
- `kakaocli` direct SQLCipher DB reads
- text verification through read-only `NTChatRoom` / `NTChatMessage` queries
- attachment metadata through `NTChatMessage.attachment`
- Windows is not verified

KakaoTalk updates may change DB paths, key derivation, table/column names, attachment JSON shape, or URL expiry behavior. Revalidate before claiming support on another version.
