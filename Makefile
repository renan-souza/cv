# Makefile to build PDF and Markdown cv from YAML.
#
# Brandon Amos <http://bamos.github.io> and
# Ellis Michael <http://ellismichael.com>
# Modified by Renan Souza <https://renansouza.org>


TODAY := $(shell date +%Y-%m-%d)

# Assuming that both the cv and github.io directories are in same parent directory `..` so the following line can work
WEBSITE_DIR=$(shell find $(shell pwd)/../*github* | head -n 1)
WEBSITE_PDF=$(WEBSITE_DIR)/data/Renan-Souza-CV.pdf
WEBSITE_PDF_SHORT=$(WEBSITE_DIR)/data/Renan-Souza-CV-short.pdf
WEBSITE_INCLUDES=$(WEBSITE_DIR)/_includes


TEMPLATES=$(shell find templates -type f)

BUILD_DIR=build
TEX=$(BUILD_DIR)/cv.tex
PDF=$(BUILD_DIR)/cv.pdf
PDF_SHORT=$(BUILD_DIR)/cv-short.pdf
MD=$(BUILD_DIR)/cv.md



ifneq ("$(wildcard cv.hidden.yaml)","")
	YAML_FILES = cv.yaml cv.hidden.yaml
else
	YAML_FILES = cv.yaml
endif

.PHONY: all public viewpdf stage web push clean

all: $(PDF) $(MD) web

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

public: $(BUILD_DIR) $(TEMPLATES) $(YAML_FILES) generate.py
	./generate.py $(YAML_FILES)

$(TEX) $(MD): $(TEMPLATES) $(YAML_FILES) generate.py
	./generate.py $(YAML_FILES)
	./generate.py $(YAML_FILES) -s
	./generate.py $(YAML_FILES) -t publications -m
	./generate.py $(YAML_FILES) -t events -m


$(PDF): $(TEX) publications/*.bib
	# TODO: Hack for biber on OSX.
	rm -rf /var/folders/8p/lzk2wkqj47g5wf8g8lfpsk4w0000gn/T/par-62616d6f73

	latexmk -pdf -cd- -jobname=$(BUILD_DIR)/cv $(BUILD_DIR)/cv
	latexmk -c -cd $(BUILD_DIR)/cv


	latexmk -pdf -cd- -jobname=$(BUILD_DIR)/cv-short $(BUILD_DIR)/cv-short
	latexmk -c -cd $(BUILD_DIR)/cv-short
	rm -f $(BUILD_DIR)/cv-short*md

	open  $(BUILD_DIR)/cv.pdf
	open  $(BUILD_DIR)/cv-short.pdf

viewpdf: $(PDF)
	gnome-open $(PDF)

stage: $(PDF) $(MD)
	rm $(WEBSITE_DIR)/data/*pdf
	cp $(PDF) $(WEBSITE_PDF)
	cp $(PDF_SHORT) $(WEBSITE_PDF_SHORT)
	cp $(BUILD_DIR)/*.md $(WEBSITE_INCLUDES)

web: stage
	./generate.py $(YAML_FILES) -o $(WEBSITE_DIR)/_config.yml
	docker run -v $(WEBSITE_DIR):/website -p 4444:4444 -it website

web_build: stage
	./generate.py $(YAML_FILES) -o $(WEBSITE_DIR)/_config.yml
	cd $(WEBSITE_DIR) && docker build -t website .
	docker run -p 4444:4444 -it website

commit:
	git -C $(WEBSITE_DIR) add $(WEBSITE_INCLUDES)/*md $(WEBSITE_DATE) $(WEBSITE_DIR)/data $(WEBSITE_DIR)/images $(WEBSITE_DIR)/_config.yml
	git -C $(WEBSITE_DIR) status
	git -C $(WEBSITE_DIR) commit -m "Update from Makefile in cv build repo."
	git -C $(WEBSITE_DIR) push

clean:
	rm -rf $(BUILD_DIR)/*cv*
	rm -rf $(BUILD_DIR)/*md
	rm -rf $(WEBSITE_INCLUDES)/*md
