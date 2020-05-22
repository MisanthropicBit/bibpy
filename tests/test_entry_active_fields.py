# -*- coding: utf-8 -*-

"""Test that fields set on entries are add/removed from its active fields."""

import bibpy
import bibpy.entry
import pytest
import random
import string


@pytest.fixture
def test_entry():
    return bibpy.entry.Entry(
        'article',
        'key',
        **{
            'author': 'Charles Darwin',
            'extra': 20
        }
    )


def test_entry_active_fields(test_entry):
    assert test_entry.author == 'Charles Darwin'
    assert test_entry.extra == 20
    assert set(test_entry.fields) == set(['author', 'extra'])

    test_entry.author = ''
    assert test_entry.author == ''
    assert test_entry.fields == ['extra']

    test_entry.author = 'Charles Darwin'
    test_entry.author = None
    assert test_entry.author is None
    assert test_entry.fields == ['extra']
    assert test_entry.extra_fields == ['extra']


def test_entry_extra_fields(test_entry):
    assert test_entry.author == 'Charles Darwin'
    assert test_entry.extra == 20
    assert set(test_entry.fields) == set(['author', 'extra'])

    test_entry.author = ''
    assert test_entry.author == ''
    assert test_entry.fields == ['extra']

    test_entry.author = 'Charles Darwin'
    test_entry.author = None
    test_entry.extra = ''
    assert test_entry.author is None
    assert test_entry.extra == ''
    assert test_entry.fields == []
    assert test_entry.extra_fields == []


def get_random_ascii_string():
    return random.sample(string.ascii_letters, random.randint(1, 10))


def test_all_fields():
    all_fields = dict(
        (field, ''.join(get_random_ascii_string()))
        for field in bibpy.fields.all
    )

    entry = bibpy.entry.Entry('article', 'key', **all_fields)

    for field, value in entry:
        assert field in entry.fields
