# -*- coding: utf-8 -*-

"""Test reading functions."""

import bibpy
import pytest


def test_reading_empty():
    bibpy.read_string('', 'bibtex')
    bibpy.read_string('', 'biblatex')
    bibpy.read_string('', 'mixed')
    bibpy.read_string('', 'relaxed')

    with pytest.raises(IOError):
        bibpy.read_file('', 'bibtex')

    with pytest.raises(IOError):
        bibpy.read_file('', 'biblatex')

    with pytest.raises(IOError):
        bibpy.read_file('', 'mixed')

    with pytest.raises(IOError):
        bibpy.read_file('', 'relaxed')


def test_reading_relaxed():
    results = bibpy.read_file(
        'tests/data/bibtex_missing_requirements.bib',
        format='relaxed',
        ignore_comments=False
    )

    assert len(results.entries) == 12
    assert len(results.strings) == 0
    assert len(results.comment_entries) == 0
    assert len(results.preambles) == 0
    assert len(results.comments) == 12


def test_reading_errors():
    bibpy.read_string(
        'tests/data/bibtex_missing_requirements.bib',
        format='bibtex'
    )

    bibpy.read_string(
        'tests/data/bibtex_missing_requirements.bib',
        format='bibtex'
    )


def test_reading_encodings():
    bibpy.read_string('@article{key,author={James Grönroos}}', format='bibtex')

    bibpy.read_file(
        'tests/data/simple_1.bib',
        format='relaxed',
        encoding='ascii'
    )

    bibpy.read_file(
        'tests/data/simple_1.bib',
        format='relaxed',
        encoding='utf-8'
    )

    bibpy.read_file(
        'tests/data/simple_1.bib',
        format='relaxed',
        encoding='iso-8859-1'
    )

    with pytest.raises(UnicodeDecodeError):
        bibpy.read_file(
            'tests/data/iso-8859-1.bib',
            format='bibtex',
            encoding='utf-8'
        )
