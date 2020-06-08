# bibpy v1.0.0

[![Build status](https://travis-ci.org/MisanthropicBit/bibpy.svg?branch=master)](https://travis-ci.org/github/MisanthropicBit/bibpy)
[![Read the Docs](https://img.shields.io/readthedocs/bibpy)](https://readthedocs.org/projects/bibpy/)
[![Coverage Status](https://coveralls.io/repos/github/MisanthropicBit/bibpy/badge.svg?branch=master)](https://coveralls.io/github/MisanthropicBit/bibpy?branch=master)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/MisanthropicBit/bibpy/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/bibpy)](https://pypi.org/project/bibpy/)
[![PyPI wheel](https://img.shields.io/pypi/wheel/bibpy)](https://pypi.org/project/bibpy/)
[![Python version](https://img.shields.io/pypi/pyversions/bibpy.svg)](https://pypi.org/project/bibpy/)

Python library for parsing bib(la)tex files and manipulating entries.

* [Automatic conversion](https://github.com/MisanthropicBit/bibpy/tree/master/examples/field_conversion.py) of entry fields to and from appropriate Python types
* [Requirements-checking for entry fields](https://github.com/MisanthropicBit/bibpy/tree/master/examples/requirements_check.py)
* [String variable expansion and unexpansion](https://github.com/MisanthropicBit/bibpy/tree/master/examples/string_expansion.py)
* [Crossreference and xdata inheritance](https://github.com/MisanthropicBit/bibpy/tree/master/examples/crossref_expansion.py)
* Accompanying [tools](https://bibpy.readthedocs.io/en/latest/tutorial.html#bibpy-tools)

# Installation

```bash
pip install bibpy
```

<a name="quickstart"></a>
# Quickstart

```python
>>> import bibpy
>>> result = bibpy.read_file('references.bib')  # Read a bib file
>>> entries = result.entries
>>> print len(entries)
6
>>> print entries[0].author
'D. J. Power'
>>> print entries[0].bibkey
'2006_power'
>>> print entries[0].bibtype
'online'
>>> print entries[0].valid('bibtex')
True  # Entry is a valid bibtex entry
>>> print entries[0].valid('biblatex')
False  # But is not a valid biblatex entry (missing field 'date' or 'year')
>>> print entries[0].aliases('bibtex')
[]
>>> print entries[0].aliases('biblatex')
['electronic', 'www']
>>> bibpy.write_file('references.bib', entries)
```

See the [`examples`](https://github.com/MisanthropicBit/bibpy/tree/master/examples)
folder for more usage examples or read the
[tutorial](https://bibpy.readthedocs.io/en/latest/tutorial.html).

## Tools

`bibpy` also comes with three tools in the `bin` folder that are installed as
runnable scripts.

* `bibformat`: Clean up, format and align references
* `bibgrep`  : Find and filter references using a simple query language
* `bibstats` : Display statistics about bib files

All three tools are described in more detail in the
[tutorial](https://bibpy.readthedocs.io/en/latest/tutorial.html#bibpy-tools).
