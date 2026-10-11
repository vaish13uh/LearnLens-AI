"""Load saved MEOWNEr attempts and generate learner progress reports."""

from .attempts import load_attempts
from .progress import build_progress


def get_learner_report(
    learner_id,
    attempts_path="data/attempts.jsonl",
    min_attempts=1,
    top_n=3,
):
    """Return a learner's progress summary from saved attempt history."""
    attempts = load_attempts(attempts_path)

    return build_progress(
        attempts=attempts,
        learner_id=learner_id,
        min_attempts=min_attempts,
        top_n=top_n,
    )
