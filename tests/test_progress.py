
import pytest
from src.progress import build_progress


def make_attempt(learner, topic, correct, track="aptitude"):
    return {
        "learner_id": learner,
        "question_id": f"Q-{topic}-{correct}",
        "track_id": track,
        "topic": topic,
        "selected_answer": "answer",
        "correct": correct,
        "timestamp": "2026-10-11T10:00:00+00:00",
    }


def test_empty_history_returns_zero_progress():
    result = build_progress([], "learner-1")
    assert result["total_attempts"] == 0
    assert result["accuracy"] == 0.0
    assert result["weak_topics"] == []


def test_overall_accuracy_is_calculated():
    attempts = [
        make_attempt("learner-1", "Percentages", 1),
        make_attempt("learner-1", "Percentages", 0),
        make_attempt("learner-1", "Averages", 1),
    ]
    result = build_progress(attempts, "learner-1")
    assert result["total_attempts"] == 3
    assert result["correct_answers"] == 2
    assert result["accuracy"] == pytest.approx(2 / 3)


def test_weak_topics_ranking_and_filtering():
    attempts = [
        make_attempt("learner-1", "Percentages", 0),
        make_attempt("learner-1", "Percentages", 0),
        make_attempt("learner-1", "Averages", 1),
        make_attempt("learner-1", "Averages", 0),
    ]
    result = build_progress(attempts, "learner-1", min_attempts=2, top_n=1)
    assert len(result["weak_topics"]) == 1
    assert result["weak_topics"][0]["topic"] == "Percentages"


def test_other_learners_are_excluded():
    attempts = [
        make_attempt("learner-1", "Percentages", 1),
        make_attempt("learner-2", "Percentages", 0),
    ]
    result = build_progress(attempts, "learner-1")
    assert result["total_attempts"] == 1
    assert result["accuracy"] == 1.0


def test_minimum_attempts_filters_weak_topics():
    attempts = [
        make_attempt("learner-1", "Percentages", 0),
        make_attempt("learner-1", "Averages", 1),
        make_attempt("learner-1", "Averages", 1),
    ]
    result = build_progress(attempts, "learner-1", min_attempts=2)
    assert all(t["attempts"] >= 2 for t in result["weak_topics"])


def test_invalid_correctness_is_rejected():
    attempts = [make_attempt("learner-1", "Percentages", 2)]
    with pytest.raises(ValueError):
        build_progress(attempts, "learner-1")


def test_invalid_top_n_is_rejected():
    with pytest.raises(ValueError):
        build_progress([], "learner-1", top_n=0)
