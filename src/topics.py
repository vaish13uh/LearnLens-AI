"""Topic taxonomy for the future MEOWNEr placement-prep platform."""

TRACKS = {
    "aptitude": {
        "name": "Quantitative Aptitude",
        "topics": [
            "Percentages",
            "Ratios and Proportions",
            "Profit and Loss",
            "Simple and Compound Interest",
            "Time and Work",
            "Time, Speed and Distance",
            "Averages",
            "Number Systems",
            "Probability",
            "Permutations and Combinations",
            "Data Interpretation",
        ],
    },
    "logical_reasoning": {
        "name": "Logical Reasoning",
        "topics": [
            "Number Series",
            "Letter Series",
            "Coding-Decoding",
            "Syllogisms",
            "Blood Relations",
            "Direction Sense",
            "Seating Arrangements",
            "Puzzles",
            "Analogies",
            "Statement and Conclusion",
        ],
    },
    "coding": {
        "name": "Programming and Coding",
        "topics": [
            "Python Basics",
            "Variables and Data Types",
            "Conditionals",
            "Loops",
            "Strings",
            "Lists and Arrays",
            "Functions",
            "Searching and Sorting",
            "Recursion",
            "Data Structures",
            "Problem Solving",
            "Debugging and Output Prediction",
        ],
    },
}


def get_tracks():
    """Return available learning tracks and their display names."""
    return {
        track_id: track["name"]
        for track_id, track in TRACKS.items()
    }


def get_topics(track_id):
    """Return topics for a track, rejecting unknown track IDs."""
    if track_id not in TRACKS:
        raise ValueError(f"Unknown learning track: {track_id}")
    return list(TRACKS[track_id]["topics"])


def find_topic(topic_name):
    """Find a topic by exact name, ignoring letter case."""
    target = topic_name.strip().casefold()

    for track_id, track in TRACKS.items():
        for topic in track["topics"]:
            if topic.casefold() == target:
                return {
                    "track_id": track_id,
                    "track_name": track["name"],
                    "topic": topic,
                }

    return None
