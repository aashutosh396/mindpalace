"""
SQLite-backed session store — every turn saved + full-text searchable (FTS5 trigram,
so substring/typo-tolerant recall). The agent injects the top matching past turns as
context on each new message, so it "remembers" across restarts and sessions.

DB lives in the USER-DATA home (memory/sessions.db), never in the core repo.
"""
import sqlite3
import time
from .. import config


def _db_path():
    config.memory_dir().mkdir(parents=True, exist_ok=True)
    return config.memory_dir() / "sessions.db"


def _connect():
    conn = sqlite3.connect(_db_path())
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def init_db():
    conn = _connect()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY, started_at INTEGER NOT NULL );
        CREATE TABLE IF NOT EXISTS turns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL, ts INTEGER NOT NULL,
            role TEXT NOT NULL, content TEXT NOT NULL );
        CREATE VIRTUAL TABLE IF NOT EXISTS turns_fts USING fts5(
            content, content='turns', content_rowid='id', tokenize='trigram' );
        CREATE TRIGGER IF NOT EXISTS turns_ai AFTER INSERT ON turns BEGIN
            INSERT INTO turns_fts(rowid, content) VALUES (new.id, new.content);
        END;
    """)
    conn.commit()
    conn.close()


class SessionStore:
    def __init__(self):
        init_db()
        self._conn = _connect()

    def ensure_session(self, session_id: str):
        self._conn.execute(
            "INSERT OR IGNORE INTO sessions(id, started_at) VALUES (?, ?)",
            (session_id, int(time.time())))
        self._conn.commit()

    def save_turn(self, session_id: str, role: str, content: str):
        self.ensure_session(session_id)
        self._conn.execute(
            "INSERT INTO turns(session_id, ts, role, content) VALUES (?, ?, ?, ?)",
            (session_id, int(time.time()), role, content))
        self._conn.commit()

    def search(self, query: str, limit: int = 3):
        """Return [(role, content, ts)] for the top matching past turns."""
        q = (query or "").strip()
        if len(q) < 3:   # trigram needs >=3 chars
            return []
        try:
            cur = self._conn.execute(
                """SELECT t.role, t.content, t.ts FROM turns_fts f
                   JOIN turns t ON t.id = f.rowid
                   WHERE turns_fts MATCH ? ORDER BY rank LIMIT ?""",
                ('"' + q.replace('"', " ") + '"', limit))
            return cur.fetchall()
        except sqlite3.OperationalError:
            return []

    def close(self):
        self._conn.close()
