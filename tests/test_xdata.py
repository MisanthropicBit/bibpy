# -*- coding: utf-8 -*-

"""Test inheritance of xdata fields."""

import bibpy
import bibpy.entry
import pytest


@pytest.fixture
def test_entries():
    entry1 = bibpy.entry.Entry(
        'xdata',
        'macmillan:name',
        **{
            'publisher': 'Macmillan'
        }
    )
    entry2 = bibpy.entry.Entry(
        'xdata',
        'macmillan:place',
        **{
            'location':  'New York and London'
        }
    )
    entry3 = bibpy.entry.Entry(
        'xdata',
        'macmillan',
        **{
            'xdata':  'macmillan:name,macmillan:place'
        }
    )
    entry4 = bibpy.entry.Entry(
        'book',
        'key',
        **{
            'author': 'Author',
            'title':  'Title',
            'date':   '2016-11-29',
            'xdata':  'macmillan'
        }
    )

    return entry1, entry2, entry3, entry4


def test_inheritance(test_entries):
    bibpy.inherit_xdata(test_entries)

    entry1 = test_entries[0]
    assert entry1.publisher == 'Macmillan'
    assert entry1.fields == ['publisher']

    entry2 = test_entries[1]
    assert entry2.location == 'New York and London'
    assert entry2.fields == ['location']

    entry3 = test_entries[2]
    assert entry3.xdata == 'macmillan:name,macmillan:place'
    assert entry3.publisher == 'Macmillan'
    assert entry3.location == 'New York and London'
    assert set(entry3.fields) == set(['xdata', 'publisher', 'location'])

    entry4 = test_entries[3]
    assert entry4.author == 'Author'
    assert entry4.title == 'Title'
    assert entry4.date == '2016-11-29'
    assert entry4.xdata == 'macmillan'
    assert entry4.publisher == 'Macmillan'
    assert entry4.location == 'New York and London'
    assert set(entry4.fields) == set([
        'author', 'title', 'date', 'xdata', 'publisher', 'location'
    ])


def test_uninheritance(test_entries):
    bibpy.inherit_xdata(test_entries)
    bibpy.uninherit_xdata(test_entries)

    entry1 = test_entries[0]
    assert entry1.publisher == 'Macmillan'
    assert entry1.fields == ['publisher']

    entry2 = test_entries[1]
    assert entry2.location == 'New York and London'
    assert entry2.fields == ['location']

    entry3 = test_entries[2]
    assert entry3.xdata == 'macmillan:name,macmillan:place'
    assert set(entry3.fields) == set(['xdata'])

    entry4 = test_entries[3]
    assert entry4.author == 'Author'
    assert entry4.title == 'Title'
    assert entry4.date == '2016-11-29'
    assert entry4.xdata == 'macmillan'
    assert set(entry4.fields) == set(['author', 'title', 'date', 'xdata'])


def test_no_entries():
    bibpy.inherit_xdata([])


def test_no_xdata(test_entries):
    bibpy.inherit_xdata([test_entries[-1]])
