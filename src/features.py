import pandas as pd


def build_history_features(df):
    """Create features using only interactions preceding each response."""
    required = {"order_id", "user_id", "skill_id", "correct", "opportunity"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    data = df.copy()
    data["correct"] = pd.to_numeric(data["correct"], errors="coerce")
    data = data.dropna(subset=["user_id", "correct"]).copy()
    data = data[data["correct"].isin([0, 1])].copy()
    data["correct"] = data["correct"].astype(int)
    data["skill_id"] = data["skill_id"].astype("string").fillna("unknown")
    data["opportunity"] = pd.to_numeric(data["opportunity"], errors="coerce")

    data = data.sort_values("order_id", kind="stable").reset_index(drop=True)

    student = data.groupby("user_id", sort=False)["correct"]
    data["prior_student_count"] = student.cumcount()
    data["prior_student_correct"] = student.cumsum() - data["correct"]

    student_skill = data.groupby(
        ["user_id", "skill_id"], sort=False
    )["correct"]
    data["prior_skill_count"] = student_skill.cumcount()
    data["prior_skill_correct"] = (
        student_skill.cumsum() - data["correct"]
    )

    data["prior_student_accuracy"] = (
        data["prior_student_correct"] + 1
    ) / (data["prior_student_count"] + 2)

    data["prior_skill_accuracy"] = (
        data["prior_skill_correct"] + 1
    ) / (data["prior_skill_count"] + 2)

    data["student_position"] = data.groupby(
        "user_id", sort=False
    ).cumcount()
    data["student_total"] = data.groupby(
        "user_id", sort=False
    )["correct"].transform("size")

    data["is_train"] = (
        data["student_position"] < data["student_total"] * 0.8
    )

    return data
