"""Test entry formatting and printing."""

import bibpy
import pytest


# Use a predefined order until we can fix arbitrary ordering
_PRESET_ORDER = ['author', 'title', 'year', 'month', 'institution']


@pytest.fixture
def test_entries():
    return bibpy.read_file('tests/data/simple_1.bib', 'biblatex').entries


def test_formatting(test_entries):
    print(test_entries[0].format())

    assert test_entries[0].format(align=True, indent='    ',
                                  order=_PRESET_ORDER) ==\
        """@article{test,
    author      = {James Conway and Archer Sterling},
    title       = {1337 Hacker},
    year        = {2010},
    month       = {4},
    institution = {Office of Information Management {and} Communications}
}"""

    assert test_entries[1].format(align=True, indent='    ', order=[]) ==\
        """@conference{lol,
    author = {k}
}"""


def test_align(test_entries):
    assert test_entries[0].format(align=False, indent='    ',
                                  order=_PRESET_ORDER) ==\
        """@article{test,
    author = {James Conway and Archer Sterling},
    title = {1337 Hacker},
    year = {2010},
    month = {4},
    institution = {Office of Information Management {and} Communications}
}"""


@pytest.mark.skip
def test_indent(test_entries, monkeypatch):
    # Set PYTHONHASHSEED to zero for Python 3+ to ensure predictable ordering
    # of Python's dictionary
    monkeypatch.setenv('PYTHONHASHSEED', 0)

    assert test_entries[0].format(align=True, indent='', order=[]) ==\
        """@article{test,
month       = {4},
title       = {1337 Hacker},
institution = {Office of Information Management {and} Communications},
year        = {2010},
author      = {James Conway and Archer Sterling}
}"""

    assert test_entries[0].format(align=True, indent=' ' * 9, order=[]) ==\
        """@article{test,
         month       = {4},
         title       = {1337 Hacker},
         institution = {Office of Information Management {and} Communications},
         year        = {2010},
         author      = {James Conway and Archer Sterling}
}"""


def test_ordering(test_entries, monkeypatch):
    for fail in ('string', 0.453245, object()):
        with pytest.raises(ValueError):
            test_entries[0].format(order=fail)

    # Print a predefined order
    order = ['author', 'title', 'year', 'institution', 'month']

    assert test_entries[0].format(align=True, indent='    ', order=order) ==\
        """@article{test,
    author      = {James Conway and Archer Sterling},
    title       = {1337 Hacker},
    year        = {2010},
    institution = {Office of Information Management {and} Communications},
    month       = {4}
}"""

    # Print fields as sorted
    assert test_entries[0].format(align=True, indent='    ', order=True) ==\
        """@article{test,
    author      = {James Conway and Archer Sterling},
    institution = {Office of Information Management {and} Communications},
    month       = {4},
    title       = {1337 Hacker},
    year        = {2010}
}"""
