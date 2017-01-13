"""Test parsing of dates and date ranges."""

import bibpy.parse


def test_date_fails():
    """Test that the parse fails on invalid dates."""
    pass


def test_single_dates():
    """Test parsing of singular dates."""
    assert bibpy.parse.parse_date('1850') == [['1850']]
    assert bibpy.parse.parse_date('1967-02') == [['1967', '02']]
    assert bibpy.parse.parse_date('2009-01-31') == [['2009', '01', '31']]


def test_date_ranges():
    """Test parsing of date ranges."""
    assert bibpy.parse.parse_date('1997/') == [['1997']]
    assert bibpy.parse.parse_date('1988/1992') == [['1988'], ['1992']]
    assert bibpy.parse.parse_date('2002-01/2002-02') == [['2002', '01'],
                                                         ['2002', '02']]
    assert bibpy.parse.parse_date('1995-03-30/1995-04-05') ==\
        [['1995', '03', '30'], ['1995', '04', '05']]
