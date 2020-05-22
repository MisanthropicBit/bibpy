# -*- coding: utf-8 -*-

"""Test parsing of dates and date ranges."""

from bibpy.date import DateRange
from bibpy.parser import parse_date
from bibpy.error import ParseException, LexerException
import pytest


def test_date_fails():
    """Test that the parse fails on invalid dates."""
    with pytest.raises(ParseException):
        parse_date('20-20')

    with pytest.raises(ParseException):
        parse_date('202034-02')

    with pytest.raises(LexerException):
        parse_date('@@@@-20')


def test_single_dates():
    """Test parsing of singular dates."""
    assert parse_date('1850') ==\
        DateRange(('1850', None, None), (None, None, None), False)

    assert parse_date('1967-02') ==\
        DateRange(('1967', '02', None), (None, None, None), False)

    assert parse_date('2009-01-31') ==\
        DateRange(('2009', '01', '31'), (None, None, None), False)


def test_date_ranges():
    """Test parsing of date ranges."""
    assert parse_date('1997/') ==\
        DateRange(('1997', None, None), (None, None, None), True)

    assert parse_date('1988/1992') ==\
        DateRange(('1988', None, None), ('1992', None, None), False)

    assert parse_date('2002-01/2002-02') ==\
        DateRange(('2002', '01', None), ('2002', '02', None), False)

    assert parse_date('1995-03-30/1995-04-05') ==\
        DateRange(('1995', '03', '30'), ('1995', '04', '05'), False)
