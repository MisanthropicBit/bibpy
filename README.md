# bibpy v0.1.0

![Build status](https://travis-ci.org/MisanthropicBit/bibpy.svg?branch=master)
![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)
[![PyPI version](https://badge.fury.io/py/bibpy.svg)](https://badge.fury.io/py/bibpy)

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

<a name="quickstart"></a>
# Quickstart

```python
import bibpy
import re

# Read a bib file
entries, strings, preambles, comment_entries, comments =\
    bibpy.read_file("references.bib")

# Print number of entries
print len(entries)
# Print the author of the first entry
print entries[0].author
# Print all entries after year 2010
print [entry for entry in entries if entry.year > 2010]
# Print all unique authors
print set([entry.author for entry in entries])
# Print all entries where the key contains 'david'
print [entry for entry in entries
       if re.search('david', entry.key, re.I)]
# Check that the first entry has the correct
# fields for its type according to biblatex
print entries[0].valid('biblatex')
# For example 'article' or 'inproceedings'
print entries[0].entry_type
# Print the available aliases for this entry's type
print entries[0].aliases('bibtex')

# Write out the entries to "references.bib" as biblatex.
bibpy.write_file("references.bib", entries, 'biblatex')
```

See the `examples` folder for more usage examples or read the
[tutorial](TUTORIAL.md).

## Tools

`bibpy` also comes with three tools in the `bin` folder that are installed as
runnable scripts.

* `bibformat`: Clean up, format and align references
* `bibgrep`  : Find and filter references using a simple query language
* `bibstats` : Display statistics about bib files

All three tools are described in more detail in the
[tutorial](TUTORIAL.md/#tools).
