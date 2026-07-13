#!/usr/bin/env python3
"""Import shared demo seed data from data/quiz_bank.db into PostgreSQL.

Requires: Python 3, Docker container `quiz-bank-pg` (or adjust PSQL_CMD),
and Flyway schema already applied (app started once).

Usage (from repo root):
  python scripts/import_seed_from_sqlite.py
"""

from __future__ import annotations

import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQLITE_PATH = ROOT / "data" / "quiz_bank.db"
SQL_OUT = ROOT / "data" / "seed_import.sql"
PSQL_CMD = [
    "docker",
    "exec",
    "-i",
    "quiz-bank-pg",
    "psql",
    "-U",
    "quiz",
    "-d",
    "quiz_bank",
]


def esc(value: str) -> str:
    return value.replace("'", "''")


def main() -> int:
    if not SQLITE_PATH.exists():
        print(f"Missing seed file: {SQLITE_PATH}", file=sys.stderr)
        return 1

    con = sqlite3.connect(SQLITE_PATH)
    con.row_factory = sqlite3.Row
    questions = con.execute(
        """
        SELECT id, question, option_a, option_b, option_c, option_d, correct, difficulty
        FROM questions
        ORDER BY id
        """
    ).fetchall()
    quizzes = con.execute("SELECT id, name FROM quizzes ORDER BY id").fetchall()
    links = con.execute(
        """
        SELECT quiz_id, question_id, position
        FROM quiz_questions
        ORDER BY quiz_id, position
        """
    ).fetchall()
    con.close()

    lines = [
        "TRUNCATE exam_answers, exam_attempts, quiz_questions, quizzes, questions RESTART IDENTITY CASCADE;"
    ]
    for q in questions:
        lines.append(
            "INSERT INTO questions (id, question, option_a, option_b, option_c, option_d, correct, difficulty) "
            f"VALUES ({q['id']}, '{esc(q['question'])}', '{esc(q['option_a'])}', '{esc(q['option_b'])}', "
            f"'{esc(q['option_c'])}', '{esc(q['option_d'])}', '{q['correct']}', '{q['difficulty']}');"
        )
    for quiz in quizzes:
        lines.append(
            f"INSERT INTO quizzes (id, name) VALUES ({quiz['id']}, '{esc(quiz['name'])}');"
        )
    for link in links:
        lines.append(
            "INSERT INTO quiz_questions (quiz_id, question_id, position) "
            f"VALUES ({link['quiz_id']}, {link['question_id']}, {link['position']});"
        )
    lines.append(
        "SELECT setval(pg_get_serial_sequence('questions','id'), (SELECT COALESCE(MAX(id),1) FROM questions));"
    )
    lines.append(
        "SELECT setval(pg_get_serial_sequence('quizzes','id'), (SELECT COALESCE(MAX(id),1) FROM quizzes));"
    )

    SQL_OUT.parent.mkdir(parents=True, exist_ok=True)
    SQL_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {SQL_OUT} ({len(questions)} questions, {len(quizzes)} quizzes)")

    completed = subprocess.run(
        PSQL_CMD,
        input=SQL_OUT.read_text(encoding="utf-8"),
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        print("psql import failed", file=sys.stderr)
        return completed.returncode

    print("Import complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
