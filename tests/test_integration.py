import os
import pytest
from generate_chapters import main

def test_main_success(tmp_path, monkeypatch):
    os.chdir(tmp_path)

    # Create fake mp3 files
    for name in ["001_CHAPTER_ONE.mp3", "002_CHAPTER_TWO.mp3"]:
        open(name, "w").close()

    def mock_run(*args, **kwargs):
        class Result:
            stdout = "10.0\n"
        return Result()

    monkeypatch.setattr("subprocess.run", mock_run)

    main()

    assert os.path.exists("chapters.txt")

    content = open("chapters.txt").read()
    assert "[CHAPTER]" in content
    assert "title=" in content

def test_main_no_files(tmp_path, monkeypatch):
    os.chdir(tmp_path)

    with pytest.raises(SystemExit):
        main()

def test_ffprobe_failure(tmp_path, monkeypatch):
    os.chdir(tmp_path)

    open("test.mp3", "w").close()

    def mock_run(*args, **kwargs):
        raise Exception("ffprobe failed")

    monkeypatch.setattr("subprocess.run", mock_run)

    with pytest.raises(SystemExit):
        main()