"""Test requirements."""

import bibpy
import pytest


def test_non_supported_formats():
    assert bibpy.requirements.check(None, 'relaxed') == (frozenset(), [])
    assert bibpy.requirements.check(None, 'mixed') == (frozenset(), [])


@pytest.mark.skip
def test_bibtex_requirements():
    entries, _, _, _, _ =\
        bibpy.read_file('tests/data/bibtex_missing_requirements.bib', 'bibtex')

    expected_fields = [
        # article
        (set(), []),
        (set(), []),
        (set(), []),
        (set(['author']), []),
        (set(['title']), []),
        (set(['journal']), []),
        (set(['year']), [])
    ]

    for entry, [required, either] in zip(entries, expected_fields):
        assert bibpy.requirements.check(entry, 'bibtex') ==\
            (required, either)

    assert bibpy.requirements.check(entry, 'relaxed') == (set(), [])


def test_biblatex_requirements():
    entries, _, _, _, _ =\
        bibpy.read_file('tests/data/biblatex_missing_requirements.bib',
                        'biblatex')

    expected_fields = [
        # article
        (set(), []),
        (set(), []),
        (set(), []),
        (set(['author']), []),
        (set(['title']), []),
        (set(['journaltitle']), []),
        (set(), [set(['date', 'year'])]),
        # book
        (set(), []),
        (set(), []),
        (set(), []),
        (set(['author']), []),
        (set(['title']), []),
        (set(), [set(['date', 'year'])]),
        # mvbook
        (set(), []),
        (set(), []),
        (set(), []),
        (set(['author']), []),
        (set(['title']), []),
        (set(), [set(['date', 'year'])]),
        # booklet
        (set(), []),
        (set(), []),
        (set(), []),
        (set(), []),
        (set(), []),
        (set(['title']), [])
    ]

    for entry, [required, either] in zip(entries, expected_fields):
        assert bibpy.requirements.check(entry, 'biblatex') ==\
            (required, either)

    assert bibpy.requirements.check(entry, 'relaxed') == (set(), [])


def test_collecting():
    entries, _, _, _, _ =\
        bibpy.read_file('tests/data/valid_bibtex.bib',
                        'bibtex')

    assert bibpy.requirements.collect(entries, 'bibtex') ==\
        [(entries[11], (set(['title', 'year']), []))]
