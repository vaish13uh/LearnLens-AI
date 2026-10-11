import json
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score, roc_auc_score, brier_score_loss, log_loss
)

try:
    from .features import build_history_features
except ImportError:
    from features import build_history_features


FEATURES = [
    "skill_id", "opportunity", "prior_student_count",
    "prior_student_accuracy", "prior_skill_count",
    "prior_skill_accuracy"
]


def evaluate(y_true, probabilities):
    predictions = (probabilities >= 0.5).astype(int)
    return {
        "accuracy": float(accuracy_score(y_true, predictions)),
        "roc_auc": float(roc_auc_score(y_true, probabilities)),
        "brier_score": float(brier_score_loss(y_true, probabilities)),
        "log_loss": float(log_loss(y_true, probabilities, labels=[0, 1]))
    }


def run_experiment(csv_path, output_dir="reports"):
    data = pd.read_csv(csv_path, low_memory=False)
    data = build_history_features(data)

    train = data[data["is_train"]].copy()
    test = data[~data["is_train"]].copy()

    if train.empty or test.empty:
        raise ValueError("Training or test split is empty.")
    if train["correct"].nunique() < 2 or test["correct"].nunique() < 2:
        raise ValueError("Both splits need examples of both target classes.")

    categorical = ["skill_id"]
    numeric = [c for c in FEATURES if c not in categorical]

    preprocessor = ColumnTransformer([
        ("skill", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]), numeric)
    ])

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(
            max_iter=300, solver="liblinear", random_state=42
        ))
    ])

    baseline = DummyClassifier(strategy="prior")
    baseline.fit(train[FEATURES], train["correct"])
    model.fit(train[FEATURES], train["correct"])

    results = {
        "evaluation": "per-student chronological 80/20 split",
        "train_rows": int(len(train)),
        "test_rows": int(len(test)),
        "train_students": int(train["user_id"].nunique()),
        "test_students": int(test["user_id"].nunique()),
        "baseline": evaluate(
            test["correct"],
            baseline.predict_proba(test[FEATURES])[:, 1]
        ),
        "history_aware_logistic_regression": evaluate(
            test["correct"],
            model.predict_proba(test[FEATURES])[:, 1]
        )
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "history_results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to the CSV dataset")
    parser.add_argument("--output-dir", default="reports")
    args = parser.parse_args()

    print(json.dumps(run_experiment(args.data, args.output_dir), indent=2))
