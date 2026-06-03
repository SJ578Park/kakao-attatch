# Kakao PC Archive Notes

카카오톡 PC 대화 텍스트와 첨부파일 메타데이터를 로컬에서 수집하기 위한 문서/스킬 초안입니다.

이 저장소는 공개 가능한 설명, 예시 설정, 스키마, OpenClaw skill만 담습니다. 실제 카카오톡 메시지, SQLCipher key, raw attachment URL, 로컬 DB 경로, 다운로드한 첨부파일은 절대 커밋하지 않습니다.

## 현재 지원 상태

- 지원 상태: macOS 검증, Windows 미검증.
- 검증된 앱: KakaoTalk for Mac.
- 검증된 카카오톡 버전:
  - Ghost-Pearl: KakaoTalk `26.1.4` build `1163`
  - Silver-Pearl: KakaoTalk `26.4.1` build `1181`
- 검증된 도구:
  - `kakaocli 0.4.1`
  - `kmsg 0.3.0`
- 텍스트 수집 기준: `kakaocli`가 KakaoTalk for Mac의 로컬 SQLCipher DB를 read-only로 읽는 방식.
- 첨부파일 기준: DB의 attachment JSON과 fresh URL을 빠르게 확인하고, 만료된 URL은 HTTP 410으로 기록.
- 수집 범위: allowlist에 넣은 채팅방만. 모든 채팅방 전체 수집은 기본값으로 금지.

카카오톡 업데이트로 DB 경로, key derivation, 테이블/필드명, attachment JSON 구조, URL 만료 정책, macOS 권한 동작이 바뀌면 동작하지 않을 수 있습니다. 위 버전 밖에서는 먼저 `docs/platform-support.md`와 `skills/kakao-pc-archive/references/version-support.md`의 재검증 절차를 따라야 합니다.

## 빠른 사용법

1. KakaoTalk for Mac 버전을 확인합니다.
2. `~/.kakaocli/config.json`이 있고 `databasePath`, `key`가 들어있는지 확인합니다.
3. `kakaocli query`로 selected chat의 최신 텍스트 row를 read-only로 확인합니다.
4. 첨부파일은 만료 전에 확인해야 합니다. active room은 1-3시간 주기 수집을 권장합니다.
5. raw message, raw URL, DB, media는 `data/`, `logs/`, `media/`처럼 gitignore된 로컬 경로에만 둡니다.

자세한 절차는 `docs/usage.md`를 보세요.

## Repository Layout

```text
.
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
│   └── usage.md
├── skills
│   └── kakao-pc-archive
│       ├── SKILL.md
│       └── references
│           ├── github-distribution.md
│           ├── macos-operations.md
│           └── version-support.md
└── scripts
    └── README.md
```

## 최소 안전 workflow

1. `config/archive.config.example.json`을 로컬 ignored config로 복사합니다.
2. 수집 대상 채팅방을 명시적으로 allowlist에 넣습니다.
3. `attachmentCollection.intervalHours`를 설정합니다.
4. 로컬에서만 수집을 실행하고 raw data는 git 밖에 둡니다.
5. commit에는 sanitized docs, schemas, code만 포함합니다.

## Agent Skill

다른 에이전트가 이 workflow를 사용하거나 확장해야 하면 `skills/kakao-pc-archive`를 해당 에이전트의 skills directory로 복사합니다.

이 skill은 다음을 분리해서 설명합니다.

- macOS + `kakaocli` DB 수집
- 첨부파일 fresh capture
- `kmsg` UI send/read 자동화
- Windows future research
- GitHub 공개/비공개 배포 노트

## Can This Reply Automatically?

가능하지만 reply automation은 2단계입니다.

현재 단계는 local collection과 normalized storage 안정화가 우선입니다. archive가 안정화된 뒤 rule engine이 특정 조건을 감지하고 답장 초안을 만들 수 있습니다. 실제 외부 발송은 규칙이 충분히 검증될 때까지 human confirmation을 유지합니다.

---

# English Summary

This repository documents a local-first KakaoTalk PC archive workflow.

Current verified scope:

- macOS only.
- KakaoTalk for Mac `26.1.4` build `1163` and `26.4.1` build `1181`.
- `kakaocli 0.4.1` for read-only SQLCipher DB reads.
- `kmsg 0.3.0` for UI send/read automation only.

KakaoTalk updates may break local DB access, field names, attachment JSON, URL expiry behavior, or accessibility automation. Revalidate before claiming support on another version.
