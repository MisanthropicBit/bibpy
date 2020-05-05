# -*- coding: utf-8 -*-

"""Special date class for handling biblatex date ranges."""

import bibpy.parser

__all__ = ('DateRange', 'PartialDate')


class PartialDate:
    """Light-weight class for representing partial dates."""

    def __init__(self, year=None, month=None, day=None):
        self.year = year if year is None else int(year)
        self.month = month if month is None else int(month)
        self.day = day if day is None else int(day)

        if self.year and self.year < 0:
            raise ValueError("Year must be positive")

        if self.month and (self.month < 1 or self.month > 12):
            raise ValueError("Month not in range")

        if self.day and (self.day < 1 or self.day > 31):
            raise ValueError("Day not in range")

    def __str__(self):
        s = str(self.year) if self.year else ""
        s += "-" + "{0:02d}".format(self.month) if self.month else ""
        s += "-" + "{0:02d}".format(self.day) if self.day else ""

        return s

    def __eq__(self, other):
        return isinstance(other, PartialDate) and self.year == other.year\
            and self.month == other.month and self.day == other.day

    def __bool__(self):
        return any(e is not None for e in [self.year, self.month, self.day])


# NOTE: Implement comparison operators? How?
class DateRange:
    """Wrapper class around biblatex date ranges."""

    def __init__(self, start, end, open):
        """Create a date range with a start and/or end date."""
        self._start = PartialDate(*start)
        self._end = PartialDate(*end)
        self._open = open

    @staticmethod
    def fromstring(string):
        """Parse a date string then return a new DateRange object."""
        # Try to parse the date (ranges)
        return bibpy.parser.parse_date(string)

    @property
    def start(self):
        """Return the start date of the range, None otherwise."""
        return self._start

    @property
    def end(self):
        """Return the end date of the range, None otherwise."""
        return self._end

    @property
    def open(self):
        """Return True if this date range is open-ended.

        Biblatex open-ended dates are formatted like this:
        '1988-01-12/'

        """
        return self._open

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.start == other.start and self.end == other.end and\
                self.open == other.open

        return False

    def __str__(self):
        if not self.start and not self.end:
            return ""

        s = str(self.start)

        if self.end:
            s += '/' + str(self.end)
        elif self.open:
            s += '/'

        return s

    def __repr__(self):
        return "DateRange(start={0}, end={1}, open={2})"\
            .format(self.start or None, self.end or None, self.open)
