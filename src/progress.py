"""Progress summaries for MEOWNEr placement-prep attempts."""

import pandas as pd


ATTEMPT_COLUMNS = [
    "learner_id", "question_id", "track_id", "topic",
    "selected_answer", "correct", "timestamp",
]


def build_progress(attempts, learner_id, min_attempts=1, top_n=3):
    """Summarize a learner's results and rank weaker topics."""
    if min_attempts < 1:
        raise ValueError("min_attempts must be at least 1")
    if top_n < 1:
        raise ValueError("top_n must be at least 1")

    df = pd.DataFrame(attempts)

    if df.empty:
        return {
            "learner_id": learner_id,
            "total_attempts": 0,
            "correct_answers": 0,
            "accuracy": 0.0,
            "topic_progress": [],
            "weak_topics": [],
        }

    missing = set(ATTEMPT_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing attempt fields: {sorted(missing)}")

    df = df[df["learner_id"] == learner_id].copy()

    if df.empty:
        return {
            "learner_id": learner_id,
            "total_attempts": 0,
            "correct_answers": 0,
            "accuracy": 0.0,
            "topic_progress": [],
            "weak_topics": [],
        }

    df["correct"] = pd.to_numeric(df["correct"], errors="raise")

    if not df["correct"].isin([0, 1]).all():
        raise ValueError("correct must contain only 0 or 1")

    total = len(df)
    correct = int(df["correct"].sum())

    topic_df = (
        df.groupby(["track_id", "topic"], as_index=False)
        .agg(
            attempts=("correct", "size"),
            correct_answers=("correct", "sum"),
        )
    )

    topic_df["correct_answers"] = topic_df["correct_answers"].astype(int)
    topic_df["accuracy"] = (
        topic_df["correct_answers"] / topic_df["attempts"]
    )

    topic_progress = topic_df.sort_values(
        ["track_id", "topic"]
    ).to_dict("records")

    weak = topic_df[topic_df["attempts"] >= min_attempts].sort_values(
        ["accuracy", "attempts", "topic"],
        ascending=[True, False, True],
    ).head(top_n)

    return {
        "learner_id": learner_id,
        "total_attempts": total,
        "correct_answers": correct,
        "accuracy": correct / total,
        "topic_progress": topic_progress,
        "weak_topics": weak.to_dict("records"),
    }
