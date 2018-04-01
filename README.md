# bibpy v0.1.0-alpha

![Build status](https://travis-ci.org/MisanthropicBit/bibpy.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/MisanthropicBit/bibpy/badge.svg?branch=master)](https://coveralls.io/github/MisanthropicBit/bibpy?branch=master)
![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)
[![PyPI version](https://badge.fury.io/py/bibpy.svg)](https://badge.fury.io/py/bibpy)
[![Can I Use Python 3?](https://caniusepython3.com/check/82202c33-6111-4c2c-9870-6245623dd3a8.svg)](https://caniusepython3.com/check/82202c33-6111-4c2c-9870-6245623dd3a8)

_`bibpy` is currently in alpha and will go up on PyPI after beta (also see [TODO.md](TODO.md))_.

Python library for parsing bib(la)tex files and manipulating entries. Tested on
Python 2.7, 3.3, 3.5, 3.6 and PyPy.

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

See the [`examples`](/examples) folder for more usage examples or read the
[tutorial](TUTORIAL.md).

## Tools

`bibpy` also comes with three tools in the `bin` folder that are installed as
runnable scripts.

* `bibformat`: Clean up, format and align references
* `bibgrep`  : Find and filter references using a simple query language
* `bibstats` : Display statistics about bib files

All three tools are described in more detail in the
[tutorial](TUTORIAL.md/#tools).
