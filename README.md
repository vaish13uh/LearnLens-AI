# LearnLens-AI 📚

**An adaptive learning analytics project that uses machine learning and learning-history features to estimate student performance and track topic mastery.**

LearnLens-AI explores how student interaction data can be used to understand learning progress, estimate the likelihood of correct responses, and identify topics that may need additional practice.

## ✨ Features

- **History-aware prediction:** Uses previous student interactions to construct learning-history features.
- **Student performance analysis:** Evaluates predictions using accuracy, ROC-AUC, Brier score, and log loss.
- **Topic mastery tracking:** Organizes learning progress by topic and learning track.
- **Attempt tracking:** Records practice attempts and correctness for individual learners.
- **Progress reports:** Summarizes attempts, accuracy, and topic-level performance.
- **Interactive dashboard:** Provides an interface for exploring learner progress and practice activity.

## 🧠 Machine Learning Approach

The project uses a logistic regression model with features derived from prior student interactions.

The feature engineering pipeline is designed to use information available before each response, helping avoid using the current response to construct its own prediction features.

### Dataset and Evaluation

| Metric | Majority-class baseline | History-aware model |
|---|---:|---:|
| Accuracy | 68.89% | 73.46% |
| ROC-AUC | 0.5000 | 0.7619 |
| Brier score | 0.2145 | 0.1742 |
| Log loss | 0.6203 | 0.5203 |

The history-aware model outperformed the majority-class baseline across the reported metrics. These results are experimental and do not establish improved real-world learning outcomes.

**Evaluation note:** The split preserves chronological order within each student's interaction history. Students may appear in both training and test periods, so this evaluation does not measure generalization to entirely unseen students.

See [`docs/results.md`](docs/results.md) for experiment details and limitations.

## 🛠️ Tech Stack

- Python
- pandas and NumPy
- scikit-learn
- Streamlit
- pytest
- JSON and JSONL for learner activity storage

## 📊 Reports and Reproducibility

Experiment results and supporting documentation are available in the `docs/` and `reports/` directories.

For reproducible evaluation, use the documented data split, feature-generation process, and model configuration. Performance metrics may vary if the dataset, preprocessing, or evaluation procedure changes.

## 🔮 Future Improvements

- Improve the interactive learning experience and dashboard design.
- Add more robust learner-specific mastery estimates.
- Compare against stronger baseline models.
- Evaluate performance on unseen students and alternative chronological splits.
- Add targeted revision recommendations based on learning history.
- Improve data persistence and deployment support.


*LearnLens-AI is an experimental machine-learning and learning-analytics project. Predictions and mastery estimates are intended to support exploration and practice, not replace formal assessments.*
