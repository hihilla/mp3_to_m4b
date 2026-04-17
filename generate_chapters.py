import os
import subprocess
import sys

files = sorted([f for f in os.listdir() if f.endswith(".mp3")])

if not files:
    print("❌ No MP3 files found")
    sys.exit(1)

start = 0
chapters = []

def clean_title(filename):
    name = filename.split("_", 1)[-1].replace(".mp3", "")
    name = name.replace("_", " ")
    name = name.replace("CHAPTER", "Chapter")

    numbers = {
        "One": "1", "Two": "2", "Three": "3",
        "Four": "4", "Five": "5", "Six": "6",
        "Seven": "7", "Eight": "8", "Nine": "9",
        "Ten": "10"
    }

    for word, digit in numbers.items():
        name = name.replace(f"Chapter {word}", f"Chapter {digit}")

    return name.strip()

for f in files:
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                f
            ],
            capture_output=True, text=True, check=True
        )

        duration = float(result.stdout.strip())

    except Exception as e:
        print(f"❌ Failed to read duration for {f}: {e}")
        sys.exit(1)

    end = start + duration
    chapters.append((start, end, clean_title(f)))
    start = end

try:
    with open("chapters.txt", "w") as f:
        f.write(";FFMETADATA1\n")
        for start, end, title in chapters:
            f.write("[CHAPTER]\n")
            f.write("TIMEBASE=1/1000\n")
            f.write(f"START={int(start*1000)}\n")
            f.write(f"END={int(end*1000)}\n")
            f.write(f"title={title}\n")
except Exception as e:
    print(f"❌ Failed to write chapters.txt: {e}")
    sys.exit(1)