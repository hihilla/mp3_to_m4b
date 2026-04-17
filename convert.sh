#!/bin/bash

set -e

INPUT_DIR=${1:-.}
OUTPUT=${2:-book.m4b}

echo "📚 Converting MP3s in $INPUT_DIR → $OUTPUT"

cd "$INPUT_DIR"

make OUTPUT="$OUTPUT"

echo "✅ Done: $OUTPUT"