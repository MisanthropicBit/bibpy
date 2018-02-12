"""Test that we can read and write bib entries with postprocessing."""

import bibpy
import pytest


@pytest.fixture
def test_string():
    return """@article{key,
        author   = {James Conway and Archer Sterling and},
        xdata    = {key1, key2,key3,     key4, key5  ,},
        urldate  = {2017-01-14},
        keywords = {parsing; computer science   ; databases;  },
        year     = {1957},
        month    = {11},
        pages    = "11--20",
        msg      = "Part of " # var # " string",
        foreword = {Jan Leo {and} the Editors}
    }"""


def test_processing_invariant(test_string):
    entry = bibpy.read_string(test_string, postprocess=True,
                              remove_braces=True).entries[0]

    assert entry.author == ['James Conway', 'Archer Sterling']
    assert entry.xdata == ['key1', 'key2', 'key3', 'key4', 'key5']
    assert entry.urldate == bibpy.date.DateRange.fromstring('2017-01-14')
    assert entry.keywords == ['parsing', 'computer science', 'databases']
    assert entry.year == 1957
    assert entry.month == 'November'
    assert entry.pages == (11, 20)
    assert entry.msg == '"Part of " # var # " string"'
    assert entry.foreword == ['Jan Leo and the Editors']

    entry = bibpy.read_string(bibpy.write_string([entry]), postprocess=True,
                              remove_braces=True).entries[0]

    assert entry.xdata == ['key1', 'key2', 'key3', 'key4', 'key5']
    assert entry.urldate == bibpy.date.DateRange.fromstring('2017-01-14')
    assert entry.keywords == ['parsing', 'computer science', 'databases']
    assert entry.year == 1957
    assert entry.month == 'November'
    assert entry.pages == (11, 20)
    assert entry.msg == '"Part of " # var # " string"'
    assert entry.foreword == ['Jan Leo and the Editors']
