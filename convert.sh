#!/bin/bash

set -euo pipefail

command -v ffmpeg >/dev/null 2>&1 || { echo "❌ ffmpeg not installed"; exit 1; }
command -v ffprobe >/dev/null 2>&1 || { echo "❌ ffprobe not installed"; exit 1; }

INPUT_DIR=${1:-.}
OUTPUT=${2:-book.m4b}

echo "📚 Starting conversion..."
echo "📁 Input: $INPUT_DIR"
echo "🎧 Output: $OUTPUT"

# Check directory exists
if [ ! -d "$INPUT_DIR" ]; then
  echo "❌ Error: Directory not found: $INPUT_DIR"
  exit 1
fi


# Check for MP3 files
MP3_COUNT=$(find "$INPUT_DIR" -name "*.mp3" | wc -l)

if [ "$MP3_COUNT" -eq 0 ]; then
  echo "❌ Error: No MP3 files found in $INPUT_DIR"
  exit 1
fi

echo "🔢 Found $MP3_COUNT MP3 files"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run conversion
if make -C "$SCRIPT_DIR" \
     AUDIO_DIR="$INPUT_DIR" \
     OUTPUT="$OUTPUT"; then
  echo "✅ Conversion successful: $OUTPUT"
else
  echo "❌ Conversion failed"
  exit 1
fi

# Validate output
if [ ! -f "$OUTPUT" ]; then
  echo "❌ Error: Output file not created"
  exit 1
fi

echo "🎉 Done!"