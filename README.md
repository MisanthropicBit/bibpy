# bibpy v0.1.0

![Build status](https://travis-ci.org/MisanthropicBit/colorise.svg?branch=rgb_256_exts)
![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)(https://raw.githubusercontent.com/MisanthropicBit/colorise/rgb_256_exts/LICENSE)

Python library for parsing bib(la)tex files and manipulating entries.

* [Automatic conversion](/examples/field_conversion.py) of entry fields to and from appropriate Python types
* [Requirements-checking for entry fields](/examples/requirements_check.py)
* [String variable expansion and unexpansion](/examples/string_expansion.py)
* [Crossreference and xdata inheritance](/examples/crossref_expansion.py)
* Accompanying [tools](#tools)

Take a look at the [quickstart example](#quickstart) for basic usage, or the
more complete [tutorial](TUTORIAL.md).

# Installation

Use pip:

```bash
pip install bibpy
```

Or `git clone https://github.com/MisanthropicBit/bibpy` and then run `python
setup.py install` from the `bibpy` directory.

## Tools

`bibpy` also comes with three tools in the `bin` folder that are installed as
runnable scripts.

* `bibformat`: Clean up, format and align references
* `bibgrep`  : Find and filter references using a simple query language
* `bibstats` : Display statistics about bib files

`bibgrep` is especially useful in conjunction with the other tools, e.g. to find
all article entries where the author field contains 'Hughes' (case-sensitive)
and print statistics as well as the total number of entries found, we can run:

```bash
$ bibgrep --entries="article" --field="author~Hughes" | bibstats --total
```

To find all entries with a year field in the inclusive range [1900;
2000] and export them to xml using `bibformat`, run:

```bash
$ bibgrep --field="year=1900-2000" | bibformat --export=xml
```

See the [tutorial](TUTORIAL.md) for more information.

<a name="quickstart"></a>
# Quickstart

```python
import bibpy
import re

# Read a bib file and convert fields if possible
entries, strings, preambles, comment_entries, comments =\
    bibpy.read_file("references.bib", postprocess=True)

print len(entries)                                      # Print number of entries
print entries[0].author                                 # Print the author of the first entry
print [entry for entry in entries if entry.year > 2010] # Print all entries after year 2010
print set([entry.author for entry in entries])          # Print all unique authors
print [entry for entry in entries
       if re.search('david', entry.key, re.I)]          # Print all entries where the key contains
                                                        # 'david'
print entries[0].valid('biblatex')                      # Check that the first entry has the correct
                                                        # fields for its type according to biblatex
print entries[0].entry_type                             # For example 'article' or 'inproceedings'
print entries[0].aliases('bibtex')                      # Print the available aliases for this entry's type

# Write out the entries to "references.bib" as biblatex. Also align equal-signs,
# use 'and' between names (author, institution etc.), a semi-colon for delimiting
# keywords and display the three fields in 'order' first if possible
bibpy.write_file("references.bib", entries,
                 'biblatex',
                 align=True,
                 name_delimiter='and',
                 keyword_delimiter=';',
                 order=['author', 'title', 'year'])
```

See the `examples` folder for more usage examples.
