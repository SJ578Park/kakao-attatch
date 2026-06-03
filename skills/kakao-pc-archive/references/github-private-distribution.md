# Private GitHub Distribution

## Does the User Need to Create the Repository?

No. An agent can create it if GitHub CLI is authenticated and the user has approved the external action.

Recommended command:

```bash
gh repo create <owner>/<repo> --private --source . --remote origin --push
```

If the repo already exists:

```bash
git remote add origin git@github.com:<owner>/<repo>.git
git push -u origin main
```

## Suggested Repository Settings

- Visibility: private.
- Include sanitized docs, skill files, schemas, and scripts only.
- Exclude local configs, raw data, logs, DB files, media, and credentials.
- Enable secret scanning if available.
- Add collaborators by GitHub username or team, not by sharing ZIP files.

## Collaborator Invite

```bash
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  /repos/<owner>/<repo>/collaborators/<username> \
  -f permission=read
```

Use `permission=read` for consumers and `permission=write` only for maintainers.

## Skill Install Guidance for Recipients

Recipients can copy:

```text
skills/kakao-pc-archive
```

into their agent skill directory, or install it through the private repo path if their skill manager supports GitHub sources.

Before first use, each recipient must create their own local config and should not receive the original operator's SQLCipher key, DB path, media files, or archive DB.

## Release Checklist

Before pushing:

1. Run `git status --short`.
2. Confirm ignored local files are absent from staging.
3. Search for obvious secrets:

```bash
rg -n "databasePath|SQLCipher|key|attachment.url|thumbnailUrl|chat_[0-9a-f]|KakaoTalkMac/Data|BEGIN|token|password" .
```

4. Inspect any matches and redact private values.
5. Push to a private repo.
6. Add only intended collaborators.
