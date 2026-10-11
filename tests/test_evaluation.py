import pytest

from src.evaluation import evaluate_binary_predictions


def test_perfect_predictions_have_perfect_auc_and_accuracy():
    result = evaluate_binary_predictions(
        [0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9]
    )
    assert result["accuracy"] == 1.0
    assert result["roc_auc"] == 1.0
    assert result["brier_score"] < 0.05


def test_auc_is_none_when_only_one_class_is_present():
    result = evaluate_binary_predictions([1, 1, 1], [0.7, 0.8, 0.9])
    assert result["roc_auc"] is None


def test_invalid_probabilities_are_rejected():
    with pytest.raises(ValueError):
        evaluate_binary_predictions([0, 1], [0.2, 1.4])


def test_mismatched_lengths_are_rejected():
    with pytest.raises(ValueError):
        evaluate_binary_predictions([0, 1], [0.3])
