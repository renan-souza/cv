#!/usr/bin/env python3

"""Generates LaTeX, markdown, and plaintext copies of my cv."""

__author__ = [
    'Brandon Amos <http://bamos.github.io>',
    'Ellis Michael <http://ellismichael.com>',
]
"""
Adapted by Renan Souza <http://renan-souza.github.io>
"""


import argparse
import os
import re
import yaml
import sys
import bibtexparser.customization as bc
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

import copy
from datetime import date
from jinja2 import Environment, FileSystemLoader
import codecs
import functools

open = functools.partial(codecs.open, encoding='utf-8')


def get_pub_md(context, config):
    """Given the bibtexparser's representation and configuration,
    return a markdown string similar to BibTeX's output
    of a markdown file.
    See `publications.bib` for an example BibTeX file.

    ### Conference Proceedings
    [C1] Names. "Paper A," in <em>IEEE</em>, 2015.<br><br>
    [C2] Names. "Paper B," in <em>IEEE</em>, 2015.<br><br>

    ### Journal Articles
    [J1] Names. "Paper C," in <em>IEEE</em>, 2015.<br><br>
"""

    def _get_author_str(immut_author_list):
        authors = copy.copy(immut_author_list)
        if len(authors) > 1:
            authors[-1] = "and " + authors[-1]
        sep = ", " if len(authors) > 2 else " "
        authors = sep.join(authors)

        # Hacky fix for special characters.
        authors = authors.replace('\\"o', '&ouml;')

        return authors

    # [First Initial]. [Last Name]
    def _format_author_list(immut_author_list):
        formatted_authors = []

        for author in immut_author_list:
            new_auth = author.split(", ")
            try:
                new_auth = new_auth[1][0] + ". " + new_auth[0]
            except:
                new_auth = new_auth[0]

            if config['name'] in new_auth:
                new_auth = "<strong>" + new_auth + "</strong>"
            formatted_authors.append(new_auth)
        return formatted_authors


    def _get_pub_str(pub, prefix, gidx, includeImage):
        author_str = _get_author_str(pub['author'])
        # prefix = category['prefix']
        title = pub['title']
        # if title[-1] not in ("?", ".", "!"):
        #    title += ","
        # title = '"{}"'.format(title)
        # if 'link' in pub:
        #     title = "<a href=\'{}\'>{}</a>".format(
        #         pub['link'], title)
        title = title.replace("\n", " ")

        venue = ""
        if 'journal' in pub:
            venue = f"{pub['journal']}"
        elif 'booktitle' in pub:
            venue = f"{pub['booktitle']}"

        if 'year' in pub:
            year = f"{pub['year']}"
        else:
            #TODO try to get from the pub['date']
            print("FATAL ERROR: Can't generate for the following bibentry because it does not have an year. "
                  "Make sure it has an year\n" + str(pub['ID']))
            sys.exit(-1)



        imgStr = '<img src="images/publications/{}.png" style="border:0"/>'.format(pub['ID'])
        links = ['[{}{}]'.format(prefix, gidx)]
        abstract = ''
        if 'abstract' in pub:
            links.append("""
[<a href='javascript: none'
    onclick=\'$(\"#abs_{}{}\").toggle()\'>abstract</a>]""".format(pub['ID'], prefix))
            abstract = "<strong>Abstract. </strong>"+context.make_replacements(pub['abstract'])
            if 'keyword' in pub:
                abstract += "<br/><strong>Keywords: </strong> " + pub['keyword']

        if 'doi' in pub:
            links.append(
                "[<a href=\'https://doi.org/{}\' target='_blank'>doi</a>] ".format(pub['doi']))
            imgStr = "<a href=\'https://doi.org/{}\' target='_blank'>{}</a> ".format(pub['doi'], imgStr)

        if 'link' in pub or 'url' in pub:
            if 'link' in pub:
                k = 'link'
            else:
                k = 'url'

            links.append(
                "[<a href=\'{}\' target='_blank'>online</a>] ".format(pub[k]))

        if 'pdf' in pub:
            links.append(
                "[<a href=\'{}\' target='_blank'>pdf</a>] ".format(pub['pdf']))

        if 'codeurl' in pub:
            links.append(
                "[<a href=\'{}\' target='_blank'>code</a>] ".format(pub['codeurl']))

        links.append("""
            [<a href='javascript: none'
            onclick=\'$(\"#bib_{}{}\").toggle()\'>bibtex</a>]""".format(pub['ID'], prefix))


        links = ' '.join(links)

        if abstract:
            abstract = '''
<div id="abs_{}{}" style="text-align: justify; display: none" markdown="1">
{}
</div>
'''.format(pub['ID'], prefix, abstract)

        bib = pub['BIB_ENTRY'].replace("{", "&#123;").replace("}", "&#125;").replace("\n","<br/>").replace("\t","&nbsp;&nbsp;")

        bib = '''
<div id="bib_{}{}" style="display: none; background-color: #eee; font-family:Courier; font-size: 0.8em; text-align: justify; border-color: gray; border: 1px solid lightgray;">
{}
</div>
'''.format(pub['ID'], prefix, bib)

        if '_note' in pub:
            note_str = '<strong>{}</strong><br>'.format(pub['_note'])
        else:
            note_str = ''

        if venue:
            yearVenue = f"<br><i>{venue}</i>, {year}."
        else:
            yearVenue = f", {year}."

        div_content = f"""
            <strong>{title}</strong><br>
            {author_str}{yearVenue}<br>
            {note_str}
            {links}<br>
            {abstract}
            {bib}
        """




        if includeImage:
            return f"""
<tr>
<td class="col-md-3 hidden-xs hidden-sm" style="vertical-align: middle;">{imgStr}</td>
<td style="vertical-align: middle; text-align: justify;">
    {div_content}
</td>
</tr>
"""

        else:
            return f"""
<tr>
<td style="vertical-align: middle; text-align: justify;">
    {div_content}
</td>
</tr>
"""

    def load_and_replace(bibtex_file):
        with open(os.path.join('publications', bibtex_file), 'r', encoding="utf-8") as f:
            fdata = f.read()
            pdict = BibTexParser(fdata).get_entry_dict()
            plist = BibTexParser(fdata, bc.author).get_entry_list()
        by_year = {}

        for pub in plist:
            pubd = pdict[pub['ID']]
            db = BibDatabase()
            db.entries = [pubd]
            writer = BibTexWriter()
            writer.indent = '\t'
            bibentry = writer.write(db)
            pub['BIB_ENTRY'] = bibentry
            for field in pub:
                if field == 'BIB_ENTRY':
                    continue
                pub[field] = context.make_replacements(pub[field])
            pub['author'] = _format_author_list(pub['author'])
            y = int(pub['year']) if 'year' in pub else 1970
            if y not in by_year:
                by_year[y] = []
            by_year[y].append(pub)

        ret = []
        for year, pubs in sorted(by_year.items(), reverse=True):
            for pub in pubs:
                ret.append(pub)

        return ret

    if 'categories' in config:
        contents = []
        for category in config['categories']:
            type_content = {}
            type_content['title'] = category['heading']

            pubs = load_and_replace(category['file'])

            details = ""
            # sep = "<br><br>\n"
            sep = "\n"
            for i, pub in enumerate(pubs):
                details += _get_pub_str(pub, category['prefix'],
                                        i + 1, includeImage=False) + sep
            type_content['details'] = details
            type_content['file'] = category['file']
            contents.append(type_content)
    else:
        contents = {}
        pubs = load_and_replace(config['file'])
        details = ""
        sep = "\n"
        for i, pub in enumerate(pubs):
            details += _get_pub_str(pub, '', i + 1, includeImage=True) + sep
        contents['details'] = details
        contents['file'] = config['file']

    return contents


class RenderContext(object):
    BUILD_DIR = 'build'
    TEMPLATES_DIR = 'templates'
    SECTIONS_DIR = 'sections'
    DEFAULT_SECTION = 'items'
    BASE_FILE_NAME = 'cv'

    def __init__(self, context_name, file_ending, jinja_options, replacements, file_name=None, short=False):
        self._file_ending = file_ending
        self._replacements = replacements
        self.file_name = self.BASE_FILE_NAME if not file_name else file_name
        if short:
            self.file_name += "-short"
        context_templates_dir = os.path.join(self.TEMPLATES_DIR, context_name)

        self._output_file = os.path.join(
            self.BUILD_DIR, self.file_name + self._file_ending)
        self._base_template = self.BASE_FILE_NAME + self._file_ending

        self._context_type_name = context_name + 'type'

        self._jinja_options = jinja_options.copy()
        self._jinja_options['loader'] = FileSystemLoader(
            searchpath=context_templates_dir)
        self._jinja_env = Environment(**self._jinja_options)

    def make_replacements(self, yaml_data):
        # Make a copy of the yaml_data so that this function is idempotent
        yaml_data = copy.copy(yaml_data)

        if isinstance(yaml_data, str):
            for o, r in self._replacements:
                yaml_data = re.sub(o, r, yaml_data)

        elif isinstance(yaml_data, dict):
            for k, v in yaml_data.items():
                yaml_data[k] = self.make_replacements(v)

        elif isinstance(yaml_data, list):
            for idx, item in enumerate(yaml_data):
                yaml_data[idx] = self.make_replacements(item)

        return yaml_data

    def _render_template(self, template_name, yaml_data):
        template_name = template_name.replace(os.path.sep, '/')  # Fixes #11.
        return self._jinja_env.get_template(template_name).render(yaml_data)

    @staticmethod
    def _make_double_list(items):
        groups = []
        items_temp = list(items)
        while len(items_temp):
            group = {}
            group['first'] = items_temp.pop(0)
            if len(items_temp):
                group['second'] = items_temp.pop(0)
            groups.append(group)
        return groups

    def render_resume(self, yaml_data, specified_tag=None, short=False):
        # Make the replacements first on the yaml_data
        yaml_data = self.make_replacements(yaml_data)
        yaml_data['today'] = date.today().strftime("%Y-%m-%d")
        section_data = {
            'src': yaml_data['personal']['src'],
            'today': yaml_data['today'],
            'personal': yaml_data['personal']
        }

        if specified_tag:
            for order_item in yaml_data['order']:
                if order_item['tag'] == specified_tag:
                    name = order_item['title']

            section_data['name'] = name
            section_content = yaml_data[specified_tag]

            if 'publications' in specified_tag and self._file_ending == ".md":
                section_data['items'] = get_pub_md(self, section_content)
            else:
                section_data['items'] = section_content

            section_template_name = os.path.join(self.SECTIONS_DIR, specified_tag + self._file_ending)

            rendered_section = self._render_template(
                section_template_name, section_data)
            body = rendered_section.rstrip() + '\n\n\n'

            yaml_data['body'] = body

            return self._render_template(
                self._base_template, yaml_data).rstrip() + '\n'

        else:

            body = ''
            for item in yaml_data['order']:
                if short:
                    display_short = False
                    if 'display-short' in item:
                        display_short = True if "true" in str(item['display-short']).lower() else False

                    if not display_short:
                        continue

                section_tag = item['tag']
                section_title = item['title']
                section_data['name'] = section_title
                display_web = True if "true" in str(item['display-web']).lower() else False
                display_pdf = item['display-pdf']
                print("  + Processing section: {}".format(section_tag))
                if self._file_ending == ".tex" and not display_pdf:
                    print("We are not generating pdf for " + section_tag)
                    continue
                elif self._file_ending == ".md" and not display_web:
                    print("We are not generating web for " + section_tag)
                    continue

                section_content = yaml_data[section_tag]
                if 'experience' in section_tag:
                    print()
                if 'publications' in section_tag and self._file_ending == ".md":
                    section_data['items'] = get_pub_md(self, section_content)
                else:
                    section_data['items'] = section_content
                    section_data['short'] = short
                section_template_name = os.path.join(
                    self.SECTIONS_DIR, section_tag + self._file_ending)

                rendered_section = self._render_template(
                    section_template_name, section_data)
                body += rendered_section.rstrip() + '\n\n\n'

            yaml_data['body'] = body
            yaml_data['today'] = date.today().strftime("%B %d, %Y")
            return self._render_template(
                self._base_template, yaml_data).rstrip() + '\n'

    def write_to_outfile(self, output_data):
        with open(self._output_file, 'w', encoding='utf-8') as out:
            #output_data = output_data.encode('utf-8')
            out.write(output_data)




def process_resume(context, yaml_data, preview, specified_tag=None, short=False):
    rendered_resume = context.render_resume(yaml_data, specified_tag, short=short)
    if preview:
        print(rendered_resume)
    else:
        context.write_to_outfile(rendered_resume)


def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Generates HTML, LaTeX, and Markdown resumes from data in YAML files.')
    parser.add_argument('yamls', metavar='YAML_FILE', nargs='+',
                        help='The YAML files that contain the resume/cv'
                        'details, in order of increasing precedence')
    parser.add_argument('-p', '--preview', action='store_true',
                        help='prints generated content to stdout instead of writing to file')
    parser.add_argument('-t', '--tag', help='Specify the tag to be generated in a separate file', default=None)
    parser.add_argument('-s', '--short', help='Indicate that the short version will be generated', action='store_true')

    parser.add_argument('-o', '--output-yaml', help='Copy some data from the input yaml to an output yaml')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--latex', action='store_true',
                       help='only generate LaTeX resume/cv')
    group.add_argument('-m', '--markdown', action='store_true',
                       help='only generate Markdown resume/cv')


    args = parser.parse_args()
    specified_tag = args.tag
    yaml_data = {}
    for yaml_file in args.yamls:
        with open(yaml_file, encoding="utf-8") as f:
            yaml_data.update(yaml.load(f))


    if args.output_yaml:
        personal_data = yaml_data['personal']
        out_data = yaml.load(open(args.output_yaml))
        out_data['today'] = date.today().strftime("%Y-%m-%d")
        out_data['personal'] = personal_data
        yaml.dump(out_data, open(args.output_yaml, 'w'))
        print("Copied yaml data to " + args.output_yaml)
        sys.exit(0)

    short = args.short
    LATEX_CONTEXT = RenderContext(
        'latex',
        '.tex',
        dict(
            block_start_string='~<',
            block_end_string='>~',
            variable_start_string='<<',
            variable_end_string='>>',
            comment_start_string='<#',
            comment_end_string='#>',
            trim_blocks=True,
            lstrip_blocks=True
        ),
        [],
        specified_tag,
        short
    )

    MARKDOWN_CONTEXT = RenderContext(
        'markdown',
        '.md',
        dict(
            trim_blocks=True,
            lstrip_blocks=True
        ),
        [
            (r'\\\\\[[^\]]*]', '\n'),  # newlines
            (r'\\ ', ' '),  # spaces
            (r'\\&', '&'),  # unescape &
            (r'\\\$', '\$'),  # unescape $
            (r'\\%', '%'),  # unescape %
            (r'\\textbf{([^}]*)}', r'**\1**'),  # bold text
            (r'\{ *\\bf *([^}]*)\}', r'**\1**'),
            (r'\\textit{([^}]*)}', r'*\1*'),  # italic text
            (r'\{ *\\it *([^}]*)\}', r'*\1*'),
            (r'\\LaTeX', 'LaTeX'),  # \LaTeX to boring old LaTeX
            (r'\\TeX', 'TeX'),  # \TeX to boring old TeX
            ('---', '-'),  # em dash
            ('--', '-'),  # en dash
            (r'``([^\']*)\'\'', r'"\1"'),  # quotes
            (r'\\url{([^}]*)}', r'[\1](\1)'),  # urls
            (r'\\href{([^}]*)}{([^}]*)}', r'[\2](\1)'),  # urls
            (r'\{([^}]*)\}', r'\1'),  # Brackets.
            (r'\\newline', r'<br/>'),
        ],
        specified_tag,
        short
    )


    if args.latex or args.markdown:
        if args.latex:
            process_resume(LATEX_CONTEXT, yaml_data, args.preview, specified_tag=specified_tag, short=short)
        elif args.markdown:
            process_resume(MARKDOWN_CONTEXT, yaml_data, args.preview, specified_tag=specified_tag, short=short)
    else:
        process_resume(LATEX_CONTEXT, yaml_data, args.preview, specified_tag=specified_tag, short=short)
        process_resume(MARKDOWN_CONTEXT, yaml_data, args.preview, specified_tag=specified_tag, short=short)


if __name__ == "__main__":
    main()
