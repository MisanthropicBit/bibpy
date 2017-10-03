"""Test the bibpy.date.DateRange class."""

from bibpy.date import DateRange
import bibpy.error
import pytest


def test_creation():
    """Test creation of DateRanges."""
    d = DateRange((None, None, None), (None, None, None), False)

    assert str(d) == ''
    assert repr(d) == 'DateRange(start=None, end=None, open=False)'


def test_fromstring():
    """Test creating DateRanges from the static fromstring method."""
    # Single date
    s = '1988-01-12'
    d = DateRange.fromstring(s)
    assert d.start == bibpy.date.PartialDate(1988, 1, 12)
    assert not d.end
    assert not d.open
    assert str(d) == s
    assert repr(d) == 'DateRange(start=1988-01-12, end=None, open=False)'

    # Date range
    s = '1988-01-12/2016-12-31'
    d = DateRange.fromstring(s)
    assert d.start == bibpy.date.PartialDate(1988, 1, 12)
    assert d.end == bibpy.date.PartialDate(2016, 12, 31)
    assert not d.open
    assert str(d) == s
    assert repr(d) == 'DateRange(start=1988-01-12, end=2016-12-31, open=False)'

    # Open-ended date range
    s = '1988-01-12/'
    d = DateRange.fromstring(s)
    assert d.start == bibpy.date.PartialDate(1988, 1, 12)
    assert not d.end
    assert d.open
    assert str(d) == s
    assert repr(d) == 'DateRange(start=1988-01-12, end=None, open=True)'

    # Date with a missing day
    s = '1988-01'
    d = DateRange.fromstring(s)
    assert d.start == bibpy.date.PartialDate(1988, 1, None)
    assert not d.end
    assert not d.open
    assert str(d) == '1988-01'
    assert repr(d) == 'DateRange(start=1988-01, end=None, open=False)'


def test_wrong_format():
    with pytest.raises(ValueError):
        # Month is invalid
        DateRange.fromstring('2016-31-12')

    with pytest.raises(bibpy.error.ParseException):
        # Format should be 'YYYY-MM-DD'
        DateRange.fromstring('31-12-2016')

    with pytest.raises(bibpy.error.ParseException):
        # Date ranges can only be open-ended relative to a start date
        DateRange.fromstring('/2016-12-31')


def test_properties():
    date1 = DateRange.fromstring('2017-01-05')
    date2 = DateRange.fromstring('2017-01-05')
    date3 = DateRange.fromstring('2016-12-30')

    assert date1 == date2
    assert date1 != date3
    assert date1 != "abc"
    assert not date1 == map
