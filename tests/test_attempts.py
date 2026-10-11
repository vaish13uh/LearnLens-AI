
import pytest
from src.attempts import create_attempt, append_attempt, load_attempts


def test_create_attempt_success():
    question = {
        "id": "COD-001",
        "track_id": "coding",
        "topic": "Python Basics",
        "options": ["7", "12", "34", "Error"],
        "answer": "12"
    }
    attempt = create_attempt("learner_123", question, "12")
    assert attempt["learner_id"] == "learner_123"
    assert attempt["question_id"] == "COD-001"
    assert attempt["correct"] == 1
    assert "timestamp" in attempt


def test_create_attempt_invalid_learner():
    question = {"id": "X", "track_id": "x", "topic": "X", "options": ["A"], "answer": "A"}
    with pytest.raises(ValueError):
        create_attempt(" ", question, "A")


def test_append_and_load_attempts(tmp_path):
    test_file = tmp_path / "test_attempts.jsonl"
    attempt = {
        "learner_id": "learner_123",
        "question_id": "COD-001",
        "track_id": "coding",
        "topic": "Python Basics",
        "selected_answer": "12",
        "correct": 1,
        "timestamp": "2023-10-27T12:00:00Z"
    }
    append_attempt(attempt, path=test_file)
    loaded = load_attempts(path=test_file)
    assert len(loaded) == 1
    assert loaded[0]["learner_id"] == "learner_123"
