Tutorial
========

This tutorial is meant to give a quick overview of all the features of bibpy.
You can also refer to the `examples
<https://github.com/MisanthropicBit/bibpy/tree/master/examples>`_.

Table of Contents
-----------------

* `Reading and Writing`_
* `Manipulating Reference Data`_
* `Requirements Checking`_
* `Post- and Preprocessing Fields`_
* `String Variable Expansion`_
* `Crossreferences and xdata Inheritance`_
* `bibpy Tools`_

Reading and writing
-------------------

You can read reference data from a string or from a file.

.. code:: bash

    >>> import bibpy
    >>> result1 = bibpy.read_string('@article{key, title = {Title}, author = {Author}}')
    >>> result2 = bibpy.read_file('references.bib')

Both functions return an :py:func:`bibpy.entries.Entries` class containing all
bibliographic entries (:code:`@conference` etc.), strings (:code:`@string`),
preambles (:code:`@preamble`), comment entries (:code:`@comment`) and finally
all comments in the source (which exist outside of entries).

By default, :py:func:`bibpy.read_string` and :py:func:`bibpy.read_file` read
data in the :code:`relaxed` mode (via the :code:`format` parameter) but
supports four different reference formats:

* **bibtex:** Treat data as bibtex. Raise error on non-conformity.
* **biblatex:** Treat data as biblatex. Raise error on non-conformity.
* **mixed:** Treat data as a mixture of bibtex and biblatex. Raise error on non-conformity.
* **relaxed:** Relax parsing rules. All types of entries and fields are allowed.

For example if you read a file containing an :code:`@online` entry as bibtex,
bibpy would raise an error since this entry type only exists in biblatex.
Therefore, the relaxed format is typically recommended when parsing third party
bib files.

Writing bib entries is straight-forward and you do not have to supply a
reference format as the entries are simply written with the data they contain.

.. code:: bash

    # Assume we still have the entries from the previous example loaded here
    >>> bibpy.write_string(result1.entries)
    >>> bibpy.write_file('new-references.bib', result2.entries)

Both functions take a lot of formatting options for e.g. alignment of the equal
signs of fields in entries, sorting fields alphabetically or using a
user-defined, partial order. Try running the `formatting example
<https://github.com/MisanthropicBit/bibpy/blob/master/examples/formatting.py>`_
to see the effects of all the options.

Manipulating reference data
---------------------------

bibpy has been designed so manipulating reference data is easy. For this
section, we assume that we have loaded the following data into the variable
:code:`entries`:

.. code:: bibtex

    @article{key1,
        author      = {James Conway and Archer Sterling},
        title       = {1337 Hacker},
        year        = {2010},
        month       = {4},
        institution = {Office of Information Management {and} Communications},
        message     = {Hello!},
        date        = {2001-07-19/}
    }

    @online{key2,
        author = {Hugh Morrison}
    }

We can iterate the fields and values of the first entry.

.. code:: python

    for field, value in entries[0]:
        print('{0} = {1}'.format(field, value))

All bibtex/biblatex fields are already accessible as properties of the entry
objects and the entries themselves support a range of sensible dict-like
operations. Entry fields that are not present in an entry return :code:`None`.

.. code:: python

    >>> entry = entries[0]
    >>> entry.author
    'James Conway and Archer Sterling'
    >>> entry.year
    '2010'
    >>> entry.bibtype
    'article'
    >>> entries[1].bibkey
    'key2'
    >>> entry['month']
    '4'
    >>> entry['invalid']
    None
    >>> entry.message
    Hello!
    >>> entry.date
    2001-07-19/
    >>> entry.invalid
    None
    >>> entry.institution
    'Office of Information Management {and} Communications'
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
    >>> entry.fields  # Get a list of the active (non-None) fields of the entry
    ['author', 'title', 'year', 'month', 'institution', 'message']
    >>> entry.extra_fields  # Get a list of any additional non-bibtex/biblatex fields
    ['message']
    >>> len(entry)  # Number of active fields in the entry
    6
    >>> entry.keys()  # Same as fields property (see below)
    ['author', 'title', 'year', 'month', 'institution', 'message']
    >>> entry.values()
    ['James Conway and Archer Sterling', '1337 Hacker', '2010', '4', 'Office of Information Management {and} Communications']
    >>> del entry['institution']
    >>> entry.fields
    ['author', 'title', 'year', 'month', 'message']
    >>> entry.clear()  # Clear all fields (set to None)

Requirements Checking
---------------------

Both bibtex and biblatex have requirements per entry that are usually not
enforced but are needed for proper formatting and bibpy can also check this for
you. Consider the entries below.

.. code:: bibtex

    Only optional date missing
    @article{key1,
        author       = {a},
        title        = {b},
        journaltitle = {c},
        year         = {d}
    }
    
    Missing author field
    @article{key4,
        title        = {b},
        journaltitle = {c},
        year         = {d}
    }

Is this valid biblatex?

.. code:: python

    >>> from bibpy.requirements import check
    >>> entries = ...  # Load entries
    >>> check(entries[0], 'biblatex')
    (set(), [])
    >>> check(entries[1], 'biblatex')
    (set(['author']), []),

The :py:func:`bibpy.requirements.check` function returns a 2-tuple. The first
element is a set of all missing required fields, the second element is a list
of sets of fields where only one of the fields are required. For example, some
bibtex entries need either an :code:`author` field or an :code:`editor` field.
No requirements are violated by the first entry since biblatex requires either
a :code:`year` or :code:`date` field and the former is provided.

Alternatively, you can call the :py:func:`bibpy.entry.entry.Entry.validate`
method on an entry to validate an exisiting entry which throws a
:py:func:`bibpy.error.RequiredFieldError` if any violations are found.

.. code:: python

    >>> entries[1].validate('biblatex')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    bibpy.error.RequiredFieldError: Entry 'key4' (type 'article') is missing required field(s): author

The exception contains the offending entry and the required and optional fields
that would be returned from :py:func:`bibpy.requirements.check`. There is also
a :py:func:`bibpy.entry.entry.Entry.valid` method that returns :code:`True` or
:code:`False` instead of raising an exception.

Finally, :py:func:`bibpy.requirements.collect` finds and aggregates all
requirement violations for a list of entries, grouped by entry. Entries that
conform are not included in the result.

.. code:: python

    >>> from bibpy.requirements import collect
    >>> collect(entries, 'bibtex')
    [(entry, (<set of required fields>, [...])), ...]

Post- and Preprocessing Fields
------------------------------

You may have noticed in the `Manipulating Reference Data`_ section that values
are returned as strings by default. You can supply :code:`postprocess=True` to
the :code:`read_*` methods to convert a subset of the standard bibtex/biblatex
fields' values to meaningful python types.  Accessing the fields of the entries
from the previous section would now return the following instead.

.. code:: python

    >>> entries = bibpy.read_file('references.bib', 'biblatex', postprocess=True).entries
    >>> entry = entries[0]
    >>> entry.author
    ['James Conway', 'Archer Sterling']  # Author names have been split
    >>> entry.year, type(entry.year)  # Year is now an int
    2010, <type 'int'>
    >>> entry.month  # Month has a proper name
    'April'
    >>> entry.institution  # Institutions are split but not on '{and}'
    ['Office of Information Management and Communications']
    >>> entry.date  # Dates are converted to an object
    bibpy.date.DateRange(2001-07-19/)
    >>> entry.date.start
    datetime.date(2001, 7, 19)
    >>> entry.end
    None
    >>> entry.open // True if an open-ended date range
    True

For name lists, 'and' is the default delimiter. bibpy does not split on
delimiters enclosed in braces, but removes them afterwards (the 'institution'
field was not split on 'and' because it was braced). A biblatex date is
converted to a special :py:func:`bibpy.date.DateRange` object since they can
both refer to single dates and the time period between two dates. In this case,
it refers to an open-ended date (hence the '/' at the end) starting on the 19th
of July 2001. When writing entries, its postprocessed fields are automatically
converted back to their pre-postprocessed counterparts.

If you need to postprocess fields manually (for example, you need to postprocess
a subset of fields only when a condition is met), you can use the postprocessing
functions directly.

.. code:: python

    from bibpy.postprocess import postprocess

    entries = bibpy.read_file(...).entries

    if condition:
        for entry in entries:
            # Postprocess the 'author' and 'date' fields if present
            postprocess(entry, ['author', 'date'])

String Variable Expansion
-------------------------

Some reference files contain string variables like these:

.. code:: bibtex

    @string{var1 = "Morrison"}

    @string(var2 = "Harvard")

    @article{key,
        title = "Jake " # var1,
    }

Each string entry contains a single variable name and a value for that
variable.  By using :py:func:`bibpy.expand_strings` on the entries after
reading, the article entry will be as though it had been as follows in the file
instead.

.. code:: bibtex

    @article{key,
        title = "Jake Morrison"
    }

Let's try and load the entry interactively.

.. code:: python

    >>> entries, strings = bibpy.read_file('references.bib', 'mixed', strings=True)[:2]
    >>> entries[0].title
    '"Jake" # var1'
    >>> bibpy.expand_strings(entries, strings)  # Done in-place
    >>> entries[0].title
    "Jake Morrison"
    >>> bibpy.unexpand_strings(entries, strings)  # We can also revert the expansion
    >>> entries[0].title
    '"Jake" # var1'

We can also undo the string variable expansion using
:py:func:`bibpy.unexpand_strings`. Both functions raise errors if they find
duplicate variable names by default which would make unexpansion impossible for
entries that use the duplicates. The unexpansion might also unexpand unrelated
text that happens to be the same as that of a variable. There is currently no
way to avoid this.

Crossreferences and xdata Inheritance
-------------------------------------

There are three primary ways to do inheritance through fields:
:code:`crossref`, :code:`xdata` and :code:`xref`. The latter is not supported
as no data is actually directly inherited, it is just a non-inheriting
reference to another entry. Imagine we have the following two fields in a file.

.. code:: bibtex

    @inbook{key1,
        crossref = {key2},
        title    = {Title},
        author   = {Author},
        pages    = {5--25}
    }

    @book{key2,
        subtitle  = {Booksubtitle},
        title     = {Booktitle},
        author    = {Author2},
        date      = {1995},
        publisher = {Publisher},
        location  = {Location}
    }

Reading in the file with bibpy and then using
:py:func:`bibpy.inherit_crossrefs`, the :code:`inbook` entry can inherit the
appropriate fields from the :code:`book` entry (done in-place).

.. code:: python

    >>> results = bibpy.read_file('crossreferences.bib', 'relaxed')
    >>> bibpy.inherit_crossrefs(results.entries)

Printing out the entries again shows that the :code:`title` and
:code:`subtitle` fields from the :code:`book` entry have been inherited (the
ordering of the fields may vary).

.. code:: bibtex

    @inbook{key1,
        crossref     = {key2},
        title        = {Title},
        booktitle    = {Booktitle},
        booksubtitle = {Booksubtitle},
        author       = {Author},
        pages        = {5--25}
    }

    @book{key2,
        subtitle  = {Booksubtitle},
        title     = {Booktitle},
        author    = {Author2},
        date      = {1995},
        publisher = {Publisher},
        location  = {Location}
    }

You can uninherit the fields again with :py:func:`bibpy.uninherit_crossrefs`.
You can also inherit and uninherit :code:`xdata` fields. The difference is that
while :code:`crossref` fields follow specific rules about which fields are
inherited and what their names become, :code:`xdata` simply pulls in the fields
from the ancestor and can optionally be made to overwrite existing fields with
the same names. If :code:`postprocess=True` when reading (see `Post- and
Preprocessing Fields`_), :code:`xdata` fields are converted from a
comma-separated string to a list of keys.

bibpy Tools
-------------

bibpy comes with three command line tools which we discuss in turn.

bibformat
^^^^^^^^^

The bibformat tool can be used to align equal signs :code:`=`, expand string
variables and reorder fields. Run :code:`bibformat --help` for full details.
Below is an example of reordering fields (ordering the :code:`author` and
:code:`title` fields before other fields in all entries, the rest are
arbitrarily ordered), aligning equal signs and surrounding field values with
double-quotes instead of braces.

.. code:: bash

    $ bibformat --order='author,title' --align --surround='""'
    @article{key4,
        author = "Archer Sterling",
        title  = "A Practical Guide To Getting Ants",
        year   = "1995",
        month  = "3"
    }

bibstats
^^^^^^^^

The bibstats tool displays statistics about bib entries. Run :code:`bibstats
--help` for full details. Below is an example of querying a bib source.

.. code:: bash

    $ bibstats --count source1.bib
    Found 4 entries
    $ bibstats --top=3 source2.bib  # Display the top 3 occurring entries
    Entry                Count
    -----------------------------------------
    article              881 (60.38%)
    inproceedings        256 (17.55%)
    techreport           113 (7.75%)

    Total entries: 1459

bibgrep
^^^^^^^

The bibgrep tool is similar to the grep command but filters entries instead of
lines.

.. code:: bash

    $ bibgrep --entry="article" --field="author~hughes" --ignore-case

The above invocation selects entries that are either :code:`@article` entries
or have "hughes" (case-insensitive) somewhere in their :code:`author` field.
The approximation operator :code:`~` also works with regular expressions.

.. code:: bash

    $ bibgrep --field="author~M.+tt" some.bib

Alternatively, one can use :code:`=` to require exact matches. We can also
combine :code:`bibgrep` with the other tools. Here we also specify inclusive
ranges for years and a lower bound for volume fields.

.. code:: bash

    $ bibgrep --entry="conference" | bibformat --indent=4 > conferences.json
    $ bibgrep --field="year=1900-2000" --field="volume>=10" | bibstats --top=5

The first command selects all :code:`@conference` entries and bibformat indents
them by 4 spaces. The second command selects all entries that have a year field
in the inclusive range [1900; 2000] **or** a volume field of 10 or more, then
prints out the statistics for the top 5 occurring entries that satisfy those
predicates.

Selecting entries that satisfy all constraints can be done by piping multiple
invocations of :code:`bibgrep`.

.. code:: bash

    $ bibgrep --entry="book" references.bib | bibgrep --field="month=1-3"

This selects all :code:`book` entries that were published in the first quarter
of any year.
