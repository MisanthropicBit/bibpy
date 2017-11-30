"""Test compatibility functions on Python 2 and 3."""

from bibpy.compat import is_string, u
import pytest
import sys


@pytest.mark.skipif(sys.version_info[0] < 3, reason="Requires Python 3.x")
def test_is_string_py3():
    assert is_string("This is a string")
    assert not is_string(20)
    assert not is_string(None)


@pytest.mark.skipif(sys.version_info[0] > 2, reason="Requires Python 2.x")
def test_is_string_py2():
    assert is_string("This is a string")
    assert not is_string(20)
    assert not is_string(None)


@pytest.mark.skipif(sys.version_info[0] < 3, reason="Requires Python 3.x")
def test_unicode_py3():
    assert isinstance(u('Some text'), str)
    assert isinstance(u(u'Some text'), str)
    assert isinstance(u(b'Some text'), bytes)


@pytest.mark.skipif(sys.version_info[0] > 2, reason="Requires Python 2.x")
def test_unicode_py2():
    assert isinstance(u('Some text'), unicode)
    assert isinstance(u(u'Some text'), unicode)
    assert isinstance(u(b'Some text'), unicode)
