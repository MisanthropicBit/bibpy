# -*- coding: utf-8 -*-

"""bibpy errors."""


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
            .format(entry.entry_key, entry.entry_type)

        if required:
            s += "{0}".format(", ".join(required))

        if optional:
            if required:
                s += ", "

            s += "{0}".format(", ".join("/".join(e) for e in optional))

        super(RequiredFieldError, self).__init__(s)
        self.entry = entry
        self.required = required
        self.optional = optional
