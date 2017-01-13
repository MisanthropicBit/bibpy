# Tutorial

This tutorial is meant to give a quick overview of all the features of `bibpy`.
You can also refer to the [examples](/examples).

## Table of Contents

* [Reading and Writing Strings and Files](#io)
* [Manipulating Reference Data](#basic_usage)
* [Requirements Checking](#requirements)
* [Post- and Preprocessing Fields](#processing)
* [String Variable Expansion](#strings)
* [Crossreferences and xdata Inheritance](#inheritance)
* [`bibpy` Tools](#tools)

<a name="io"></a>
## Reading and writing strings and files

You can read reference data from a string or from a file. `bibpy` supports four
different reference formats:

* **bibtex:** Treat data as bibtex. Raise parsing error on non-conformity.
* **biblatex:** Treat data as biblatex. Raise parsing error on non-conformity.
* **mixed:** Treat data as a mixture of bibtex and biblatex. Raise parsing errors on non-conformity.
* **relaxed:** Relax parsing rules. All types of entries and fields are allowed.

For example if you read a file containing an `@online` entry as bibtex, `bibpy`
would raise an error since this entry type only exists in biblatex. Therefore,
the `relaxed` format is typically recommended when parsing third party bib
files. Below is an example of reading data from a string and a file.

```python
>>> import bibpy
>>> entries = bibpy.read_string('@article{key, title = {Title}, author = {Author}}', 'bibtex')[0]
>>> entries = bibpy.read_file('references.bib', 'relaxed')[0]
```

Both functions return a [`collections.namedtuple`]() of five elements (notice
the index at the end of the functions): The entries (`@conference` etc.),
strings (`@string`), preambles (`@preamble`), comment entries (`@comment`) and
finally all comments in the source (which exist outside of entries).

Writing bib entries is straight-forward and you do not have to supply a
reference format as the entries are simply written with the data they contain.

```python
# Assume we still have the entries from the previous example loaded here
>>> bibpy.write_string(entries)
>>> bibpy.write_file('references.bib', entries)
```

Both functions take a lot of formatting options to e.g. align the equal signs of
fields in entries, or sort fields alphabetically or using a user-defined,
partial order. Try running the [formatting example](/examples/formatting.py) to
see the effects of all the options. There is also the `bibformat` tool which we
defer until a later section.

<a name="basic_usage"></a>
## Manipulating reference data

`bibpy` has been designed to be pythonic so most manipulation of reference data
should come naturally. For the remaining of this section, we assume that we have
loaded the following data into the variable `entries`:

```
@article{key1,
    author      = {James Conway and Archer Sterling},
    title       = {1337 Hacker},
    year        = {2010},
    month       = {4},
    institution = {Office of Information Management {and} Communications},
    message     = {Hello!}
}

@online{key2,
    author = {Hugh Morrison}
}
```

We can iterate the fields and values of the first entry.

```python
for field, value in entries[0]:
    print field, value
```

All bibtex/biblatex fields are already accessible as properties of the entry
objects and the entries themselves support a range of sensible dict-like
operations.

```python
>>> entry = entries[0]
>>> entry.author
'James Conway and Archer Sterling'
>>> entry.year
'2010'
>>> entry.entry_type
'article'
>>> entries[1].entry_key
'key2'
>>> entry['month']
'4'
>>> entry['invalid']
None
>>> entry.invalid
None
>>> 'institution' in entry
True
>>> 'volume' in entry
False
>>> entry == entries[1]
False
>>> entry == entry
True
>>> entry != entries[1]
True
>>> entry.aliases('biblatex')  # List of biblatex aliases for 'article'
[]
>>> entries[1].aliases('biblatex')
['electronic', 'www']
>>> entry.valid('biblatex')  # Does the entry contain all required fields according to biblatex?
True
>>> entry.fields  # Get a list of the active fields of the entry
['author', 'title', 'year', 'month', 'institution', 'message']
>>> entry.extra_fields  # Get a list of any additional non-bibtex/biblatex fields
['message']
>>> len(entry)  # Number of active fields in the entry
6
>>> entry.keys()  # Same as fields
['author', 'title', 'year', 'month', 'institution', 'message']
>>> entry.values()
['James Conway and Archer Sterling', '1337 Hacker', '2010', '4', 'Office of Information Management {and} Communications']
>>> entry.clear()  # Clear all fields (set to None)
>>> del entry['institution']
>>> entry.fields
['author', 'title', 'year', 'month', 'message']
```

Active fields...

<a name="processing"></a>
## Post- and Preprocessing Fields

You may have noticed in the previous section that values are returned as strings
by default (unicode strings by default). You can supply `postprocessing=True` to
the `read_*` methods to convert a subset of the standard bibtex/biblatex fields'
values to meaningful python types. Accessing the fields of the entries from the
previous section would now return the following instead.

```python
>>> entries = bibpy.read_file('references.bib', 'biblatex', postprocessing=True)[0]
>>> entries[0].author
['James Conway', 'Archer Sterling']
>>> entries[0].year
2010
>>> type(entries[0].year)
<type 'int'>
>>> entries[0].month
'April'
>>> entries[0].institution
['Office of Information Management and Communications']
```

For name lists, 'and' is the default delimiter. Notice that `bibpy` does not
split on delimiters enclosed in braces, but removes them afterwards. When
writing entries, its postprocessed fields are automatically converted back to
their pre-postprocessed counterparts.

<a name="strings"></a>
## String Variable Expansion

Some reference files contain string variables like these:

```
@string{ var1 = "Morrison" }
@string( var2 = "Harvard" )

@article{key,
    ...
    title = "Jake " # var1,
    ...
}
```

Each string entry contains a single variable name and a value for that variable.
By using `bibpy.expand_strings` on the entries after reading, the article entry
will be as though it was:

```
@article{key,
    ...
    title = "Jake Morrison"
    ...
}
```

Let's try and load the entry interactively.

```python
>>> entries, strings = bibpy.read_file('references.bib', 'mixed', strings=True)[:2]
>>> entries[0].title
'"Jake" # var1'
>>> bibpy.expand_strings(entries, strings)  # Done in-place
>>> entries[0].title
"Jake Morrison"
>>> bibpy.unexpand_strings(entries, strings)  # We can also revert the expansion
>>> entries[0].title
'"Jake" # var1'
```

As you can see, we can also undo the string variable expansion using
`bibpy.unexpand_strings`. Both functions report duplicate variable names by
default which would make unexpansion impossible for entries that use the
duplicates.

<a name="inheritance"></a>
## Crossreferences and xdata Inheritance

There are three primary ways to do inheritance through fields: `crossref`,
`xdata` and `xref`. The latter is not supported as ....

<a name="tools"></a>
## `bibpy` Tools

`bibpy` comes with three command line tools which we discuss in turn.

### `bibformat`

`bibformat` can be used to align `=` signs, order fields and export to different
formats. Run `bibformat --help` for full details. Below is an example of
exporting some entries to xml.

```bash
$ bibformat --order='author,title' --export=xml > entries.xml
```

Runinng this command orders the `author` and `title` fields first in all entries
(the rest are arbitrarily ordered) and exports the entries to xml.

### `bibstats`

`bibstats` displays statistics about bib entries. Run `bibstats --help` for full
details. Below is an example of querying a bib source.

```bash
$ bibstats --count source.bib
Found 4 entries
$ bibstats --top=3 source.bib  # Display the top 3 occurring entries
???
$ bibstats --total --percetanges --sort
???
```

The final command prints the total number of entries, the percentages of
different entry types and sorts the results ascendingly.

### `bibgrep`

`bibgrep` is by far the most powerful tool because it can be combined
effectively with the other two.

```bash
$ bibgrep --entries="article" --field="author~hughes" --ignore-case
```

The command selects all `@article` entries that have "hughes" (case-insensitive)
somewhere in their `author` field. Next, we illustrate how we can combine
`bibgrep` with the other tools.

```bash
$ bibgrep --entries="conference" | bibformat --indent=4 --export=json > conferences.xml
$ bibgrep --field="year=1900-2000" --field="volume>=10" | bibstats --top=5
```

The first command selects all `@conference` entries and exports them to json
with an indentation of 4 spaces. The second command selects all entries that
have a year field in the inclusive range [1900; 2000] **and** a volume field of
10 or more, then prints out the statistics for the top 5 occurring entries that
satisfy those predicates. (Show how to && and || predicates).
