# -*- coding: utf-8 -*-

"""bibpy errors."""


class LexerException(Exception):
    """Raised on a lexer error."""

    pass


class ParseException(Exception):
    """Raised on errors in parsing."""

    pass


class RequiredFieldError(Exception):
    """Raised when an entry does not conform to a format's requirements."""

    def __init__(self, entry, required, optional):
        """Format a message for an entry's missing fields."""
        if not all(len(opt) == 2 for opt in optional):
            raise ValueError("Fields with options should have only two "
                             "options")

        s = "Entry '{0}' (type '{1}') is missing required field(s): "\
            .format(entry.bibkey, entry.bibtype)

        if required:
            s += "{0}".format(", ".join(required))

        if optional:
            if required:
                s += ", "

            s += "{0}".format(", ".join("/".join(e) for e in optional))

        super().__init__(s)
        self._entry = entry
        self._required = required
        self._optional = optional

    @property
    def entry(self):
        """The offending entry."""
        return self._entry

    @property
    def required(self):
        """Missing required fields."""
        return self._required

    @property
    def optional(self):
        """Missing fields where one of several fields are required."""
        return self._optional
