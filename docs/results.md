# Experiment Results

## Results recorded in README.md

| Experiment | Accuracy | ROC-AUC | Brier score | Log loss |
|---|---:|---:|---:|---:|
| Majority baseline, unseen students | 68.57% | 0.5000 | 0.2156 | 0.6226 |
| Logistic regression, unseen students | 69.07% | 0.6568 | 0.2010 | 0.5856 |
| History-aware logistic regression, chronological split | 73.45% | 0.7619 | 0.1742 | 0.5203 |

These values are transcribed from the README; they are not newly
reproduced by this document.

## Comparability
The unseen-student and chronological experiments use different splits.
Their scores should not be treated as a direct apples-to-apples comparison.

## Reproduction
Obtain the dataset separately, install `requirements.txt`, then run:

```bash
python -m src.train --data /path/to/skill_builder_data.csv
```

The script writes fresh results to `reports/history_results.json` by default.

## Further work
- Reproduce the unseen-student experiments with documented scripts.
- Audit feature availability at prediction time.
- Test for leakage across train/test boundaries.
- Record dataset provenance and split sizes.
- Compare models using consistent evaluation splits.
