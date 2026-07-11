import pytest

from backend.database import get_connection, init_db
from backend.exam_repository import ExamAttemptRepository


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "exam_repo.db"
    init_db(path)
    # Seed a quiz (FK target) and a couple of questions (answer FK targets).
    conn = get_connection(path)
    conn.execute("INSERT INTO quizzes (id, name) VALUES (1, 'Quiz')")
    conn.executemany(
        "INSERT INTO questions (id, question, option_a, option_b, option_c, option_d, correct, difficulty)"
        " VALUES (?, ?, 'a', 'b', 'c', 'd', 'A', 'Easy')",
        [(1, "Q1"), (2, "Q2"), (3, "Q3")],
    )
    conn.commit()
    conn.close()
    return path


@pytest.fixture
def repo(db_path):
    return ExamAttemptRepository(db_path=db_path)


def _tables(db_path):
    conn = get_connection(db_path)
    try:
        return {
            r["name"]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
        }
    finally:
        conn.close()


# --- schema ------------------------------------------------------------------


def test_migration_creates_exam_tables(db_path):
    tables = _tables(db_path)
    assert "exam_attempts" in tables
    assert "exam_answers" in tables


def test_existing_tables_intact(db_path):
    tables = _tables(db_path)
    assert {"questions", "quizzes", "quiz_questions"} <= tables

    conn = get_connection(db_path)
    version = conn.execute("PRAGMA user_version").fetchone()[0]
    conn.close()
    assert version == 3


# --- create / read -----------------------------------------------------------


def test_create_attempt_is_pending(repo):
    attempt = repo.create_attempt(1)
    assert attempt["id"] is not None
    assert attempt["quiz_id"] == 1
    assert attempt["submitted_at"] is None
    assert attempt["score"] is None
    assert attempt["total"] is None
    assert attempt["started_at"] is not None


def test_get_attempt_missing_returns_none(repo):
    assert repo.get_attempt(9999) is None


# --- save_answer -------------------------------------------------------------


def test_save_answer_inserts(repo):
    attempt = repo.create_attempt(1)
    repo.save_answer(attempt["id"], 1, "B")
    detail = repo.get_attempt_with_answers(attempt["id"])
    assert len(detail["answers"]) == 1
    assert detail["answers"][0]["question_id"] == 1
    assert detail["answers"][0]["selected_option"] == "B"


def test_save_answer_replaces_existing(repo):
    attempt = repo.create_attempt(1)
    repo.save_answer(attempt["id"], 1, "A")
    repo.save_answer(attempt["id"], 1, "C")  # change answer, same question
    detail = repo.get_attempt_with_answers(attempt["id"])
    assert len(detail["answers"]) == 1  # not duplicated
    assert detail["answers"][0]["selected_option"] == "C"


def test_save_answer_allows_null_selection(repo):
    attempt = repo.create_attempt(1)
    repo.save_answer(attempt["id"], 2, None)  # unanswered
    detail = repo.get_attempt_with_answers(attempt["id"])
    assert detail["answers"][0]["selected_option"] is None


# --- submit ------------------------------------------------------------------


def test_submit_attempt_sets_score_and_timestamp(repo):
    attempt = repo.create_attempt(1)
    repo.save_answer(attempt["id"], 1, "A")
    submitted = repo.submit_attempt(attempt["id"], score=2, total=3)
    assert submitted["score"] == 2
    assert submitted["total"] == 3
    assert submitted["submitted_at"] is not None


def test_submit_missing_attempt_returns_none(repo):
    assert repo.submit_attempt(9999, score=1, total=3) is None


# --- get_attempt_with_answers ------------------------------------------------


def test_get_attempt_with_answers_returns_all(repo):
    attempt = repo.create_attempt(1)
    repo.save_answer(attempt["id"], 1, "A")
    repo.save_answer(attempt["id"], 2, "B")
    repo.save_answer(attempt["id"], 3, None)
    detail = repo.get_attempt_with_answers(attempt["id"])
    assert detail["id"] == attempt["id"]
    assert len(detail["answers"]) == 3
    assert {a["question_id"] for a in detail["answers"]} == {1, 2, 3}


def test_get_attempt_with_answers_missing_returns_none(repo):
    assert repo.get_attempt_with_answers(9999) is None
