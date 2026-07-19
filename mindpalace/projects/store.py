"""SQLite store for the v3 workspace: projects, repos, tasks, chat, assets.

One DB at  <home>/projects/index.db ; asset bytes live on disk at
<home>/projects/<slug>/assets/ — the DB holds metadata only (vault philosophy).
Thread-safe by construction (uvicorn workers + watchers share it): one connection,
WAL mode, every access under a lock — the same lesson the memory store learned.
"""
from __future__ import annotations

import re
import sqlite3
import threading
import time

from .. import config

STATUSES = ("todo", "in_progress", "review", "done")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS project (
  id INTEGER PRIMARY KEY, slug TEXT UNIQUE NOT NULL, name TEXT NOT NULL,
  created_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS repo (
  id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL REFERENCES project(id),
  path TEXT NOT NULL, url TEXT, is_primary INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS repo_link (      -- repo referenced FROM another project
  project_id INTEGER NOT NULL REFERENCES project(id),
  repo_id INTEGER NOT NULL REFERENCES repo(id),
  PRIMARY KEY (project_id, repo_id));
CREATE TABLE IF NOT EXISTS task (
  id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL REFERENCES project(id),
  title TEXT NOT NULL, body TEXT DEFAULT '', status TEXT NOT NULL DEFAULT 'todo',
  created_by TEXT NOT NULL DEFAULT 'user', session_id TEXT,
  result TEXT DEFAULT '', created_at REAL NOT NULL, closed_at REAL);
CREATE TABLE IF NOT EXISTS chat_message (
  id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL REFERENCES project(id),
  role TEXT NOT NULL, text TEXT NOT NULL, task_id INTEGER REFERENCES task(id),
  created_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS asset (
  id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL REFERENCES project(id),
  filename TEXT NOT NULL, path TEXT NOT NULL, size INTEGER DEFAULT 0,
  uploaded_at REAL NOT NULL);
"""

_conn: sqlite3.Connection | None = None
_lock = threading.Lock()


def _db() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        root = config.home() / "projects"
        root.mkdir(parents=True, exist_ok=True)
        _conn = sqlite3.connect(root / "index.db", check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.execute("PRAGMA journal_mode=WAL")
        _conn.execute("PRAGMA foreign_keys=ON")
        _conn.executescript(_SCHEMA)
        _conn.commit()
    return _conn


def _rows(rows) -> list[dict]:
    return [dict(r) for r in rows]


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "project"


def project_dir(slug: str):
    return config.home() / "projects" / slug


# ---- projects ----
def create_project(name: str) -> dict:
    slug = base = slugify(name)
    with _lock:
        db = _db()
        n = 2
        while db.execute("SELECT 1 FROM project WHERE slug=?", (slug,)).fetchone():
            slug = f"{base}-{n}"; n += 1
        cur = db.execute("INSERT INTO project (slug, name, created_at) VALUES (?,?,?)",
                         (slug, name.strip() or slug, time.time()))
        db.commit()
        pid = cur.lastrowid
    (project_dir(slug) / "assets").mkdir(parents=True, exist_ok=True)
    return get_project(pid)


def get_project(pid: int) -> dict | None:
    with _lock:
        r = _db().execute("SELECT * FROM project WHERE id=?", (pid,)).fetchone()
    return dict(r) if r else None


def list_projects() -> list[dict]:
    with _lock:
        rows = _db().execute(
            """SELECT p.*,
                 (SELECT COUNT(*) FROM task t WHERE t.project_id=p.id
                    AND t.status != 'done') AS open_tasks
               FROM project p ORDER BY p.created_at DESC""").fetchall()
    return _rows(rows)


def rename_project(pid: int, name: str) -> dict | None:
    with _lock:
        _db().execute("UPDATE project SET name=? WHERE id=?", (name.strip(), pid))
        _db().commit()
    return get_project(pid)


def delete_project(pid: int) -> bool:
    """Removes DB rows only — asset files stay on disk for manual cleanup (never
    silently destroy user bytes)."""
    with _lock:
        db = _db()
        if not db.execute("SELECT 1 FROM project WHERE id=?", (pid,)).fetchone():
            return False
        db.execute("DELETE FROM chat_message WHERE project_id=?", (pid,))
        db.execute("DELETE FROM task WHERE project_id=?", (pid,))
        db.execute("DELETE FROM repo_link WHERE project_id=?", (pid,))
        db.execute("DELETE FROM asset WHERE project_id=?", (pid,))
        db.execute("DELETE FROM repo WHERE project_id=?", (pid,))
        db.execute("DELETE FROM project WHERE id=?", (pid,))
        db.commit()
    return True


# ---- repos ----
def add_repo(pid: int, path: str, url: str | None = None, is_primary: bool = False) -> dict:
    with _lock:
        db = _db()
        cur = db.execute("INSERT INTO repo (project_id, path, url, is_primary) VALUES (?,?,?,?)",
                         (pid, path, url, int(is_primary)))
        db.commit()
        r = db.execute("SELECT * FROM repo WHERE id=?", (cur.lastrowid,)).fetchone()
    return dict(r)


def link_repo(pid: int, repo_id: int) -> bool:
    """Reference a repo owned by ANOTHER project (read/write from this project's chat)."""
    with _lock:
        db = _db()
        if not db.execute("SELECT 1 FROM repo WHERE id=?", (repo_id,)).fetchone():
            return False
        db.execute("INSERT OR IGNORE INTO repo_link (project_id, repo_id) VALUES (?,?)",
                   (pid, repo_id))
        db.commit()
    return True


def repos_for(pid: int) -> dict:
    """{'own': [...], 'linked': [...]} — linked rows carry their owner project's slug."""
    with _lock:
        db = _db()
        own = db.execute("SELECT * FROM repo WHERE project_id=? ORDER BY is_primary DESC, id",
                         (pid,)).fetchall()
        linked = db.execute(
            """SELECT r.*, p.slug AS owner_slug FROM repo_link l
               JOIN repo r ON r.id = l.repo_id JOIN project p ON p.id = r.project_id
               WHERE l.project_id=? ORDER BY r.id""", (pid,)).fetchall()
    return {"own": _rows(own), "linked": _rows(linked)}


def repo_paths_for(pid: int) -> list[str]:
    """The task sandbox allowlist: own ∪ linked repo paths (asset dir added by caller)."""
    r = repos_for(pid)
    return [x["path"] for x in r["own"] + r["linked"]]


# ---- tasks (the kanban) ----
def create_task(pid: int, title: str, body: str = "", created_by: str = "user") -> dict:
    with _lock:
        db = _db()
        cur = db.execute(
            "INSERT INTO task (project_id, title, body, created_by, created_at) VALUES (?,?,?,?,?)",
            (pid, title.strip()[:200], body, created_by, time.time()))
        db.commit()
        r = db.execute("SELECT * FROM task WHERE id=?", (cur.lastrowid,)).fetchone()
    return dict(r)


def get_task(tid: int) -> dict | None:
    with _lock:
        r = _db().execute("SELECT * FROM task WHERE id=?", (tid,)).fetchone()
    return dict(r) if r else None


def list_tasks(pid: int) -> list[dict]:
    with _lock:
        rows = _db().execute("SELECT * FROM task WHERE project_id=? ORDER BY created_at",
                             (pid,)).fetchall()
    return _rows(rows)


def set_task_status(tid: int, status: str, result: str | None = None) -> dict | None:
    if status not in STATUSES:
        return None
    with _lock:
        db = _db()
        db.execute("UPDATE task SET status=?, closed_at=?, result=COALESCE(?, result) WHERE id=?",
                   (status, time.time() if status == "done" else None, result, tid))
        db.commit()
    return get_task(tid)


def claim_next_todo(pid: int | None = None) -> dict | None:
    """Atomically take the oldest 'todo' task into 'in_progress' — the worker's pickup.
    Claim happens under the lock so two watchers can never grab the same card."""
    with _lock:
        db = _db()
        q = "SELECT * FROM task WHERE status='todo'"
        args: tuple = ()
        if pid is not None:
            q += " AND project_id=?"; args = (pid,)
        r = db.execute(q + " ORDER BY created_at LIMIT 1", args).fetchone()
        if not r:
            return None
        db.execute("UPDATE task SET status='in_progress' WHERE id=?", (r["id"],))
        db.commit()
        return dict(r) | {"status": "in_progress"}


# ---- chat ----
def add_chat(pid: int, role: str, text: str, task_id: int | None = None) -> dict:
    with _lock:
        db = _db()
        cur = db.execute(
            "INSERT INTO chat_message (project_id, role, text, task_id, created_at) VALUES (?,?,?,?,?)",
            (pid, role, text, task_id, time.time()))
        db.commit()
        r = db.execute("SELECT * FROM chat_message WHERE id=?", (cur.lastrowid,)).fetchone()
    return dict(r)


def list_chat(pid: int, limit: int = 200) -> list[dict]:
    with _lock:
        rows = _db().execute(
            "SELECT * FROM (SELECT * FROM chat_message WHERE project_id=? "
            "ORDER BY created_at DESC LIMIT ?) ORDER BY created_at", (pid, limit)).fetchall()
    return _rows(rows)


# ---- assets ----
def add_asset(pid: int, filename: str, path: str, size: int) -> dict:
    with _lock:
        db = _db()
        cur = db.execute(
            "INSERT INTO asset (project_id, filename, path, size, uploaded_at) VALUES (?,?,?,?,?)",
            (pid, filename, path, size, time.time()))
        db.commit()
        r = db.execute("SELECT * FROM asset WHERE id=?", (cur.lastrowid,)).fetchone()
    return dict(r)


def list_assets(pid: int) -> list[dict]:
    with _lock:
        rows = _db().execute("SELECT * FROM asset WHERE project_id=? ORDER BY uploaded_at DESC",
                             (pid,)).fetchall()
    return _rows(rows)
