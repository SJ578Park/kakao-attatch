# GitHub 배포

## 현재 배포 방식

현재 저장소는 우선 public으로 공개할 수 있게 관리한다. 필요한 사용자 확인 후 owner가 private로 전환할 수 있다.

public 상태에서 포함해도 되는 것:

- sanitized docs
- skill files
- schema examples
- fake config examples
- 공개 reference URL
- 버전/환경 지원 설명

public 상태에서 포함하면 안 되는 것:

- local config
- raw data
- logs
- DB files
- media files
- credentials
- raw attachment URLs
- 원문 메시지

## 저장소 생성

public repo 생성 예시:

```bash
gh repo create <owner>/<repo> --public --source . --remote origin --push
```

private repo 생성 예시:

```bash
gh repo create <owner>/<repo> --private --source . --remote origin --push
```

이미 repo가 있으면:

```bash
git remote add origin git@github.com:<owner>/<repo>.git
git push -u origin main
```

## public/private 전환

public으로 전환:

```bash
gh repo edit <owner>/<repo> --visibility public --accept-visibility-change-consequences
```

private로 전환:

```bash
gh repo edit <owner>/<repo> --visibility private --accept-visibility-change-consequences
```

## collaborator 초대

private 전환 후 특정 사용자에게만 전달하려면 collaborator를 초대한다.

```bash
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  /repos/<owner>/<repo>/collaborators/<username> \
  -f permission=read
```

소비자는 `permission=read`, 유지보수자는 `permission=write`를 사용한다.

## recipient 설치 안내

수신자는 아래 폴더를 자기 agent skill directory에 복사한다.

```text
skills/kakao-pc-archive
```

각 수신자는 자기 머신에서 로컬 config를 만들어야 한다. 원 운영자의 SQLCipher key, DB path, media file, archive DB를 받으면 안 된다.

## release checklist

push 전:

1. `git status --short` 확인.
2. ignored local file이 staging에 없는지 확인.
3. obvious secret 검색:

```bash
rg -n "databasePath|SQLCipher|key|attachment.url|thumbnailUrl|chat_[0-9a-f]|KakaoTalkMac/Data|BEGIN|token|password" .
```

4. match를 직접 확인하고 private value가 있으면 redaction.
5. public repo라면 특히 `README.md`, `docs/`, `skills/`에 raw data가 없는지 확인.

## English Summary

This repository can be distributed publicly as long as it contains only sanitized documentation, skill files, schemas, fake config examples, and public references. Convert it to private later if distribution should be limited to selected users.
