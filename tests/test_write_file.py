import os
from generate_chapters import write_chapters_file

def test_write_chapters_file(tmp_path):
    output = tmp_path / "chapters.txt"

    chapters = [
        (0, 10, "Intro"),
        (10, 20, "Chapter 1")
    ]

    write_chapters_file(chapters, output)

    content = output.read_text()

    assert ";FFMETADATA1" in content
    assert "title=Intro" in content
    assert "title=Chapter 1" in content
    assert "START=0" in content
    assert "END=10000" in content