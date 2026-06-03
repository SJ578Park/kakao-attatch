# Architecture

## Goal

Collect selected KakaoTalk PC conversations and attachment metadata into a local archive that can later support search, summaries, dashboards, and rule-based reply drafts.

## Principles

- Local-first.
- Private by default.
- Allowlist-only chat collection.
- Raw data stays out of git.
- Message collection comes before automation.
- Sending replies requires explicit confirmation until proven safe.

## Data Flow

```text
KakaoTalk local DB/cache
  -> platform adapter
  -> normalized archive.sqlite
  -> attachment queue
  -> local media store
  -> summaries/search/rules
  -> optional draft replies
```

## Suggested Tables

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

## Current Mac Adapter

The current practical adapter shells out to:

```bash
kakaocli query "<SQL>" --db "$databasePath" --key "$key"
```

The local config provides `databasePath` and `key`. These values must never be committed.

