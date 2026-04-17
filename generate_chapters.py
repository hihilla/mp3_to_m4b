import os
import subprocess
import sys
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]


def get_mp3_files():
    files = [f for f in os.listdir() if f.endswith(".mp3")]
    return sorted(files, key=natural_sort_key)


def get_duration(file):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file
        ],
        capture_output=True, text=True, check=True
    )
    return float(result.stdout.strip())


def clean_title(filename):
    name = filename.split("_", 1)[-1].replace(".mp3", "")
    name = name.replace("_", " ")
    name = re.sub(r"\bCHAPTER\b", "Chapter", name)

    numbers = {
        "One": "1", "Two": "2", "Three": "3",
        "Four": "4", "Five": "5", "Six": "6",
        "Seven": "7", "Eight": "8", "Nine": "9",
        "Ten": "10"
    }

    for word, digit in numbers.items():
        name = name.replace(f"Chapter {word}", f"Chapter {digit}")

    return name.strip()


def generate_chapters(files):
    start = 0
    chapters = []

    for f in files:
        duration = get_duration(f)
        end = round(start + duration, 3)
        chapters.append((start, end, clean_title(f)))
        start = end

    return chapters

def write_chapters_file(chapters, output="chapters.txt"):
    with open(output, "w") as f:
        f.write(";FFMETADATA1\n")
        for start, end, title in chapters:
            f.write("[CHAPTER]\n")
            f.write("TIMEBASE=1/1000\n")
            f.write(f"START={int(start*1000)}\n")
            f.write(f"END={int(end*1000)}\n")
            f.write(f"title={title}\n")

def main():
    files = get_mp3_files()

    if not files:
        print("❌ No MP3 files found")
        sys.exit(1)

    try:
        chapters = generate_chapters(files)
        write_chapters_file(chapters)
    except Exception as e:
        print(f"❌ Error while generating chapters: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()