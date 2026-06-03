#!/usr/bin/env python3
"""Safe KakaoTalk local DB probe.

Prints environment, table counts, required columns, and redacted attachment
field names only. It does not print SQLCipher keys, DB paths, message bodies,
or raw attachment URLs.
"""

from __future__ import annotations

import json
import pathlib
import platform
import plistlib
import re
import subprocess
import sys


def run(cmd: list[str], timeout: int = 20) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)


def query(binary: str, db_path: str, key: str, sql: str) -> object:
    proc = run([binary, "query", sql, "--db", db_path, "--key", key])
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip())
    return json.loads(proc.stdout) if proc.stdout.strip() else None


def first_cell(rows: object) -> object:
    if isinstance(rows, list) and rows and isinstance(rows[0], list) and rows[0]:
        return rows[0][0]
    return rows


def auth_probe(binary: str, user_id: object) -> dict[str, object]:
    if not user_id:
        return {"status": "not_run", "reason": "missing_userId"}

    proc = run([binary, "auth", "--user-id", str(user_id)], timeout=20)
    text = f"{proc.stdout}\n{proc.stderr}"
    tables = sorted(set(re.findall(r"^\s+-\s+(NT[A-Za-z0-9_]+)\s*$", text, re.MULTILINE)))
    required = {"NTChatRoom", "NTChatMessage"}
    return {
        "status": "pass" if proc.returncode == 0 and required.issubset(tables) else "fail",
        "opened": "Database opened successfully!" in text,
        "requiredTablesPresent": {name: name in tables for name in sorted(required)},
        "tableCount": len(tables),
        "error": "" if proc.returncode == 0 else redact_error(text),
    }


def redact_error(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if "Database found:" in line or "Secure key:" in line or "UUID:" in line or "User ID:" in line:
            continue
        lines.append(line)
    return "\n".join(lines).strip()[:160]


def app_version() -> str:
    info = pathlib.Path("/Applications/KakaoTalk.app/Contents/Info.plist")
    if not info.exists():
        return "not found"
    with info.open("rb") as f:
        data = plistlib.load(f)
    return f"{data.get('CFBundleShortVersionString', 'unknown')} build {data.get('CFBundleVersion', 'unknown')}"


def main() -> int:
    cfg_path = pathlib.Path.home() / ".kakaocli" / "config.json"
    binary_path = pathlib.Path.home() / ".local" / "bin" / "kakaocli"
    binary = str(binary_path) if binary_path.exists() else "kakaocli"

    result: dict[str, object] = {
        "host": {
            "machine": platform.machine(),
            "processor": platform.processor(),
            "macos": platform.mac_ver()[0],
            "kakaotalk": app_version(),
        },
        "tools": {},
        "config": {},
        "auth_probe": {},
        "db_probe": {},
        "attachment_probe": {},
    }

    version = run([binary, "--version"], timeout=10)
    result["tools"] = {"kakaocli": (version.stdout or version.stderr).strip() or "unknown"}

    if not cfg_path.exists():
        result["config"] = {"exists": False}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    cfg = json.loads(cfg_path.read_text())
    db_path = cfg.get("databasePath", "")
    key = cfg.get("key", "")
    user_id = cfg.get("userId", "")
    result["config"] = {
        "exists": True,
        "hasDatabasePath": bool(db_path),
        "hasKey": bool(key),
        "hasUserId": bool(user_id),
        "dbExists": pathlib.Path(db_path).exists() if db_path else False,
    }

    result["auth_probe"] = auth_probe(binary, user_id)

    if not (db_path and key):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    for label, sql in {
        "NTChatMessage_count": "select count(*) from NTChatMessage",
        "NTChatRoom_count": "select count(*) from NTChatRoom",
    }.items():
        try:
            result["db_probe"][label] = {"status": "pass", "value": first_cell(query(binary, db_path, key, sql))}
        except Exception as exc:
            result["db_probe"][label] = {"status": "fail", "error": str(exc)[:160]}

    try:
        rows = query(binary, db_path, key, "pragma table_info(NTChatMessage)")
        columns = [row[1] for row in rows if isinstance(row, list) and len(row) > 1] if isinstance(rows, list) else []
        required = ["chatId", "logId", "msgId", "authorId", "type", "message", "attachment", "sentAt", "localFilePath"]
        result["db_probe"]["NTChatMessage_columns"] = {
            "status": "pass",
            "requiredPresent": {name: name in columns for name in required},
        }
    except Exception as exc:
        result["db_probe"]["NTChatMessage_columns"] = {"status": "fail", "error": str(exc)[:160]}

    attachment_sql = """
    select type, attachment
    from NTChatMessage
    where attachment is not null and attachment != ''
    order by sentAt desc
    limit 20
    """
    try:
        rows = query(binary, db_path, key, attachment_sql)
        type_fields: dict[str, set[str]] = {}
        if isinstance(rows, list):
            for row in rows:
                if not (isinstance(row, list) and len(row) >= 2):
                    continue
                msg_type, raw = row[0], row[1]
                try:
                    obj = json.loads(raw) if isinstance(raw, str) else raw
                except Exception:
                    obj = None
                if isinstance(obj, dict):
                    type_fields.setdefault(str(msg_type), set()).update(obj.keys())
        result["attachment_probe"] = {
            "status": "pass",
            "sampledRows": len(rows) if isinstance(rows, list) else 0,
            "fieldNamesByType": {k: sorted(v) for k, v in sorted(type_fields.items())},
        }
    except Exception as exc:
        result["attachment_probe"] = {"status": "fail", "error": str(exc)[:160]}

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
