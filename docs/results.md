# Experimental Results

## Dataset and evaluation

The experiment used the ASSISTments interaction dataset available in the project environment.

- Evaluation: per-student chronological 80/20 split
- Training interactions: 422,038
- Test interactions: 103,496
- Students represented in training: 4,217
- Students represented in testing: 3,776

## Model comparison

| Metric | Majority-class baseline | History-aware logistic regression |
|---|---:|---:|
| Accuracy | 0.6889 | 0.7346 |
| ROC-AUC | 0.5000 | 0.7619 |
| Brier score (lower is better) | 0.2145 | 0.1742 |
| Log loss (lower is better) | 0.6203 | 0.5203 |

## Interpretation

In this run, the history-aware logistic regression achieved higher accuracy and ROC-AUC
and lower Brier score and log loss than the majority-class baseline. These results suggest
that prior student performance, prior skill performance, skill identity, and opportunity
information provide useful predictive signal in this evaluation.

## Evaluation caveats

The split is chronological within each student. Features for later test interactions can
include answers from earlier interactions in the test period. This is appropriate for
sequential prediction when each preceding response is observed before the next prediction,
but it is not an isolated holdout evaluation in which all test predictions are made
without observing any test-period responses.

The previous baseline-results CSV reports a different logistic-regression baseline.
That model is not the majority-class baseline reported in this run; direct comparisons
between those separate reports should not be made without rerunning both models on
the same split and evaluation pipeline.

These metrics describe this particular evaluation and do not establish causal effects
or guarantee performance on other learners or datasets.
