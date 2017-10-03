"""Test parsing of dates and date ranges."""

import bibpy.date
from bibpy.parser import parse_date


def test_date_fails():
    """Test that the parse fails on invalid dates."""
    pass


def test_single_dates():
    """Test parsing of singular dates."""
    assert parse_date('1850') ==\
        bibpy.date.DateRange(('1850', None, None), (None, None, None), False)

    assert parse_date('1967-02') ==\
        bibpy.date.DateRange(('1967', '02', None), (None, None, None), False)

    assert parse_date('2009-01-31') ==\
        bibpy.date.DateRange(('2009', '01', '31'), (None, None, None), False)


def test_date_ranges():
    """Test parsing of date ranges."""
    assert parse_date('1997/') ==\
        bibpy.date.DateRange(('1997', None, None), (None, None, None), True)

    assert parse_date('1988/1992') ==\
        bibpy.date.DateRange(('1988', None, None), ('1992', None, None), False)

    assert parse_date('2002-01/2002-02') ==\
        bibpy.date.DateRange(('2002', '01', None), ('2002', '02', None), False)

    assert parse_date('1995-03-30/1995-04-05') ==\
        bibpy.date.DateRange(('1995', '03', '30'), ('1995', '04', '05'), False)
