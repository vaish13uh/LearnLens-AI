import pandas as pd
from src.features import build_history_features


def test_history_features_exclude_current_answer():
    df = pd.DataFrame({
        "order_id": [1, 2, 3],
        "user_id": [10, 10, 10],
        "skill_id": [5, 5, 5],
        "correct": [1, 0, 1],
        "opportunity": [1, 2, 3]
    })

    result = build_history_features(df)

    assert result["prior_student_count"].tolist() == [0, 1, 2]
    assert result["prior_student_correct"].tolist() == [0, 1, 1]
    assert result["prior_skill_count"].tolist() == [0, 1, 2]
    assert result["prior_skill_correct"].tolist() == [0, 1, 1]


def test_first_interaction_uses_smoothed_accuracy():
    df = pd.DataFrame({
        "order_id": [1],
        "user_id": [10],
        "skill_id": [None],
        "correct": [1],
        "opportunity": [1]
    })

    result = build_history_features(df)

    assert result.iloc[0]["prior_student_accuracy"] == 0.5
    assert result.iloc[0]["prior_skill_accuracy"] == 0.5
