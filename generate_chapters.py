import os
import subprocess
import sys
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]


def get_mp3_files(audio_dir="."):
    files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith(".mp3")]
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
    import re

    # Extract name after first underscore (if exists)
    parts = filename.split("_", 1)
    name = parts[1] if len(parts) > 1 else parts[0]

    # Remove extension
    name = name.replace(".mp3", "")

    # Replace underscores with spaces
    name = name.replace("_", " ")

    # Normalize whitespace
    name = re.sub(r"\s+", " ", name).strip()

    # Normalize CHAPTER casing
    name = re.sub(r"\bCHAPTER\b", "Chapter", name, flags=re.IGNORECASE)

    # Convert written numbers to digits
    numbers = {
        "One": "1", "Two": "2", "Three": "3",
        "Four": "4", "Five": "5", "Six": "6",
        "Seven": "7", "Eight": "8", "Nine": "9",
        "Ten": "10"
    }

    for word, digit in numbers.items():
        name = re.sub(rf"\b{word}\b", digit, name, flags=re.IGNORECASE)

    return name


def generate_chapters(files):
    start = 0
    chapters = []

    total = len(files)

    for i, f in enumerate(files, 1):
        duration = get_duration(f)
        end = round(start + duration, 3)
        chapters.append((start, end, clean_title(f)))
        start = end

        # Progress update (overwrite same line)
        print(f"\r🧠 Processing chapters: {i}/{total}", end="", flush=True)

    print()  # newline after loop

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
    audio_dir = os.environ.get("AUDIO_DIR", ".")
    files = get_mp3_files(audio_dir)

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