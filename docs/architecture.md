# Architecture

## 목표

선택한 KakaoTalk PC 대화와 첨부파일 metadata를 로컬 archive로 수집합니다. 이후 search, summaries, dashboards, rule-based reply drafts에 사용할 수 있습니다.

## 원칙

- Local-first.
- 공개 저장소에는 sanitized docs/code만 둡니다.
- raw data는 private local storage에만 둡니다.
- allowlist에 들어간 채팅방만 수집합니다.
- message collection이 automation보다 먼저입니다.
- 실제 답장 발송은 충분히 검증될 때까지 confirmation을 요구합니다.

## Data flow

```text
KakaoTalk local DB/cache
  -> platform adapter
  -> normalized archive.sqlite
  -> attachment queue
  -> local media store
  -> summaries/search/rules
  -> optional draft replies
```

## Suggested tables

```sql
create table if not exists source_runs (
  id integer primary key autoincrement,
  started_at text not null,
  finished_at text,
  platform text not null,
  status text not null,
  error text
);

create table if not exists selected_chats (
  id integer primary key autoincrement,
  label text not null,
  match_type text not null,
  match_value text not null,
  enabled integer not null default 1,
  notes text
);

create table if not exists messages (
  chat_id text not null,
  message_id text not null,
  sender_id text,
  sender_label text,
  sent_at integer,
  message_type text,
  body text,
  raw_json text,
  archived_at text not null,
  primary key (chat_id, message_id)
);

create table if not exists attachments (
  id integer primary key autoincrement,
  chat_id text not null,
  message_id text not null,
  asset_index integer not null,
  asset_type text,
  filename_hint text,
  mime_type text,
  size_bytes integer,
  width integer,
  height integer,
  remote_status text,
  local_path text,
  archive_path text,
  raw_json text,
  created_at text not null
);

create table if not exists reply_candidates (
  id integer primary key autoincrement,
  chat_id text not null,
  message_id text,
  rule_id text not null,
  reason text not null,
  draft_reply text,
  status text not null default 'draft',
  created_at text not null
);
```

## Current Mac adapter

현재 macOS adapter는 다음 명령을 사용합니다.

```bash
kakaocli query "<SQL>" --db "$databasePath" --key "$key"
```

local config가 `databasePath`와 `key`를 제공합니다. 이 값은 절대 commit하지 않습니다.

---

# English Summary

The repository can be public, but raw KakaoTalk data must remain private and local. Collect only allowlisted chats, keep raw messages/media/DB files out of git, and require confirmation before real reply sending.
