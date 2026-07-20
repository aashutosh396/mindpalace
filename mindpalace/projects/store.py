"""SQLite store for the v3 palace — TWO layers:

  PROJECTS  the inventory (machine layer): a name + folders/git repos on disk.
            Scanned/managed by the keeper. No chat, no board, no assets.
  ROOMS     the channels (human layer): created BY THE OWNER, like Discord
            channels. A room connects to any number of projects (that's where
            its agent gets folders/grounding) and carries the chat, the kanban
            cards, the assets and the routines.

One DB at <home>/projects/index.db ; room asset bytes at
<home>/rooms/<slug>/assets/. Thread-safe: one connection, WAL, every access
under a lock.
"""
from __future__ import annotations

import re
import sqlite3
import threading
import time

from .. import config

STATUSES = ("todo", "in_progress", "review", "done")
HOME_SLUG = "home"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS project (     -- inventory: resources, not workspaces
  id INTEGER PRIMARY KEY, slug TEXT UNIQUE NOT NULL, name TEXT NOT NULL,
  created_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS repo (
  id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL REFERENCES project(id),
  path TEXT NOT NULL, url TEXT, is_primary INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS room (        -- the owner's channels
  id INTEGER PRIMARY KEY, slug TEXT UNIQUE NOT NULL, name TEXT NOT NULL,
  created_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS room_project (
  room_id INTEGER NOT NULL REFERENCES room(id),
  project_id INTEGER NOT NULL REFERENCES project(id),
  PRIMARY KEY (room_id, project_id));
CREATE TABLE IF NOT EXISTS task (
  id INTEGER PRIMARY KEY, room_id INTEGER NOT NULL REFERENCES room(id),
  title TEXT NOT NULL, body TEXT DEFAULT '', status TEXT NOT NULL DEFAULT 'todo',
  created_by TEXT NOT NULL DEFAULT 'user', session_id TEXT,
  kind TEXT DEFAULT 'task', promise TEXT, iterations INTEGER DEFAULT 0,
  result TEXT DEFAULT '', created_at REAL NOT NULL, closed_at REAL);
CREATE TABLE IF NOT EXISTS task_log (
  id INTEGER PRIMARY KEY, task_id INTEGER NOT NULL REFERENCES task(id),
  text TEXT NOT NULL, created_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS task_thread (
  id INTEGER PRIMARY KEY, task_id INTEGER NOT NULL REFERENCES task(id),
  role TEXT NOT NULL, text TEXT NOT NULL, created_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS routine (
  id INTEGER PRIMARY KEY, room_id INTEGER NOT NULL REFERENCES room(id),
  title TEXT NOT NULL, body TEXT DEFAULT '', schedule TEXT NOT NULL,
  enabled INTEGER DEFAULT 1, last_run REAL, next_run REAL, created_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS chat_message (
  id INTEGER PRIMARY KEY, room_id INTEGER NOT NULL REFERENCES room(id),
  role TEXT NOT NULL, text TEXT NOT NULL, task_id INTEGER REFERENCES task(id),
  created_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS home_chat (
  id INTEGER PRIMARY KEY, role TEXT NOT NULL, text TEXT NOT NULL,
  ref_room_id INTEGER, task_id INTEGER, created_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS asset (
  id INTEGER PRIMARY KEY, room_id INTEGER NOT NULL REFERENCES room(id),
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
    return s or "item"


def _unique_slug(db, table: str, base: str) -> str:
    slug, n = base, 2
    while db.execute(f"SELECT 1 FROM {table} WHERE slug=?", (slug,)).fetchone():
        slug = f"{base}-{n}"; n += 1
    return slug


def room_dir(slug: str):
    return config.home() / "rooms" / slug


# ======================================================================
# PROJECTS — the inventory
# ======================================================================
def create_project(name: str) -> dict:
    with _lock:
        db = _db()
        slug = _unique_slug(db, "project", slugify(name))
        cur = db.execute("INSERT INTO project (slug, name, created_at) VALUES (?,?,?)",
                         (slug, name.strip() or slug, time.time()))
        db.commit()
        pid = cur.lastrowid
    return get_project(pid)


def get_project(pid: int) -> dict | None:
    with _lock:
        r = _db().execute("SELECT * FROM project WHERE id=?", (pid,)).fetchone()
    return dict(r) if r else None


def list_projects() -> list[dict]:
    """Inventory with repo summary + which rooms use each project."""
    with _lock:
        rows = _db().execute("SELECT * FROM project ORDER BY name").fetchall()
        out = []
        for p in _rows(rows):
            repos = _rows(_db().execute(
                "SELECT * FROM repo WHERE project_id=? ORDER BY is_primary DESC, id",
                (p["id"],)).fetchall())
            rooms = _rows(_db().execute(
                """SELECT r.id, r.name, r.slug FROM room_project l
                   JOIN room r ON r.id=l.room_id WHERE l.project_id=?""", (p["id"],)).fetchall())
            out.append({**p, "repos": repos, "rooms": rooms})
    return out


def rename_project(pid: int, name: str) -> dict | None:
    with _lock:
        _db().execute("UPDATE project SET name=? WHERE id=?", (name.strip(), pid))
        _db().commit()
    return get_project(pid)


def delete_project(pid: int) -> bool:
    with _lock:
        db = _db()
        if not db.execute("SELECT 1 FROM project WHERE id=?", (pid,)).fetchone():
            return False
        db.execute("DELETE FROM room_project WHERE project_id=?", (pid,))
        db.execute("DELETE FROM repo WHERE project_id=?", (pid,))
        db.execute("DELETE FROM project WHERE id=?", (pid,))
        db.commit()
    return True


# ---- repos (belong to projects) ----
def add_repo(pid: int, path: str, url: str | None = None, is_primary: bool = False) -> dict:
    with _lock:
        db = _db()
        cur = db.execute("INSERT INTO repo (project_id, path, url, is_primary) VALUES (?,?,?,?)",
                         (pid, path, url, int(is_primary)))
        db.commit()
        r = db.execute("SELECT * FROM repo WHERE id=?", (cur.lastrowid,)).fetchone()
    return dict(r)


def repos_for_project(pid: int) -> list[dict]:
    with _lock:
        rows = _db().execute("SELECT * FROM repo WHERE project_id=? ORDER BY is_primary DESC, id",
                             (pid,)).fetchall()
    return _rows(rows)


def project_repo_paths(pid: int) -> list[str]:
    return [r["path"] for r in repos_for_project(pid)]


def remove_repo(pid: int, repo_id: int) -> bool:
    with _lock:
        db = _db()
        cur = db.execute("DELETE FROM repo WHERE id=? AND project_id=?", (repo_id, pid))
        db.commit()
    return cur.rowcount > 0


# ======================================================================
# ROOMS — the owner's channels
# ======================================================================
def create_room(name: str) -> dict:
    with _lock:
        db = _db()
        slug = _unique_slug(db, "room", slugify(name))
        cur = db.execute("INSERT INTO room (slug, name, created_at) VALUES (?,?,?)",
                         (slug, name.strip() or slug, time.time()))
        db.commit()
        rid = cur.lastrowid
    (room_dir(slug) / "assets").mkdir(parents=True, exist_ok=True)
    return get_room(rid)


def ensure_home_room() -> dict:
    """Hidden system room where the palace-keeper's general cards live."""
    with _lock:
        r = _db().execute("SELECT * FROM room WHERE slug=?", (HOME_SLUG,)).fetchone()
    if r:
        return dict(r)
    with _lock:
        db = _db()
        cur = db.execute("INSERT INTO room (slug, name, created_at) VALUES (?,?,?)",
                         (HOME_SLUG, "Home", time.time()))
        db.commit()
        rid = cur.lastrowid
    return get_room(rid)


def get_room(rid: int) -> dict | None:
    with _lock:
        r = _db().execute("SELECT * FROM room WHERE id=?", (rid,)).fetchone()
    return dict(r) if r else None


def list_rooms(include_home: bool = False) -> list[dict]:
    with _lock:
        rows = _db().execute(
            """SELECT r.*,
                 (SELECT COUNT(*) FROM task t WHERE t.room_id=r.id
                    AND t.status != 'done') AS open_tasks
               FROM room r ORDER BY r.created_at DESC""").fetchall()
    out = _rows(rows)
    if not include_home:
        out = [r for r in out if r["slug"] != HOME_SLUG]
    return out


def rename_room(rid: int, name: str) -> dict | None:
    with _lock:
        _db().execute("UPDATE room SET name=? WHERE id=?", (name.strip(), rid))
        _db().commit()
    return get_room(rid)


def delete_room(rid: int) -> bool:
    """Rows only — room asset files stay on disk. Projects are untouched
    (they're inventory; other rooms may use them)."""
    with _lock:
        db = _db()
        if not db.execute("SELECT 1 FROM room WHERE id=?", (rid,)).fetchone():
            return False
        db.execute("DELETE FROM chat_message WHERE room_id=?", (rid,))
        db.execute("DELETE FROM task_thread WHERE task_id IN "
                   "(SELECT id FROM task WHERE room_id=?)", (rid,))
        db.execute("DELETE FROM task_log WHERE task_id IN "
                   "(SELECT id FROM task WHERE room_id=?)", (rid,))
        db.execute("DELETE FROM task WHERE room_id=?", (rid,))
        db.execute("DELETE FROM routine WHERE room_id=?", (rid,))
        db.execute("DELETE FROM asset WHERE room_id=?", (rid,))
        db.execute("DELETE FROM room_project WHERE room_id=?", (rid,))
        db.execute("DELETE FROM room WHERE id=?", (rid,))
        db.commit()
    return True


# ---- room ↔ project connections ----
def connect_project(rid: int, pid: int) -> bool:
    with _lock:
        db = _db()
        if not db.execute("SELECT 1 FROM project WHERE id=?", (pid,)).fetchone():
            return False
        db.execute("INSERT OR IGNORE INTO room_project (room_id, project_id) VALUES (?,?)",
                   (rid, pid))
        db.commit()
    return True


def disconnect_project(rid: int, pid: int) -> bool:
    with _lock:
        db = _db()
        cur = db.execute("DELETE FROM room_project WHERE room_id=? AND project_id=?", (rid, pid))
        db.commit()
    return cur.rowcount > 0


def projects_for_room(rid: int) -> list[dict]:
    with _lock:
        rows = _db().execute(
            """SELECT p.* FROM room_project l JOIN project p ON p.id=l.project_id
               WHERE l.room_id=? ORDER BY p.name""", (rid,)).fetchall()
    out = []
    for p in _rows(rows):
        out.append({**p, "repos": repos_for_project(p["id"])})
    return out


def room_paths(rid: int) -> list[str]:
    """The room agent's grounding: every folder of every connected project."""
    paths, seen = [], set()
    for p in projects_for_room(rid):
        for r in p["repos"]:
            if r["path"] not in seen:
                seen.add(r["path"])
                paths.append(r["path"])
    return paths


def match_projects_in_text(text: str, exclude_room: int | None = None) -> list[dict]:
    """Inventory projects mentioned (whole-word) in a message — for auto-connect."""
    txt = text.lower()
    already = {p["id"] for p in projects_for_room(exclude_room)} if exclude_room else set()
    out = []
    for p in list_projects():
        if p["id"] in already:
            continue
        for token in {p["name"].lower(), p["slug"]}:
            if len(token) >= 3 and re.search(
                    r"(?<![a-z0-9])" + re.escape(token) + r"(?![a-z0-9])", txt):
                out.append(p)
                break
    return out


def rooms_index() -> list[dict]:
    """What the concierge sees: every room with its projects + board state."""
    out = []
    for r in list_rooms():
        tasks = list_tasks(r["id"])
        open_cards = [t for t in tasks if t["status"] != "done"]
        out.append({
            "slug": r["slug"], "name": r["name"], "id": r["id"],
            "projects": [p["name"] for p in projects_for_room(r["id"])],
            "counts": {s: sum(1 for t in tasks if t["status"] == s) for s in STATUSES},
            "open_titles": [t["title"] for t in open_cards[:3]],
        })
    return out


# ======================================================================
# TASKS (the kanban — lives in rooms)
# ======================================================================
def create_task(rid: int, title: str, body: str = "", created_by: str = "user",
                kind: str = "task", promise: str | None = None) -> dict:
    with _lock:
        db = _db()
        cur = db.execute(
            "INSERT INTO task (room_id, title, body, created_by, kind, promise, created_at) "
            "VALUES (?,?,?,?,?,?,?)",
            (rid, title.strip()[:200], body, created_by, kind, promise, time.time()))
        db.commit()
        r = db.execute("SELECT * FROM task WHERE id=?", (cur.lastrowid,)).fetchone()
    return dict(r)


def get_task(tid: int) -> dict | None:
    with _lock:
        r = _db().execute("SELECT * FROM task WHERE id=?", (tid,)).fetchone()
    return dict(r) if r else None


def list_tasks(rid: int) -> list[dict]:
    with _lock:
        rows = _db().execute("SELECT * FROM task WHERE room_id=? ORDER BY created_at",
                             (rid,)).fetchall()
    return _rows(rows)


def all_tasks() -> list[dict]:
    with _lock:
        rows = _db().execute(
            """SELECT t.*, r.slug AS room_slug, r.name AS room_name
               FROM task t JOIN room r ON r.id = t.room_id
               WHERE t.status != 'done' ORDER BY t.created_at""").fetchall()
        done = _db().execute(
            """SELECT t.*, r.slug AS room_slug, r.name AS room_name
               FROM task t JOIN room r ON r.id = t.room_id
               WHERE t.status = 'done' ORDER BY t.closed_at DESC LIMIT 12""").fetchall()
    return _rows(rows) + list(reversed(_rows(done)))


def set_task_status(tid: int, status: str, result: str | None = None) -> dict | None:
    if status not in STATUSES:
        return None
    with _lock:
        db = _db()
        db.execute("UPDATE task SET status=?, closed_at=?, result=COALESCE(?, result) WHERE id=?",
                   (status, time.time() if status == "done" else None, result, tid))
        db.commit()
    return get_task(tid)


def set_task_iterations(tid: int, n: int) -> dict | None:
    with _lock:
        db = _db()
        db.execute("UPDATE task SET iterations=? WHERE id=?", (n, tid))
        db.commit()
    return get_task(tid)


def set_task_result(tid: int, result: str) -> None:
    with _lock:
        db = _db()
        db.execute("UPDATE task SET result=? WHERE id=?", (result, tid))
        db.commit()


def claim_next_todo(rid: int | None = None) -> dict | None:
    with _lock:
        db = _db()
        q = "SELECT * FROM task WHERE status='todo'"
        args: tuple = ()
        if rid is not None:
            q += " AND room_id=?"; args = (rid,)
        r = db.execute(q + " ORDER BY created_at LIMIT 1", args).fetchone()
        if not r:
            return None
        db.execute("UPDATE task SET status='in_progress' WHERE id=?", (r["id"],))
        db.commit()
        return dict(r) | {"status": "in_progress"}


def add_task_log(tid: int, text: str) -> None:
    with _lock:
        db = _db()
        db.execute("INSERT INTO task_log (task_id, text, created_at) VALUES (?,?,?)",
                   (tid, text[:500], time.time()))
        db.commit()


def list_task_log(tid: int, limit: int = 300) -> list[dict]:
    with _lock:
        rows = _db().execute(
            "SELECT * FROM (SELECT * FROM task_log WHERE task_id=? "
            "ORDER BY created_at DESC LIMIT ?) ORDER BY created_at", (tid, limit)).fetchall()
    return _rows(rows)


def add_thread(tid: int, role: str, text: str) -> dict:
    with _lock:
        db = _db()
        cur = db.execute(
            "INSERT INTO task_thread (task_id, role, text, created_at) VALUES (?,?,?,?)",
            (tid, role, text, time.time()))
        db.commit()
        r = db.execute("SELECT * FROM task_thread WHERE id=?", (cur.lastrowid,)).fetchone()
    return dict(r)


def list_thread(tid: int) -> list[dict]:
    with _lock:
        rows = _db().execute("SELECT * FROM task_thread WHERE task_id=? ORDER BY created_at",
                             (tid,)).fetchall()
    return _rows(rows)


# ======================================================================
# ROUTINES (live in rooms)
# ======================================================================
def _next_run(schedule: str, after: float) -> float:
    kind, _, arg = schedule.partition("@")
    if kind == "every":
        n, unit = int(arg[:-1] or 1), arg[-1]
        return after + n * (3600 if unit == "h" else 60)
    hh, mm = (int(x) for x in arg.split(":"))
    lt = time.localtime(after)
    candidate = time.mktime((lt.tm_year, lt.tm_mon, lt.tm_mday, hh, mm, 0,
                             lt.tm_wday, lt.tm_yday, -1))
    return candidate if candidate > after else candidate + 86400


def add_routine(rid: int, title: str, body: str, schedule: str) -> dict:
    now = time.time()
    with _lock:
        db = _db()
        cur = db.execute(
            "INSERT INTO routine (room_id, title, body, schedule, next_run, created_at) "
            "VALUES (?,?,?,?,?,?)",
            (rid, title.strip()[:200], body, schedule, _next_run(schedule, now), now))
        db.commit()
        r = db.execute("SELECT * FROM routine WHERE id=?", (cur.lastrowid,)).fetchone()
    return dict(r)


def list_routines(rid: int | None = None) -> list[dict]:
    with _lock:
        q = "SELECT * FROM routine" + (" WHERE room_id=?" if rid else "") + " ORDER BY id"
        rows = _db().execute(q, (rid,) if rid else ()).fetchall()
    return _rows(rows)


def delete_routine(rtid: int) -> bool:
    with _lock:
        db = _db()
        cur = db.execute("DELETE FROM routine WHERE id=?", (rtid,))
        db.commit()
    return cur.rowcount > 0


def toggle_routine(rtid: int, enabled: bool) -> dict | None:
    with _lock:
        db = _db()
        db.execute("UPDATE routine SET enabled=? WHERE id=?", (int(enabled), rtid))
        db.commit()
        r = db.execute("SELECT * FROM routine WHERE id=?", (rtid,)).fetchone()
    return dict(r) if r else None


def due_routines(now: float | None = None) -> list[dict]:
    now = now or time.time()
    with _lock:
        rows = _db().execute(
            "SELECT * FROM routine WHERE enabled=1 AND next_run <= ?", (now,)).fetchall()
    return _rows(rows)


def mark_routine_run(rtid: int, schedule: str) -> None:
    now = time.time()
    with _lock:
        db = _db()
        db.execute("UPDATE routine SET last_run=?, next_run=? WHERE id=?",
                   (now, _next_run(schedule, now), rtid))
        db.commit()


# ======================================================================
# CHAT (rooms) + HALL + ASSETS + SEARCH + BRIEF
# ======================================================================
def add_chat(rid: int, role: str, text: str, task_id: int | None = None) -> dict:
    with _lock:
        db = _db()
        cur = db.execute(
            "INSERT INTO chat_message (room_id, role, text, task_id, created_at) VALUES (?,?,?,?,?)",
            (rid, role, text, task_id, time.time()))
        db.commit()
        r = db.execute("SELECT * FROM chat_message WHERE id=?", (cur.lastrowid,)).fetchone()
    return dict(r)


def list_chat(rid: int, limit: int = 200) -> list[dict]:
    with _lock:
        rows = _db().execute(
            "SELECT * FROM (SELECT * FROM chat_message WHERE room_id=? "
            "ORDER BY created_at DESC LIMIT ?) ORDER BY created_at", (rid, limit)).fetchall()
    return _rows(rows)


def add_home_chat(role: str, text: str, ref_room_id: int | None = None,
                  task_id: int | None = None) -> dict:
    with _lock:
        db = _db()
        cur = db.execute(
            "INSERT INTO home_chat (role, text, ref_room_id, task_id, created_at) VALUES (?,?,?,?,?)",
            (role, text, ref_room_id, task_id, time.time()))
        db.commit()
        r = db.execute("SELECT * FROM home_chat WHERE id=?", (cur.lastrowid,)).fetchone()
    return dict(r)


def list_home_chat(limit: int = 200) -> list[dict]:
    with _lock:
        rows = _db().execute(
            "SELECT * FROM (SELECT * FROM home_chat ORDER BY created_at DESC LIMIT ?) "
            "ORDER BY created_at", (limit,)).fetchall()
    return _rows(rows)


def add_asset(rid: int, filename: str, path: str, size: int) -> dict:
    with _lock:
        db = _db()
        cur = db.execute(
            "INSERT INTO asset (room_id, filename, path, size, uploaded_at) VALUES (?,?,?,?,?)",
            (rid, filename, path, size, time.time()))
        db.commit()
        r = db.execute("SELECT * FROM asset WHERE id=?", (cur.lastrowid,)).fetchone()
    return dict(r)


def get_asset(aid: int) -> dict | None:
    with _lock:
        r = _db().execute("SELECT * FROM asset WHERE id=?", (aid,)).fetchone()
    return dict(r) if r else None


def delete_asset(rid: int, aid: int) -> dict | None:
    with _lock:
        db = _db()
        r = db.execute("SELECT * FROM asset WHERE id=? AND room_id=?", (aid, rid)).fetchone()
        if not r:
            return None
        db.execute("DELETE FROM asset WHERE id=?", (aid,))
        db.commit()
    return dict(r)


def list_assets(rid: int) -> list[dict]:
    with _lock:
        rows = _db().execute("SELECT * FROM asset WHERE room_id=? ORDER BY uploaded_at DESC",
                             (rid,)).fetchall()
    return _rows(rows)


def search(q: str, limit: int = 8) -> dict:
    like = f"%{q}%"
    with _lock:
        db = _db()
        rooms = db.execute(
            "SELECT * FROM room WHERE (name LIKE ? OR slug LIKE ?) AND slug != ? LIMIT ?",
            (like, like, HOME_SLUG, limit)).fetchall()
        projects = db.execute(
            "SELECT * FROM project WHERE name LIKE ? OR slug LIKE ? LIMIT ?",
            (like, like, limit)).fetchall()
        tasks = db.execute(
            """SELECT t.*, r.slug AS room_slug, r.name AS room_name FROM task t
               JOIN room r ON r.id = t.room_id
               WHERE t.title LIKE ? OR t.body LIKE ? ORDER BY t.created_at DESC LIMIT ?""",
            (like, like, limit)).fetchall()
        chats = db.execute(
            """SELECT c.*, r.slug AS room_slug, r.name AS room_name FROM chat_message c
               JOIN room r ON r.id = c.room_id
               WHERE c.text LIKE ? ORDER BY c.created_at DESC LIMIT ?""",
            (like, limit)).fetchall()
    return {"rooms": _rows(rooms), "projects": _rows(projects),
            "tasks": _rows(tasks), "chats": _rows(chats)}


def brief_stats(hours: float = 24) -> dict:
    since = time.time() - hours * 3600
    with _lock:
        db = _db()
        review = db.execute(
            """SELECT t.id, t.title, t.result, r.name AS room FROM task t
               JOIN room r ON r.id=t.room_id
               WHERE t.status='review' ORDER BY t.created_at DESC""").fetchall()
        done = db.execute(
            """SELECT t.id, t.title, r.name AS room FROM task t
               JOIN room r ON r.id=t.room_id
               WHERE t.status='done' AND t.closed_at >= ? ORDER BY t.closed_at DESC""",
            (since,)).fetchall()
        created = db.execute(
            "SELECT COUNT(*) AS n FROM task WHERE created_at >= ?", (since,)).fetchone()
        working = db.execute(
            """SELECT t.id, t.title, r.name AS room FROM task t
               JOIN room r ON r.id=t.room_id WHERE t.status='in_progress'""").fetchall()
    return {"review": _rows(review), "done": _rows(done),
            "created": created["n"], "working": _rows(working)}


def has_brief_today() -> bool:
    lt = time.localtime()
    midnight = time.mktime((lt.tm_year, lt.tm_mon, lt.tm_mday, 0, 0, 0, 0, 0, -1))
    with _lock:
        r = _db().execute("SELECT 1 FROM home_chat WHERE role='brief' AND created_at >= ? LIMIT 1",
                          (midnight,)).fetchone()
    return bool(r)
