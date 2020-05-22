# -*- coding: utf-8 -*-

"""Test that strings or files are in the correct reference format."""

import bibpy
import pytest


@pytest.fixture
def bibtex_entries():
    return """
A collection of bibtex entries

@article{key,
    author  = {Author},
    title   = {Title},
    journal = {Journal},
    year    = 2000
}

@book{key,
    author    = {Author},
    title     = {Title},
    publisher = {Publisher},
    year      = {2000}
}

@book{key,
    editor    = {Author},
    title     = {Title},
    publisher = {Publisher},
    year      = "2000"
}

@booklet{key,
    title = {Title}
}

@inbook{key,
    editor    = {Editor},
    title     = {Title},
    chapter   = {Chapter},
    pages     = {Pages},
    publisher = {Publisher},
    year      = 1998
}

@incollection{key,
    author    = {Author},
    title     = {Title},
    booktitle = {Booktitle},
    publisher = {Publisher},
    year      = 1998,
    address   = {123 Illinois}
}

@inproceedings{key,
    author    = {Author},
    title     = {Title},
    booktitle = {Booktitle},
    year      = 1998,
}

@manual{key,
    title = {Title},
    organization = {Organization}
}

@misc{key,
}

@proceedings{key,
    title     = {Title},
    booktitle = {Booktitle},
    year      = 1998,
    note      = {...}
}

@unpublished{key,
    month = {12},
    year = 1854,
    author = "Author",
    title = {Title},
    note = "Bla bla bla"
}

@conference{key,
    author    = {Author},
    booktitle = {Booktitle},
}

@masterthesis{key,
    year = "1945",
    author = "Author",
    title = {Title},
    school = "The {Institute} of Schools"
}

@phdthesis{key,
    year = "1945",
    school = "UWT",
    author = "Author",
    title = {Title},
    type = {PhD}
}

@techreport{key,
    school = "UWT",
    number = {19},
    author = {Author},
    title = {Title},
    year = "2032",
    institution = {Tech. School}
}"""


def test_bibtex():
    assert bibpy.string_is_format(
        open('tests/data/valid_bibtex.bib').read(),
        'bibtex'
    )
    assert not bibpy.string_is_format(
        open('tests/data/invalid_bibtex1.bib').read(),
        'bibtex'
    )
    assert not bibpy.string_is_format(
        open('tests/data/invalid_bibtex2.bib').read(),
        'bibtex'
    )

    assert bibpy.file_is_format('tests/data/valid_bibtex.bib', 'bibtex')
    assert not bibpy.file_is_format('tests/data/invalid_bibtex1.bib', 'bibtex')
    assert not bibpy.file_is_format('tests/data/invalid_bibtex2.bib', 'bibtex')
    assert not bibpy.file_is_format('tests/data/valid_biblatex.bib', 'bibtex')
    assert not bibpy.file_is_format('tests/data/valid_mixed.bib', 'bibtex')


def test_biblatex():
    assert not bibpy.string_is_format(
        open('tests/data/invalid_bibtex2.bib').read(),
        'biblatex'
    )

    assert bibpy.file_is_format('tests/data/valid_biblatex.bib', 'biblatex')
    assert not bibpy.file_is_format(
        'tests/data/invalid_bibtex2.bib',
        'biblatex'
    )
    assert not bibpy.file_is_format('tests/data/valid_mixed.bib', 'biblatex')


def test_mixed():
    assert bibpy.file_is_format('tests/data/valid_mixed.bib', 'mixed')
    assert bibpy.file_is_format('tests/data/valid_bibtex.bib', 'mixed')
    assert bibpy.file_is_format('tests/data/valid_biblatex.bib', 'mixed')


def test_bibtex_string(bibtex_entries):
    assert bibpy.string_is_format(bibtex_entries, 'bibtex')
