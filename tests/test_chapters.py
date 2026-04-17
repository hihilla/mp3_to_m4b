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

def test_natural_sorting(monkeypatch):
    files = ["1.mp3", "10.mp3", "2.mp3"]

    monkeypatch.setattr("os.listdir", lambda: files)

    from generate_chapters import get_mp3_files
    result = get_mp3_files()

    assert result == ["1.mp3", "2.mp3", "10.mp3"]

def test_clean_title_edge_cases():
    from generate_chapters import clean_title

    assert clean_title("001__CHAPTER__ONE.mp3") == "Chapter 1"
    assert clean_title("weird-file.mp3") == "weird-file"

def test_no_float_drift(monkeypatch):
    from generate_chapters import generate_chapters

    files = ["a.mp3"] * 100

    monkeypatch.setattr(
        "generate_chapters.get_duration",
        lambda f: 0.1
    )

    chapters = generate_chapters(files)

    assert chapters[-1][1] == 10.0

