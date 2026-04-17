import pytest
from generate_chapters import clean_title, generate_chapters

def test_clean_title_basic():
    assert clean_title("0009_CHAPTER_ONE.mp3") == "Chapter 1"

def test_clean_title_underscores():
    assert clean_title("0010_Hello_World.mp3") == "Hello World"

def test_clean_title_no_prefix():
    assert clean_title("Intro.mp3") == "Intro"

def test_generate_chapters(monkeypatch):
    files = ["a.mp3", "b.mp3", "c.mp3"]

    durations = {
        "a.mp3": 10.0,
        "b.mp3": 20.0,
        "c.mp3": 30.0
    }

    def mock_duration(file):
        return durations[file]

    monkeypatch.setattr("generate_chapters.get_duration", mock_duration)

    chapters = generate_chapters(files)

    assert len(chapters) == 3

    assert chapters[0] == (0, 10.0, "a")
    assert chapters[1] == (10.0, 30.0, "b")
    assert chapters[2] == (30.0, 60.0, "c")