# Methodology

## Data preparation
The training pipeline reads the ASSISTments CSV, validates required fields,
converts response correctness to numeric values, removes invalid responses,
and sorts interactions by `order_id`.

## Historical features
The model uses skill ID, opportunity, previous student response count,
previous student accuracy, previous student-skill attempt count, and
previous student-skill accuracy.

Historical accuracy uses additive smoothing:

`(previous correct answers + 1) / (previous attempts + 2)`

## Model
The pipeline uses one-hot encoding for skill IDs, median imputation and
standardisation for numeric features, and logistic regression.
A prior-class DummyClassifier serves as the baseline.

## Evaluation
The training script assigns each student's earliest 80% of interactions
to training and the remaining 20% to testing. This is a chronological
per-student split, not an unseen-student evaluation.

Historical features are constructed before splitting. Although each
response excludes its own correctness from its historical accuracy features,
the pipeline does not reset cumulative history at the train/test boundary.
Test-time information availability should therefore be audited.

## Metrics
- Accuracy: classification accuracy at a 0.5 threshold.
- ROC-AUC: ranking performance across thresholds.
- Brier score: squared error of predicted probabilities.
- Log loss: penalty for inaccurate predicted probabilities.

## Mastery estimation
The default smoothed estimate is:

`(correct answers + 4 * 0.5) / (attempts + 4)`

Bands: below 0.60 is `needs_practice`; 0.60–0.79 is `developing`;
0.80 and above is `strong`.

These bands are heuristics, not validated knowledge measurements.
