import sys
import re
import subprocess
import glob
import os

def get_total_duration():
    total = 0
    audio_dir = os.environ.get("AUDIO_DIR", ".")
    for file in glob.glob(f"{audio_dir}/*.mp3"):
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                file
            ],
            capture_output=True, text=True
        )
        try:
            total += float(result.stdout.strip())
        except:
            pass
    return total

total_duration = get_total_duration()

for line in sys.stdin:
    match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)
    if match and total_duration:
        h, m, s = match.groups()
        current = int(h)*3600 + int(m)*60 + float(s)

        percent = (current / total_duration) * 100
        print(f"\r🎧 Encoding: {percent:5.1f}%", end="", flush=True)

print("\n✅ Done encoding")