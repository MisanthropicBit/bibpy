"""Ensure that all flavors, apart from relaxed, can be parsed."""

import bibpy

filename = "tests/data/simple_1.bib"


def test_all_entry_types_bibtex():
    """Ensure that all bitex entry types can be parsed."""
    entry = bibpy.read_file(filename, 'bibtex').entries[0]

    assert entry.author == "James Conway and Archer Sterling"
    assert entry.title == "1337 Hacker"
    assert entry.year == "2010"
    assert entry.month == "4"
    assert entry.institution == "Office of Information Management {and} " +\
                                "Communications"


def test_all_entry_types_biblatex():
    """Ensure that all biblatex entry types can be parsed."""
    entry = bibpy.read_file(filename, 'biblatex').entries[0]

    assert entry.author == "James Conway and Archer Sterling"
    assert entry.title == "1337 Hacker"
    assert entry.year == "2010"
    assert entry.month == "4"
    assert entry.institution == "Office of Information Management {and} " +\
                                "Communications"


# def test_all_entry_types_mixed():
#     """Ensure that all mixed entry types can be parsed."""
#     entries = bibpy.read_string(test, "mixed")
#     # entries = bibpy.read_file(filename, "mixed")
