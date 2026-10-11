"""Evaluation helpers for binary student-response prediction."""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    log_loss,
    roc_auc_score,
)


def evaluate_binary_predictions(y_true, probabilities, threshold=0.5):
    """Return standard metrics for predicted probabilities.

    probabilities must represent P(correct answer), between 0 and 1.
    ROC-AUC is undefined when y_true contains only one class.
    """
    y_true = np.asarray(y_true, dtype=int)
    probabilities = np.asarray(probabilities, dtype=float)

    if y_true.ndim != 1 or probabilities.ndim != 1:
        raise ValueError("Inputs must be one-dimensional.")
    if len(y_true) == 0 or len(y_true) != len(probabilities):
        raise ValueError("Inputs must have the same non-zero length.")
    if not np.isin(y_true, [0, 1]).all():
        raise ValueError("y_true must contain only 0 and 1.")
    if not np.isfinite(probabilities).all():
        raise ValueError("Probabilities must be finite.")
    if ((probabilities < 0) | (probabilities > 1)).any():
        raise ValueError("Probabilities must be between 0 and 1.")
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1.")

    predicted = (probabilities >= threshold).astype(int)

    return {
        "accuracy": float(accuracy_score(y_true, predicted)),
        "brier_score": float(brier_score_loss(y_true, probabilities)),
        "log_loss": float(log_loss(y_true, probabilities, labels=[0, 1])),
        "roc_auc": (
            float(roc_auc_score(y_true, probabilities))
            if len(np.unique(y_true)) == 2
            else None
        ),
    }
