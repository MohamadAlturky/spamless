import sqlite3
from pathlib import Path


def _db_path() -> Path:
    p = Path.home() / ".spamless"
    p.mkdir(exist_ok=True)
    return p / "plans.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(_db_path()))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                title      TEXT    NOT NULL,
                content    TEXT    NOT NULL DEFAULT '',
                created_at TEXT    NOT NULL DEFAULT (datetime('now'))
            )
        """)


def create_plan(title: str) -> int:
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO plans (title) VALUES (?)", (title,)
        )
        return cur.lastrowid


def list_plans(page: int, page_size: int = 5) -> tuple[list[dict], int]:
    offset = (page - 1) * page_size
    with _connect() as conn:
        total = conn.execute("SELECT COUNT(*) FROM plans").fetchone()[0]
        rows = conn.execute(
            "SELECT id, title, created_at FROM plans ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (page_size, offset),
        ).fetchall()
    return [dict(r) for r in rows], total


def get_plan(plan_id: int) -> dict | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, title, content, created_at FROM plans WHERE id = ?", (plan_id,)
        ).fetchone()
    return dict(row) if row else None


def save_plan(plan_id: int, content: str) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE plans SET content = ? WHERE id = ?", (content, plan_id)
        )


def delete_plan(plan_id: int) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM plans WHERE id = ?", (plan_id,))
