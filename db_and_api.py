"""
TaskFlow - Week 3: Data & APIs
- Stores tasks in a SQLite database
- Fetches a motivational quote from a public API on startup
"""

import sqlite3
import requests
from datetime import datetime

DB_PATH = "taskflow.db"


# ── Database setup ────────────────────────────────────────────
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # return dict-like rows
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL,
                priority    TEXT DEFAULT 'medium',
                category    TEXT DEFAULT 'general',
                done        INTEGER DEFAULT 0,
                created_at  TEXT
            )
        """)
        conn.commit()
    print("Database initialised.")


# ── CRUD operations ───────────────────────────────────────────
def add_task(title: str, priority: str = "medium", category: str = "general") -> int:
    if not title.strip():
        raise ValueError("Title cannot be empty.")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, priority, category, created_at) VALUES (?, ?, ?, ?)",
            (title.strip(), priority, category, now)
        )
        conn.commit()
        print(f"Task added (id={cursor.lastrowid}): {title}")
        return cursor.lastrowid


def get_all_tasks(done: int | None = None) -> list[dict]:
    query = "SELECT * FROM tasks"
    params = []
    if done is not None:
        query += " WHERE done = ?"
        params.append(done)
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]


def complete_task(task_id: int) -> bool:
    with get_connection() as conn:
        rows_changed = conn.execute(
            "UPDATE tasks SET done = 1 WHERE id = ?", (task_id,)
        ).rowcount
        conn.commit()
    return rows_changed > 0


def delete_task(task_id: int) -> bool:
    with get_connection() as conn:
        rows_changed = conn.execute(
            "DELETE FROM tasks WHERE id = ?", (task_id,)
        ).rowcount
        conn.commit()
    return rows_changed > 0


# ── External API ──────────────────────────────────────────────
def fetch_quote() -> str:
    """Fetches a motivational quote from the ZenQuotes API."""
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        response.raise_for_status()
        data = response.json()
        quote = data[0]["q"]
        author = data[0]["a"]
        return f'"{quote}" — {author}'
    except requests.exceptions.RequestException as e:
        # graceful fallback — never crash because of a network issue
        print(f"[Warning] Could not fetch quote: {e}")
        return '"Stay focused and keep building." — You'


# ── Display helper ────────────────────────────────────────────
def display_tasks(tasks: list[dict]):
    if not tasks:
        print("  No tasks found.")
        return
    for t in tasks:
        status = "✅" if t["done"] else "⬜"
        print(f"  [{t['id']}] {status} ({t['priority'].upper()}) {t['title']}  [{t['category']}]")


# ── Demo ──────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()

    # show a motivational quote
    print(f"\n💡 Quote of the day: {fetch_quote()}\n")

    # seed some tasks
    add_task("Set up Flask routes", priority="high", category="backend")
    add_task("Connect frontend to API", priority="medium", category="frontend")
    add_task("Write API documentation", priority="low", category="docs")

    print("\nAll tasks:")
    display_tasks(get_all_tasks())

    # complete first task
    all_tasks = get_all_tasks()
    if all_tasks:
        complete_task(all_tasks[0]["id"])

    print("\nPending tasks:")
    display_tasks(get_all_tasks(done=0))
