
"""Record and persist MEOWNEr learner question attempts."""

import json
from datetime import datetime, timezone
from pathlib import Path


def create_attempt(learner_id, question, selected_answer):
    """Create a validated attempt record from a bank question."""
    if not isinstance(learner_id, str) or not learner_id.strip():
        raise ValueError("learner_id must be a non-empty string")

    required = {"id", "track_id", "topic", "options", "answer"}
    missing = required - set(question)
    if missing:
        raise ValueError(f"Question is missing fields: {sorted(missing)}")

    if selected_answer not in question["options"]:
        raise ValueError("selected_answer must be one of the question options")

    return {
        "learner_id": learner_id.strip(),
        "question_id": question["id"],
        "track_id": question["track_id"],
        "topic": question["topic"],
        "selected_answer": selected_answer,
        "correct": int(selected_answer == question["answer"]),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def append_attempt(attempt, path="data/attempts.jsonl"):
    """Append one attempt as a JSON line and return its saved record."""
    required = {
        "learner_id", "question_id", "track_id", "topic",
        "selected_answer", "correct", "timestamp"
    }
    missing = required - set(attempt)
    if missing:
        raise ValueError(f"Attempt is missing fields: {sorted(missing)}")

    if attempt["correct"] not in (0, 1):
        raise ValueError("correct must be 0 or 1")

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("a", encoding="utf-8") as file:
        file.write(json.dumps(attempt, ensure_ascii=False) + "\n")

    return attempt


def load_attempts(path="data/attempts.jsonl"):
    """Load saved attempts, returning an empty list if none exist."""
    source = Path(path)
    if not source.exists():
        return []

    with source.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]
