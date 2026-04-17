#!/bin/bash

set -euo pipefail

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

cd "$INPUT_DIR"

# Check for MP3 files
MP3_COUNT=$(ls *.mp3 2>/dev/null | wc -l)

if [ "$MP3_COUNT" -eq 0 ]; then
  echo "❌ Error: No MP3 files found in $INPUT_DIR"
  exit 1
fi

echo "🔢 Found $MP3_COUNT MP3 files"

# Run conversion
if make OUTPUT="$OUTPUT"; then
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