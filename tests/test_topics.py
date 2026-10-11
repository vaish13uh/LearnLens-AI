import pytest

from src.topics import TRACKS, find_topic, get_topics, get_tracks


def test_three_placement_tracks_exist():
    assert set(get_tracks()) == {
        "aptitude", "logical_reasoning", "coding"
    }


@pytest.mark.parametrize("track_id", list(TRACKS))
def test_each_track_has_topics(track_id):
    topics = get_topics(track_id)
    assert len(topics) > 0
    assert len(topics) == len(set(topics))


def test_unknown_track_is_rejected():
    with pytest.raises(ValueError):
        get_topics("school_mathematics")


def test_topic_lookup_is_case_insensitive():
    result = find_topic("python basics")
    assert result["track_id"] == "coding"
    assert result["topic"] == "Python Basics"


def test_unknown_topic_returns_none():
    assert find_topic("Unknown Topic") is None
