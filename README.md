
# About

Here you'll find the source code to automatically generate my CV
and [Webpage](https://renansouza.org)
from YAML and BibTeX input.

This repo is the main one, but it is intended to work together with the [website repo](https://github.com/renan-souza/renan-souza.github.io).
So make sure you clone it as well and put it in the same parent directory of this repo.
That is, the directory structure looks like this:

- `parent-dir`
    - `cv`
    - `renan-souza.github.io`

The script [generate.py](generate.py) reads from [cv.yaml](cv.yaml) and
[publications](publications) and outputs LaTeX and Markdown
by using Jinja templates.

## Requirements

- #### Python 3

- #### Docker
- #### Latexmk
    See https://latextools.readthedocs.io/en/latest/install
# Installation

### [Website repo](https://github.com/renan-souza/renan-souza.github.io):

Ruby is used to generate the website and we use a Docker image to use the right Ruby (and dependencies) versions that work for this website.

- Build the Docker image for the website:
```bash
cd renan-souza.github.io
docker build -t website .
```


### [This repo](#):

 ```shell
 cd cv
 # Assuming you use conda
 conda create -n cv
 conda activate cv
 pip install -r requirements.txt
 ```

# Building and Running

The [Makefile](Makefile) contains the instructions to build both the pdf and the webpage. Take a look at it.

On Mac or Linux, `make` command will call [generate.py](generate.py) to
build the LaTeX documents with `latexmk` and `biber`.
`make` will then generate the `_config.yml` of the Website repo and call the
target `web` to start the server using Docker (`docker run -p 4444:4444 -it website`) so that the server will start at [localhost:4444](http://localhost:4444) (port is specified in the `_config.yml`).


# What to modify
Change the content in `cv.yaml`.
You should also look through the template files to make sure there isn't any
special-case code that needs to be modified.
The `Makefile` can also start a Jekyll server and push the
new documents to another repository.


## Warnings
1. Strings in `cv.yaml` should be LaTeX (though, the actual LaTeX formatting
   should be in the left in the templates as much as possible).
2. If you do include any new LaTeX commands, make sure that one of the
   `REPLACEMENTS` in `generate.py` converts them properly.
3. The LaTeX templates use modified Jinja delimiters to avoid overlaps with
   normal LaTeX. See `generate.py` for details.

## Publications
All publications are stored as BibTeX in [publications](publications).
The entries can be obtained from Google Scholar.


BibTeX is built for integration with LaTeX, but producing
Markdown is not traditionally done from BibTeX files.
This repository uses [BibtexParser][bibtexparser] to load the
bibliography into a map.
The data is manually formatted to mimic the LaTeX
IEEE bibliography style.

[bibtexparser]: https://bibtexparser.readthedocs.org/en/latest/index.html

# Useful info and docs

The variables and code in the files under [templates](templates)
use [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/)
whose syntax, for the variables, is similar to python.

The variables and code in the files under in the [website's repo](https://github.com/renan-souza/renan-souza.github.io)
use [Jekyll](https://jekyllrb.com/). This [doc](https://shopify.github.io/liquid/filters/) is handy if you need to
manipulate variables in the Jekyll's template.


# Licensing

This repo is a fork from [Brandon Amos](http://bamos.github.io)'s [repo](https://github.com/bamos/cv) for building CV and personal webpage.
Based on Brandon's code, I have made several changes here to customize for my own template.

This work is distributed under the [MIT license](LICENSE.mit)
with portions copyright [Brandon Amos](licenses/LICENSE-emichael.mit) and [Ellis Michael](licenses/LICENSE-emichael.mit).
This work includes major refactorings done in and after the commit [685a7a7](https://github.com/renan-souza/cv/commit/685a7a73515c06ce3dbe3da8ccfdda0d0bcf19be)
which is compliant to the website repo's commit [8cd893a](https://github.com/renan-souza/renan-souza.github.io/commit/8cd893a5149b244f9f8e13a82f7d7c4660ed4fca).
