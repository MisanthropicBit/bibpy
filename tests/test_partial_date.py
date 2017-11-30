"""Test the bibpy.date.PartialDate class."""

from bibpy.date import PartialDate
import pytest
import sys


def test_creation():
    pd1 = PartialDate(2017, 11, 29)
    assert pd1.year == 2017
    assert pd1.month == 11
    assert pd1.day == 29


def test_incorrect_input():
    with pytest.raises(ValueError):
        PartialDate(-3, 11, 29)

    with pytest.raises(ValueError):
        PartialDate(2017, 13, 29)

    with pytest.raises(ValueError):
        PartialDate(2017, 11, 32)


@pytest.mark.skipif(sys.version_info[0] != 2, reason="requires python 2")
def test_properties_py2():
    pd1 = PartialDate(2017, 11, 29)
    pd2 = PartialDate()

    assert bool(pd1)
    assert not bool(pd2)


@pytest.mark.skipif(sys.version_info[0] != 3, reason="requires python 3")
def test_properties_py3():
    pd1 = PartialDate(2017, 11, 29)
    pd2 = PartialDate()

    assert bool(pd1)
    assert not bool(pd2)
