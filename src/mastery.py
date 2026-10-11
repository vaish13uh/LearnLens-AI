
import pandas as pd


def _clean_interactions(df):
    required = {"order_id", "user_id", "skill_id", "correct"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    data = df.copy()
    data["correct"] = pd.to_numeric(data["correct"], errors="coerce")
    data = data.dropna(subset=["user_id", "correct"]).copy()
    data = data[data["correct"].isin([0, 1])].copy()
    data["correct"] = data["correct"].astype(int)
    data["skill_id"] = (
        data["skill_id"].astype("string").fillna("unknown")
    )
    return data.sort_values("order_id", kind="stable").reset_index(drop=True)


def _mastery_band(score):
    if score < 0.60:
        return "needs_practice"
    if score < 0.80:
        return "developing"
    return "strong"


def build_mastery_features(
    df, prior_strength=4.0, prior_mastery=0.5
):
    """Estimate skill mastery before and after each response."""
    if prior_strength <= 0:
        raise ValueError("prior_strength must be positive")
    if not 0 <= prior_mastery <= 1:
        raise ValueError("prior_mastery must be between 0 and 1")

    data = _clean_interactions(df)

    history = data.groupby(
        ["user_id", "skill_id"], sort=False
    )["correct"]

    data["prior_skill_count"] = history.cumcount()
    data["prior_skill_correct"] = (
        history.cumsum() - data["correct"]
    )

    prior_total = prior_strength * prior_mastery
    data["mastery_before"] = (
        data["prior_skill_correct"] + prior_total
    ) / (data["prior_skill_count"] + prior_strength)

    data["mastery_after"] = (
        data["prior_skill_correct"] + data["correct"] + prior_total
    ) / (data["prior_skill_count"] + 1 + prior_strength)

    data["mastery_band_after"] = data["mastery_after"].map(
        _mastery_band
    )
    return data


def summarize_mastery(
    df, user_id, top_n=3, min_attempts=1,
    prior_strength=4.0, prior_mastery=0.5
):
    """Rank a student's previously attempted skills for practice."""
    if top_n < 1:
        raise ValueError("top_n must be at least 1")
    if min_attempts < 1:
        raise ValueError("min_attempts must be at least 1")
    if prior_strength <= 0:
        raise ValueError("prior_strength must be positive")
    if not 0 <= prior_mastery <= 1:
        raise ValueError("prior_mastery must be between 0 and 1")

    columns = [
        "user_id", "skill_id", "attempts", "correct_answers",
        "mastery_estimate", "mastery_band"
    ]
    data = _clean_interactions(df)
    data = data[
        (data["user_id"] == user_id)
        & (data["skill_id"] != "unknown")
    ]

    if data.empty:
        return pd.DataFrame(columns=columns)

    summary = data.groupby(
        ["user_id", "skill_id"], as_index=False
    ).agg(
        attempts=("correct", "size"),
        correct_answers=("correct", "sum"),
    )

    summary["mastery_estimate"] = (
        summary["correct_answers"] + prior_strength * prior_mastery
    ) / (summary["attempts"] + prior_strength)

    summary["mastery_band"] = summary["mastery_estimate"].map(
        _mastery_band
    )

    summary = summary[summary["attempts"] >= min_attempts]
    return summary.sort_values(
        ["mastery_estimate", "attempts", "skill_id"],
        ascending=[True, False, True],
    ).head(top_n).reset_index(drop=True)
