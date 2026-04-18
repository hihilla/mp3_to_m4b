# MP3 → M4B Audiobook Converter

Convert a folder of chapter-based MP3 files into a single `.m4b` audiobook with chapters.

Made to unite the output from [.epub to Audiobook](https://github.com/p0n1/epub_to_audiobook) tool.

## Features

* Merges multiple MP3 files into one audiobook
* Automatically generates chapter markers
* Cleans up chapter titles
* Optionally embeds cover art (`cover.jpg`)
* Works with iOS audiobook apps like BookPlayer and Bound

## Requirements

* `ffmpeg`
* `ffprobe`
* `python3`

## Usage

```bash
./convert.sh /path/to/mp3s output.m4b
```

Or run inside the folder:

```bash
./convert.sh
```

## Input format

MP3 files should be ordered like:

```
0001_Intro.mp3
0002_Chapter_One.mp3
0003_Chapter_Two.mp3
```

## Optional

Add a `cover.jpg` to embed cover art.

## Output

* `book.m4b` (or custom filename)
* Fully chaptered audiobook
* Compatible with iOS apps like BookPlayer / Bound

## Notes

* Chapters are based on file durations
* Filenames are used to generate chapter titles

## Tests

From your repo root:

```bash
pytest
```

Or with coverage:

```bash
pytest --cov=generate_chapters --cov-report=term-missing
```