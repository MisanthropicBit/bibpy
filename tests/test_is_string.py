"""Test is_string function on Python 2 and 3."""

from bibpy.compat import is_string
import pytest
import sys


@pytest.mark.skipif(sys.version_info[0] < 3, reason="Only on Python 3.x")
def test_is_string_py3():
    assert is_string("This is a string")
    assert not is_string(20)
    assert not is_string(None)


@pytest.mark.skipif(sys.version_info[0] != 2, reason="Only on Python 2.x")
def test_is_string_py2():
    assert is_string("This is a string")
    assert not is_string(20)
    assert not is_string(None)
