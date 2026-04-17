AUDIO_DIR=.
OUTPUT?=book.m4b

MP3_FILES := $(shell ls $(AUDIO_DIR)/*.mp3 2>/dev/null | sort)

all: check $(OUTPUT)

check:
	@if [ -z "$(MP3_FILES)" ]; then \
		echo "❌ No MP3 files found"; \
		exit 1; \
	fi

files.txt:
	@echo "📄 Generating file list..."
	@rm -f files.txt
	@for f in $(MP3_FILES); do \
		printf "file '%s'\n" "$$f" >> files.txt; \
	done

chapters.txt:
	@echo "🧠 Generating chapters..."
	@python3 generate_chapters.py || (echo "❌ Chapter generation failed" && exit 1)

$(OUTPUT): files.txt chapters.txt
	@echo "🎧 Creating audiobook..."

	@ffmpeg -y -loglevel error -f concat -safe 0 -i files.txt \
	-i chapters.txt \
	-map_metadata 1 \
	-c:a aac -b:a 64k \
	temp.m4b || (echo "❌ ffmpeg merge failed" && exit 1)

	@if [ -f cover.jpg ]; then \
		echo "🖼 Adding cover..."; \
		ffmpeg -y -loglevel error -i temp.m4b -i cover.jpg \
		-map 0 -map 1 \
		-c copy \
		-disposition:v attached_pic \
		$(OUTPUT) || (echo "❌ Cover embedding failed" && exit 1); \
		rm temp.m4b; \
	else \
		echo "ℹ️ No cover.jpg found — skipping cover"; \
		mv temp.m4b $(OUTPUT); \
	fi

	@echo "✅ Created $(OUTPUT)"

clean:
	rm -f files.txt chapters.txt temp.m4b $(OUTPUT)