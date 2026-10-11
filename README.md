# LearnLens AI

Adaptive learning intelligence using machine learning and
knowledge tracing.

## Project goals

- Analyse student-question response histories.
- Estimate knowledge mastery by concept.
- Predict future question correctness.
- Evaluate models on held-out student data.
- Explore personalised practice recommendations.

## Current status

Initial development: evaluation utilities and tests.

Model performance will be reported only after experiments on
a documented dataset with an appropriate evaluation split.

## Planned stack

Python, pandas, NumPy, scikit-learn, pytest, FastAPI,
Streamlit and PostgreSQL.

## Getting started

Install dependencies:

```bash
pip install -r requirements.txt
pytest -q
```

## First experiments

Dataset: ASSISTments Skill Builder (525,534 interactions, 4,217 students).

| Experiment | Accuracy | ROC-AUC | Brier score | Log loss |
|---|---:|---:|---:|---:|
| Majority-class baseline, unseen students | 68.57% | 0.5000 | 0.2156 | 0.6226 |
| Logistic regression, unseen students | 69.07% | 0.6568 | 0.2010 | 0.5856 |
| History-aware logistic regression, chronological split | 73.45% | 0.7619 | 0.1742 | 0.5203 |

The history-aware experiment uses prior student and student-skill performance
features. The reusable training pipeline has now been run successfully on the full
dataset, and its fresh metrics match the recorded results to rounding. Its test split differs from the unseen-student experiment, so these
scores are not a direct apples-to-apples comparison. The observed results are
recorded in `reports/experiment_results.json`; rerun the training script to
reproduce metrics from the local dataset.

## Run locally

Install dependencies with `pip install -r requirements.txt`, then run:

`python -m src.train --data /path/to/skill_builder_data.csv`

The dataset is not included in this repository.
