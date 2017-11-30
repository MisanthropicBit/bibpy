"""Class for names split into its components (given name, family name etc.)."""

import bibpy.compat
import bibpy.lexers

__all__ = ('Name')


# A set of valid prefixes for name prefixes
_valid_prefixes = frozenset([
    "de",
    "da",
    "del",
    "della",
    "van",
    "von"
])


@bibpy.compat.unicode_compatibility
class Name(object):
    """Class containing the individual components of a name."""

    _lexer = bibpy.lexers.NameLexer()

    def __init__(self, first='', prefix='', last='', suffix=''):
        """Create a name consisting of first, prefix, last and suffix parts."""
        self._first = first
        self._prefix = prefix
        self._last = last
        self._suffix = suffix

    @staticmethod
    def fromstring(string):
        """Extract the name parts of a string name."""
        return bibpy.parser.parse_name(string)

    @property
    def first(self):
        """Return the first or given name."""
        return self._first

    @property
    def given(self):
        """Alias for self.first."""
        return self.first

    @property
    def prefix(self):
        """Return the prefix (e.g. 'von')."""
        return self._prefix

    @property
    def von(self):
        """Alias for self.prefix."""
        return self.prefix

    @property
    def last(self):
        """Return the last or family name."""
        return self._last

    @property
    def family(self):
        """Alias for self.last."""
        return self.last

    @property
    def suffix(self):
        """Return the suffix (e.g. 'Jr.')."""
        return self._suffix

    @property
    def junior(self):
        """Alias for self.suffix."""
        return self.suffix

    @property
    def parts(self):
        return [self.first, self.prefix, self.last, self.suffix]

    def format(self, style='first-last'):
        """Format the name using different styles. Default is 'first-last'.

        Consider the name 'John Smith' and its different styled formatings:
            * first-last => 'John Smith'
            * last-first => 'Smith, John'

        """
        if style == 'first-last':
            return "{0} {1} {2} {3}".format(self.first, self.prefix,
                                            self.last, self.suffix)

    def __eq__(self, other):
        if not isinstance(other, Name):
            return False

        return (self.first, self.prefix, self.last, self.suffix) ==\
            (other.first, other.prefix, other.last, other.suffix)

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return " ".join(self.parts)

    def __repr__(self):
        return "Name(first={0}, prefix={1}, last={2}, suffix={3})"\
            .format(self.first, self.prefix, self.last, self.suffix)

    def __unicode__(self):
        pass
