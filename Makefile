AUDIO_DIR=.
OUTPUT?=book.m4b

MP3_FILES := $(shell ls $(AUDIO_DIR)/*.mp3 2>/dev/null | sort)

all: $(OUTPUT)

files.txt:
	@echo "📄 Generating file list..."
	@for f in $(MP3_FILES); do echo "file '$$f'"; done > files.txt

chapters.txt:
	@echo "🧠 Generating chapters..."
	@python3 generate_chapters.py

$(OUTPUT): files.txt chapters.txt
	@echo "🎧 Creating audiobook..."
	@ffmpeg -loglevel error -f concat -safe 0 -i files.txt \
	-i chapters.txt \
	-map_metadata 1 \
	-c:a aac -b:a 64k \
	temp.m4b

	@if [ -f cover.jpg ]; then \
		echo "🖼 Adding cover..."; \
		ffmpeg -loglevel error -i temp.m4b -i cover.jpg \
		-map 0 -map 1 \
		-c copy \
		-disposition:v attached_pic \
		$(OUTPUT); \
		rm temp.m4b; \
	else \
		mv temp.m4b $(OUTPUT); \
	fi

	@echo "✅ Created $(OUTPUT)"

clean:
	rm -f files.txt chapters.txt temp.m4b $(OUTPUT)