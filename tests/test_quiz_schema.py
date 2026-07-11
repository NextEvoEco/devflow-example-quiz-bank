import pytest

from backend.database import get_connection, init_db


@pytest.fixture
def conn(tmp_path):
    db_path = tmp_path / "schema_test.db"
    init_db(db_path)
    connection = get_connection(db_path)
    yield connection
    connection.close()


def columns(conn, table):
    return {row["name"] for row in conn.execute(f"PRAGMA table_info({table})")}


def test_schema_version_at_least_2(conn):
    # The quiz schema landed at v2; later objectives advance the version further.
    assert conn.execute("PRAGMA user_version").fetchone()[0] >= 2


def test_quizzes_table_columns(conn):
    assert columns(conn, "quizzes") == {"id", "name", "created_at"}


def test_quiz_questions_table_columns(conn):
    assert columns(conn, "quiz_questions") == {"quiz_id", "question_id", "position"}


def test_quiz_questions_foreign_keys(conn):
    fks = conn.execute("PRAGMA foreign_key_list(quiz_questions)").fetchall()
    mapping = {fk["from"]: fk["table"] for fk in fks}
    assert mapping.get("quiz_id") == "quizzes"
    assert mapping.get("question_id") == "questions"


def test_position_column_is_integer(conn):
    types = {row["name"]: row["type"] for row in conn.execute("PRAGMA table_info(quiz_questions)")}
    assert types["position"].upper() == "INTEGER"


def test_questions_table_unaffected(conn):
    # V1 questions table and its columns must remain intact after the v2 migration.
    assert columns(conn, "questions") == {
        "id", "question", "option_a", "option_b", "option_c", "option_d",
        "correct", "difficulty",
    }


def test_migration_is_idempotent(tmp_path):
    db_path = tmp_path / "idempotent.db"
    init_db(db_path)
    # Insert a question through the raw schema, then re-run init_db.
    conn = get_connection(db_path)
    conn.execute(
        "INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct, difficulty)"
        " VALUES ('q', 'a', 'b', 'c', 'd', 'A', 'Easy')"
    )
    conn.commit()
    conn.close()

    init_db(db_path)  # running again must not error or wipe data

    conn = get_connection(db_path)
    count = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    version = conn.execute("PRAGMA user_version").fetchone()[0]
    conn.close()
    assert count == 1
    assert version >= 2


def test_cascade_delete_removes_join_rows(tmp_path):
    db_path = tmp_path / "cascade.db"
    init_db(db_path)
    conn = get_connection(db_path)
    conn.execute(
        "INSERT INTO questions (id, question, option_a, option_b, option_c, option_d, correct, difficulty)"
        " VALUES (1, 'q', 'a', 'b', 'c', 'd', 'A', 'Easy')"
    )
    conn.execute("INSERT INTO quizzes (id, name) VALUES (1, 'Quiz')")
    conn.execute("INSERT INTO quiz_questions (quiz_id, question_id, position) VALUES (1, 1, 0)")
    conn.commit()

    conn.execute("DELETE FROM quizzes WHERE id = 1")
    conn.commit()
    remaining = conn.execute("SELECT COUNT(*) FROM quiz_questions").fetchone()[0]
    conn.close()
    assert remaining == 0
