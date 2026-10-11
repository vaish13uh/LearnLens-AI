# Learner Tracking and Mastery

## Research mastery utilities
`src/mastery.py` provides:
- `build_mastery_features(df)`: estimates mastery before and after responses.
- `summarize_mastery(df, user_id)`: ranks attempted skills by estimated mastery.

The default prior strength is 4 and prior mastery is 0.5.

## Placement-preparation tracker
- `src/attempts.py` validates and stores submitted answers.
- `src/progress.py` aggregates attempts, correctness, accuracy, and topic progress.
- `src/report.py` creates reports for a learner.
- `src/topics.py` defines aptitude, logical reasoning, and coding tracks.

Attempts are stored as JSON Lines records with learner and question identifiers,
topic, selected answer, correctness, and UTC timestamp.

The app expects `data/questions.json` and stores attempts in
`data/attempts.jsonl`.

## Important distinction
Research mastery uses ASSISTments student-skill interactions.
The placement-preparation tracker uses the app's own questions and attempts.

## Limitations
Mastery is an accuracy-based proxy. Topic accuracy can be unstable with
few attempts. Local JSONL persistence is not a multi-user database, and
learner IDs do not provide authentication.
