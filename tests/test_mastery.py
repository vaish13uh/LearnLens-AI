import pandas as pd
import pytest

from src.mastery import build_mastery_features, summarize_mastery


def sample_data():
    return pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5],
        "user_id": [10, 10, 10, 10, 10],
        "skill_id": ["A", "A", "B", "B", "A"],
        "correct": [1, 0, 1, 1, 0],
    })


def test_mastery_before_uses_only_previous_answers():
    result = build_mastery_features(sample_data())

    assert result.loc[0, "mastery_before"] == pytest.approx(0.5)
    assert result.loc[1, "mastery_before"] == pytest.approx(0.6)
    assert result.loc[2, "mastery_before"] == pytest.approx(0.5)


def test_mastery_updates_after_current_answer():
    result = build_mastery_features(sample_data())

    assert result.loc[0, "mastery_after"] == pytest.approx(0.6)
    assert result.loc[1, "mastery_after"] == pytest.approx(0.5)


def test_recommendations_rank_weaker_skills_first():
    result = summarize_mastery(sample_data(), user_id=10, top_n=2)

    assert list(result["skill_id"]) == ["A", "B"]
    assert result.iloc[0]["mastery_estimate"] < result.iloc[1]["mastery_estimate"]


def test_unknown_student_returns_empty_result():
    result = summarize_mastery(sample_data(), user_id=999)

    assert result.empty


def test_invalid_prior_strength_is_rejected():
    with pytest.raises(ValueError):
        build_mastery_features(sample_data(), prior_strength=0)
