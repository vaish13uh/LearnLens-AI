# LearnLens-AI — Project Overview

## Purpose
LearnLens-AI explores machine learning for predicting student responses,
estimating skill mastery, and identifying areas for additional practice.

## Dataset
The initial experiments use the ASSISTments Skill Builder dataset.
The README records 525,534 interactions from 4,217 students.
The dataset is not included in this repository.

## Main components
- `src/features.py`: historical response feature engineering.
- `src/train.py`: model training and evaluation.
- `src/evaluation.py`: binary prediction metrics.
- `src/mastery.py`: smoothed skill mastery estimates.
- `src/attempts.py`, `src/progress.py`, `src/report.py`: learner tracking.
- `app.py`: Streamlit placement-preparation interface.

## Scope
The ASSISTments research experiments and the MEOWNEr placement-preparation
app are separate workflows. The app uses its own question bank and attempts.

## Limitation
Accuracy-based mastery estimates are proxies, not validated measurements
of a student's underlying knowledge.
