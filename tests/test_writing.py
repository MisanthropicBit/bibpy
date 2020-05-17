"""Test writing functions."""

import bibpy
import os
import pytest
import tempfile


@pytest.fixture
def test_entries():
    return [bibpy.entry.Entry('article', 'key1', **{'author': 'Dave'}),
            bibpy.entry.String('var', '10')]


def test_write_string(test_entries):
    assert bibpy.write_string([]) == ''

    assert bibpy.write_string(test_entries) == """@article{key1,
    author = {Dave}
}

@string{var = "10"}"""


def test_write_file(test_entries):
    ntf = tempfile.NamedTemporaryFile(mode='r+', delete=False)

    bibpy.write_file(ntf, test_entries)

    with open(ntf.name) as fh:
        assert fh.read() == """@article{key1,
    author = {Dave}
}

@string{var = "10"}"""

    ntf.close()
    os.unlink(ntf.name)

    with tempfile.NamedTemporaryFile(mode='r+') as ntf:
        bibpy.write_file(ntf.name, test_entries)

        assert ntf.read() == """@article{key1,
    author = {Dave}
}

@string{var = "10"}"""
