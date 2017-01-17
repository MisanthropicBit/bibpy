"""Special date class for handling biblatex date ranges."""

import bibpy.parse
import datetime

__all__ = ('DateRange')


# NOTE: Implement comparison operators? How?
class DateRange(object):
    """Wrapper class around biblatex date ranges."""

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, start, end, open):
        """Create a date range with a start and/or end date."""
        self._start = start
        self._end = end
        self._open = open

    @staticmethod
    def fromstring(string):
        """Parse a date string then return a new DateRange object."""
        # Try to parse the date (ranges)
        dates = [list(map(int, d)) for d in bibpy.parse.parse_date(string)]

        # Provide missing information and create bibpy.date object
        dates = [datetime.date(*(d + [1] * (3 - len(d)))) for d in dates]

        return DateRange(dates[0] if dates else None,
                         dates[1] if len(dates) > 1 else None,
                         string.endswith('/'))

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
        if self.start is None and self.end is None:
            return ""

        s = self.start.strftime(self.DATE_FORMAT)

        if self.end:
            s += '/' + self.end.strftime(self.DATE_FORMAT)
        elif self.open:
            s += '/'

        return s

    def __repr__(self):
        return "DateRange(start={0}, end={1}, open={2})"\
            .format(
                self.start.strftime(self.DATE_FORMAT) if self.start else None,
                self.end.strftime(self.DATE_FORMAT) if self.end else None,
                self.open
            )
