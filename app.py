"""
TaskFlow - Week 4: Advanced Features
Flask REST API with:
- Input validation
- Security headers
- Rate-limiting awareness
- Refactored, readable code
"""

from flask import Flask, request, jsonify, abort
import sqlite3
from datetime import datetime
import re

app = Flask(__name__)
DB_PATH = "taskflow.db"

VALID_PRIORITIES = {"low", "medium", "high"}
MAX_TITLE_LENGTH = 200


# ── Security headers ──────────────────────────────────────────
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


# ── DB helper ─────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT NOT NULL,
            priority   TEXT DEFAULT 'medium',
            category   TEXT DEFAULT 'general',
            done       INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)
    return conn


# ── Input validation ──────────────────────────────────────────
def validate_task_input(data: dict) -> tuple[bool, str]:
    title = data.get("title", "").strip()
    if not title:
        return False, "Title is required."
    if len(title) > MAX_TITLE_LENGTH:
        return False, f"Title must be under {MAX_TITLE_LENGTH} characters."
    # sanitise: allow only printable characters
    if not re.match(r'^[\w\s\-.,!?\'\"()]+$', title):
        return False, "Title contains invalid characters."
    priority = data.get("priority", "medium")
    if priority not in VALID_PRIORITIES:
        return False, f"Priority must be one of: {', '.join(VALID_PRIORITIES)}."
    return True, ""


# ── Routes ────────────────────────────────────────────────────
@app.route("/tasks", methods=["GET"])
def list_tasks():
    done_filter = request.args.get("done")
    query = "SELECT * FROM tasks"
    params = []
    if done_filter in ("0", "1"):
        query += " WHERE done = ?"
        params.append(int(done_filter))
    with get_db() as conn:
        rows = conn.execute(query, params).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Request body must be JSON.")

    valid, error = validate_task_input(data)
    if not valid:
        abort(400, description=error)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, priority, category, created_at) VALUES (?, ?, ?, ?)",
            (data["title"].strip(), data.get("priority", "medium"),
             data.get("category", "general"), now)
        )
        conn.commit()
        task_id = cursor.lastrowid

    return jsonify({"id": task_id, "message": "Task created."}), 201


@app.route("/tasks/<int:task_id>/complete", methods=["PATCH"])
def complete_task(task_id):
    with get_db() as conn:
        rows = conn.execute(
            "UPDATE tasks SET done = 1 WHERE id = ?", (task_id,)
        ).rowcount
        conn.commit()
    if rows == 0:
        abort(404, description="Task not found.")
    return jsonify({"message": "Task marked complete."})


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with get_db() as conn:
        rows = conn.execute(
            "DELETE FROM tasks WHERE id = ?", (task_id,)
        ).rowcount
        conn.commit()
    if rows == 0:
        abort(404, description="Task not found.")
    return jsonify({"message": "Task deleted."})


# ── Error handlers ────────────────────────────────────────────
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": str(e.description)}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": str(e.description)}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
