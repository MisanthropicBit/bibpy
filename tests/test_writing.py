"""Test writing functions."""

import bibpy
import pytest


@pytest.fixture
def test_entries():
    return [bibpy.entry.Entry('article', 'key1', **{'author': 'Dave'}),
            bibpy.entry.String('var', '10')]


def test_write_string(test_entries):
    assert bibpy.write_string('') == ''

    assert bibpy.write_string(test_entries) == """@article{key1,
    author = {Dave}
}

@string{var = "10"}"""
