def clean_title(filename):
    name = filename.split("_", 1)[-1].replace(".mp3", "")

    # Replace underscores
    name = name.replace("_", " ")

    # Fix common patterns
    name = name.replace("CHAPTER", "Chapter")

    # Convert "Chapter One" → "Chapter 1"
    numbers = {
        "One": "1", "Two": "2", "Three": "3", "Four": "4",
        "Five": "5", "Six": "6", "Seven": "7", "Eight": "8",
        "Nine": "9", "Ten": "10"
    }

    for word, digit in numbers.items():
        name = name.replace(f"Chapter {word}", f"Chapter {digit}")

    return name.strip()