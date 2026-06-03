# GitHub Distribution Guide

## 공개/비공개 운영

이 저장소는 public으로 공개해도 되지만, raw data와 secret이 절대 들어가면 안 됩니다.

public에 올려도 되는 것:

- sanitized docs
- skill files
- schema examples
- fake config example
- public references

public에 올리면 안 되는 것:

- `~/.kakaocli/config.json`
- SQLCipher key
- raw message body
- raw attachment URL
- downloaded media
- archive DB
- account hash가 포함된 local path

## visibility 변경

public으로 바꾸기:

```bash
gh repo edit <owner>/<repo> --visibility public
```

private로 되돌리기:

```bash
gh repo edit <owner>/<repo> --visibility private
```

## repo 생성

```bash
gh repo create <owner>/<repo> --public --source . --remote origin --push
```

이미 repo가 있으면:

```bash
git remote add origin https://github.com/<owner>/<repo>.git
git push -u origin main
```

## 권장 repository settings

- Visibility: public 또는 private. 단, public 기준으로 항상 sanitize.
- Secret scanning 가능하면 활성화.
- collaborator는 GitHub username/team으로 초대.
- ZIP 공유보다 repository access를 권장.

## collaborator invite

```bash
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  /repos/<owner>/<repo>/collaborators/<username> \
  -f permission=read
```

consumer는 `permission=read`, maintainer만 `permission=write`를 사용합니다.

## recipient 설치 안내

사용자는 아래 폴더를 agent skill directory로 복사합니다.

```text
skills/kakao-pc-archive
```

또는 skill manager가 GitHub source install을 지원하면 이 repo에서 설치합니다.

각 사용자는 자신의 local config를 직접 만들어야 합니다. 원 운영자의 SQLCipher key, DB path, media file, archive DB를 공유하지 않습니다.

## release checklist

push 전:

1. Run `git status --short`.
2. Confirm ignored local files are absent from staging.
3. Search for obvious secrets:

```bash
rg -n "databasePath|SQLCipher|key|attachment.url|thumbnailUrl|chat_[0-9a-f]|KakaoTalkMac/Data|BEGIN|token|password" .
```

4. match를 직접 확인하고 private value를 redaction합니다.
5. push합니다.
6. 필요한 collaborator만 초대합니다.

---

# English Summary

The repository can be public if it contains only sanitized docs, examples, schemas, and skill files. Never publish local config, SQLCipher keys, raw messages, raw attachment URLs, downloaded media, or archive DB files.
