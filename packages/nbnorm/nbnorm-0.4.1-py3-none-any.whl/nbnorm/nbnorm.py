"""
convenience tool for normalizing notebooks
"""

# pylint: disable=missing-function-docstring, missing-class-docstring

import sys
import re
from pathlib import Path
from enum import Enum
import traceback
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


import IPython
from nbformat.notebooknode import NotebookNode
import jupytext


from nbnorm.xpath import xpath, xpath_create

from jupytext.config import find_jupytext_configuration_file, load_jupytext_configuration_file

def jupytext_config():
    config_file = find_jupytext_configuration_file('.')
    config = load_jupytext_configuration_file(config_file)
    return config


LANG_INFO_PADDING = {
    'language_info': {
        'name': 'python',
        'nbconvert_exporter': 'python',
        'pygments_lexer': 'ipython3',
    }
}

CELLTOOLBAR_CLEAR = {
    'celltoolbar': 'None'
}

####################
# padding is a set of keys/subkeys
# that we want to make sure are defined
# this will never alter a key already present
# just add key-pair values from the default
# it means that we define these keys
# if not yet present

def pad_metadata(metadata, padding, force=False):
    """
    makes sure the keys in padding are defined in metadata
    if force is set, overwrite any previous value
    """
    for key, value in padding.items():
        if isinstance(value, dict):
            sub_meta = metadata.setdefault(key, {})
            pad_metadata(sub_meta, value, force)
        if not isinstance(value, dict):
            if force:
                metadata[key] = value
            else:
                metadata.setdefault(key, value)

def clear_metadata(metadata, padding):
    """
    makes sure the keys in padding are removed in metadata
    """
    for key, value in padding.items():
        # supertree missing in metadata : we're good
        if key not in metadata:
            continue
        if isinstance(value, dict):
            sub_meta = metadata[key]
            clear_metadata(sub_meta, value)
        if not isinstance(value, dict):
            del metadata[key]


####################
class Notebook:

    def __init__(self, name, verbose):
        if name.endswith(".ipynb"):
            name = name.replace(".ipynb", "")
        self.name = name
        #self.filename = "{}.ipynb".format(self.name)
        self.filename = self.name
        self.verbose = verbose
        self.notebook = None


    def parse(self):
        try:
            self.notebook = jupytext.read(self.filename, config=jupytext_config())
        except Exception:       # pylint: disable=broad-except
            print(f"Could not parse {self.filename}")
            traceback.print_exc()

    # def debug(self, message):
    #     print(f"-- {message} - we have {len(self.notebook.cells)} cells")
    #     for index, cell in enumerate(self.notebook.cells[:3]):
    #         print(f"cell #{index} has type {cell.cell_type}")

    def xpath(self, path):
        return xpath(self.notebook, path)

    def xpath_create(self, path, leaf_type):
        return xpath_create(self.notebook, path, leaf_type)

    def cells(self):
        return self.xpath('cells')

    def cell_contents(self, cell):
        return cell['source']


    def first_heading1(self):
        for cell in self.cells():
            if cell['cell_type'] == 'heading' and cell['level'] == 1:
                return xpath(cell, 'source')
            elif cell['cell_type'] == 'markdown':
                lines = self.cell_contents(cell).split("\n")
                line = lines[0]
                if line.startswith('# '):
                    return line[2:]
        return "NO HEADING 1 found"

    def set_title_from_heading1(self, *, title, force_title):
        """
        set 'nbhosting.title'
        if title=='h1', use the first heading 1 cell
        if already present: not overwritten except if force_title
        """
        # do not do anything if title not provided
        if title is None:
            return
        # retrieve previous one
        old_title = self.xpath_create('metadata.nbhosting.title', str)
        # compute what it would become
        if title == 'h1':
            new_title = self.first_heading1()
        else:
            new_title = title
        # if already present, do nothing unless force_title
        if old_title and force_title is None:
            if self.verbose and new_title != old_title:
                print(f"---- {self.filename}:\n"
                      f"     title `{old_title}`\n"
                      f"     not changed to `{new_title}`")
                print(f"  use -f to override") # pylint: disable=f-string-without-interpolation
            return
        self.xpath('metadata.nbhosting')['title'] = new_title
        if self.verbose:
            print(f"{self.filename} title -> {self.xpath('metadata.nbhosting.title')}")

    def fill_language_info(self, language_info):
        """
        make sure the language_info section is defined
        """
        if not language_info:
            return
        pad_metadata(self.notebook['metadata'], LANG_INFO_PADDING)

    def _ensure_item(self, name, cell_type, rank, crumb, template_filename):
        path = Path(template_filename)

        if not path.exists():
            raise FileNotFoundError(f"the {name} feature requires a {template_filename} file")

        with path.open(encoding="utf-8") as feed:
            text = feed.read().rstrip("\n")

        # a bit rustic but good enough
        def is_item_cell(cell):
            source = cell['source'].lower()
            nonlocal crumb
            crumb = crumb.lower()
#            if self.verbose:
#                print(f"for {name}, searching {crumb} in {source}")
            return re.search(crumb, source) is not None

        # look only in the first 6 cells
        for cell in self.cells()[:6]:
            if is_item_cell(cell):
                if cell['source'] != text:
                    cell['source'] = text
                break
        else:
            self.cells().insert(
                rank-1,
                NotebookNode({
                    "cell_type": cell_type,
                    "metadata": {},
                    "source": text,
                }))


    def ensure_style(self, style_rank, style_crumb):
        """
        make sure one of the first cells is a style cell

        the actual text is searched in a file named .style
        """
        return self._ensure_item(
            "style", "code", style_rank, style_crumb, ".style")

    def ensure_license(self, license_rank, license_crumb):
        """
        make sure one of the first cells is a license cell

        the actual text is searched in a file named .license
        """
        return self._ensure_item(
            "license", "markdown", license_rank, license_crumb, ".license")



    # I keep the code for these 2 but don't need this any longer
    # as I have all kinds of shortcuts and interactive tools now
    # plus, nbconvert(at least in jupyter) has preprocessor options to deal
    # with this as well
    def clear_all_outputs(self):
        """
        clear the 'outputs' field of python code cells,
        and remove 'prompt_number' as well when present
        """
        for cell in self.cells():
            if cell['cell_type'] == 'code':
                cell['outputs'] = []
                if 'prompt_number' in cell:
                    del cell['prompt_number']
                # this is now required in nbformat4
                if 'execution_count' in cell:
                    cell['execution_count'] = None


    def empty_cell(self, cell):
        try:
            return cell['cell_type'] == 'code' and not cell['input']
        except KeyError:
            return cell['cell_type'] == 'code' and not cell['source']

    def remove_empty_cells(self):
        """
        remove any empty cell - code cells only for now
        """
        nb_empty = 0
        cells_to_remove = [
            cell for cell in self.cells() if self.empty_cell(cell)]
        nb_empty += len(cells_to_remove)
        for cell_to_remove in cells_to_remove:
            self.cells().remove(cell_to_remove)
        if nb_empty:
            print(f"found and removed {nb_empty} empty cells")

    re_blank = re.compile(r"\A\s*\Z")
    re_bullet = re.compile(r"\A\s*\*\s")
    class Line(Enum):
        BLANK = 0
        BULLET = 1
        REGULAR = 2

    def line_class(self, line):
        if not line or self.re_blank.match(line):
            return self.Line.BLANK
        if self.re_bullet.match(line):
            return self.Line.BULLET
        return self.Line.REGULAR


    # this is an attempt at fixting a bad practice
    def fix_ill_formed_markdown_bullets(self):
        """
        Regular markdown has it that if a bullet list is inserted right after
        a paragraph, there must be a blank line before the bullets.
        However this somehow is not enforced by jupyter,  and being lazy
        I have ended up used this **a lot**; but that does not play well with
        pdf generation.
        """
        nb_patches = 0
        for cell in self.cells():
            if cell['cell_type'] != 'markdown':
                continue
            source = cell['source']
            # oddly enough, we observe that the logo cells
            # come up with source being a list, while all others
            # show up as str
            if isinstance(source, list):
                continue
            new_lines = []
            lines = source.split("\n")
            # it's convenient to take line #0 as a blank line
            curr_type = self.Line.BLANK
            for line in lines:
                next_type = self.line_class(line)
                # this seems to be the only case that matters
                if (curr_type == self.Line.REGULAR and next_type == self.Line.BULLET):
                    # insert artificial newline
                    new_lines.append("")
                    nb_patches += 1
                # always preserve initial input
                new_lines.append(line)
                # remember for next line
                curr_type = next_type
            new_source = "\n".join(new_lines)
            if  new_source != source:
                cell['source'] = new_source
        if nb_patches != 0:
            print(f"In {self.name}:"
                  f"fixed {nb_patches} occurrences of ill-formed bullet")


    MAX_CODELEN = 80

    def spot_long_code_cells(self):
        """
        Prints out a warning when a code cell has a line longer than
        a hard-wired limit
        """
        for cell in self.cells():
            if cell['cell_type'] != 'code':
                continue
            source = cell['source']
            for line in source.split("\n"):
                if len(line) >= self.MAX_CODELEN:
                    print(f"{self.name} - WARNING "
                          f"code line {len(line)} longer than {self.MAX_CODELEN}")
                    print(f"{line}")


    def spot_md_escapes_4_spaces(self):
        for index, cell in enumerate(self.cells(), 1):
            if cell.cell_type != 'markdown':
                continue
            lines = (cell.source
                     if isinstance(cell.source, list)
                     else cell.source.split("\n"))
            in_backquotes = False
            for line in lines:
                if line.startswith("```"):
                    in_backquotes = not in_backquotes
                if not in_backquotes and line.startswith("    "):
                    print(f"MD4SP: {self.name}:{index} -> {line}")

    # in one ontebook of w8 we have a lot of urls
    # embedded in quoted sections of the Markdown
    # so they show up as false positive
    # could maybe be coupled with the previous spotting add-on ..
    def spot_direct_urls(self):
        for index, cell in enumerate(self.cells(), 1):
            if cell.cell_type != 'markdown':
                continue
            lines = (cell.source
                     if isinstance(cell.source, list)
                     else cell.source.split("\n"))
            for line in lines:
                match1 = re.search(r'(?P<url>http[s]?://[^/\]\)]*)/', line)
                if not match1:
                    continue
                url = match1.group('url')
                match2 = re.search(rf'\[.*\]\(.*{url}.*\)', line)
                if match2:
                    continue
                match3 = re.search(rf'<.*{url}.*>', line)
                if not match3:
                    print(f"DIRURL: {self.name}:{index} -> {line}")


    def save(self):
        jupytext.write(self.notebook, self.filename, config=jupytext_config())
        print(f"{self.filename} saved")


    def full_monty(self, *, title, force_title,
                   style_rank, style_crumb,
                   license_rank, license_crumb,
                   language_info, celltoolbar,
                   backquotes, urls):
        self.parse()
        self.clear_all_outputs()
        self.remove_empty_cells()
        self.set_title_from_heading1(title=title, force_title=force_title)
        self.fill_language_info(language_info)
        if celltoolbar:
            clear_metadata(self.notebook['metadata'], CELLTOOLBAR_CLEAR)
        if style_rank is not None:
            self.ensure_style(style_rank, style_crumb)
        if license_rank is not None:
            self.ensure_license(license_rank, license_crumb)
        self.fix_ill_formed_markdown_bullets()
        self.spot_long_code_cells()
        if backquotes:
            self.spot_md_escapes_4_spaces()
        if urls:
            self.spot_direct_urls()
        self.save()


def full_monty(name, **kwds):
    verbose = kwds['verbose']
    del kwds['verbose']
    Notebook(name, verbose).full_monty(**kwds)


USAGE = """normalize notebooks
 * Metadata
   * checks for nbhosting.title (from first heading1 if missing, or from forced name on the command line)
 * Contents
   * makes sure a correct license cell is inserted - defined in .license
   * same for a style cell - defined in .style
* Miscell
   * clears all outputs
   * removes empty code cells
  * also notify of miscell common markdown errors
"""

def main():
    parser = ArgumentParser(usage=USAGE, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-t", "--title", action="store", dest="title", default=None,
        help="""value for nbhosting.title; can be a plain string,
                or 'h1' to use the first header;
                by default, the title is not overridden if already present,
                use the -f option to force a replacement""")
    parser.add_argument(
        "-f", "--force-title", action="store", dest="force_title", default=None,
        help="""force writing nbhosting.title (when provided with -t),
                even if already present""")
    parser.add_argument(
        "-s", "--style-rank", dest='style_rank', default=None, action='store', type=int,
        help="""make sure the style cell is up-to-date with .style;
                provide the style rank, used only for inserting a missing cell;
                default is to not manage style""")
    parser.add_argument(
        "-S", "--style-crumb", default=r"HTML\(",
        help="a cell that contains that string is considered a style cell")
    parser.add_argument(
        "-l", "--license-rank", dest='license_rank', default=None, action='store', type=int,
        help="""make sure the license cell is up-to-date with .license;
                provide the license cell rank, used only for inserting a missing cell;
                default is to not manage license""")
    parser.add_argument(
        "-L", "--license-crumb", default="license",
        help="a cell that contains that string is considered a license cell")
    parser.add_argument(
        "-i", "--language-info", default=False, action='store_true',
        help="make sure the language_info section is defined")
    parser.add_argument(
        "-c", "--celltoolbar", default=False, action='store_true',
        help="clear celltoolbar")
    parser.add_argument(
        "-b", "--backquotes", default=False, action='store_true',
        help="check for use of ``` rather than 4 preceding spaces")
    parser.add_argument(
        "-u", "--urls", default=False, action='store_true',
        help="tries to spot direct URLs, i.e. used outside of markdown []()")
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", default=False,
        help="show current nbhosting.title")
    parser.add_argument(
        "notebooks", nargs="*",
        help="the notebooks to normalize")
    parser.add_argument(
        "--summary", action="store_true", default=False,
        help="show summary of all settings - exit immediately"
    )

    args = parser.parse_args()

    if args.summary:
        print(f"nbhosting.title: {args.title}")
        print(f"force title: {args.force_title}")
        print(f"style rank: {args.style_rank}")
        print(f"style crumb: {args.style_crumb}")
        print(f"license rank: {args.license_rank}")
        print(f"license crumb: {args.license_crumb}")
        print(f"language info: {args.language_info}")
        print(f"celltoolbar: {args.celltoolbar}")
        print(f"backquotes: {args.backquotes}")
        print(f"urls: {args.urls}")
        exit(0)

    if not args.notebooks:
        parser.print_help()
        sys.exit(1)

    for notebook in args.notebooks:
        if args.verbose:
            print(f"{sys.argv[0]} is opening notebook {notebook}")
        full_monty(
            notebook, title=args.title, force_title=args.force_title,
            license_rank=args.license_rank, license_crumb=args.license_crumb,
            style_rank=args.style_rank, style_crumb=args.style_crumb,
            language_info=args.language_info, celltoolbar=args.celltoolbar,
            backquotes=args.backquotes,
            urls=args.urls, verbose=args.verbose)

if __name__ == '__main__':
    main()
