# -*- coding: utf-8 -*-

"""Base class for all lexers."""

import re


class Token(object):
    """Class for lexer tokens.

    This class has been modified from funcparserlib.lexer.Token to allow the
    lexer classes to be used with pyparsing.

    """
    def __init__(self, type, value, start=None, end=None):
        self.type = type
        self.value = value
        self.start = start
        self.end = end

    def __repr__(self):
        return u'Token({0}, {1})'.format(self.type, self.value)

    def __eq__(self, other):
        # FIXME: Case sensitivity is assumed here
        return self.type == other.type and self.value == other.value

    def _pos_str(self):
        if self.start is None or self.end is None:
            return ''
        else:
            sl, sp = self.start
            el, ep = self.end
            return u'{0},{1}-{2},{3}:'.format(sl, sp, el, ep)

    def __str__(self):
        s = u"{0} {1} '{2}'".format(self._pos_str(), self.type, self.value)
        return s.strip()

    @property
    def name(self):
        return self.value

    def pformat(self):
        return u"{0} {1} '{2}'".format(self._pos_str().ljust(20),
                                       self.type.ljust(14),
                                       self.value)


class LexerError(ValueError):
    """General lexer error."""

    def __init__(self, msg, pos, char, lnum, brace_level, line):
        self.msg = msg
        self.pos = pos
        self.char = char
        self.lnum = lnum
        self.brace_level = brace_level
        self.line = line

    def __str__(self):
        return "Failed at line {0}, char {1}, position {2}, brace level {3}: "\
               "{4}"\
               .format(self.lnum, self.char, self.pos, self.brace_level,
                       self.msg)


class BaseLexer(object):
    """Base class for all lexers in bibpy."""

    def __init__(self):
        self._modes = {}
        self.patterns = None

    def reset(self, string):
        """Reset the internal state of the lexer."""
        self.pos = 0
        self.lastpos = 0
        self.maxpos = len(string)
        self.char = 1
        self.lnum = 1
        self.last_lnum = 1
        self.brace_level = 0
        self.ignore_whitespace = False
        self.string = string

    def _compile_regexes(self, patterns):
        # Save a copy of the patterns that respects the order. We could also
        # use a collections.OrderedDict, but this actually affected performance
        # ever so slighty
        self._iter_patterns = [(name, (re.compile(pattern, re.UNICODE), f))
                               for name, (pattern, f) in patterns]

        # This is used for lookups
        self.patterns = dict(self._iter_patterns)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value

    @property
    def modes(self):
        return self._modes

    @property
    def eos(self):
        """Return True if we have reached the end of the string."""
        return self.pos >= self.maxpos

    @property
    def current_char(self):
        """Return the current character or None if no such character."""
        if self.string and self.pos >= 0 and self.pos < len(self.string):
            return self.string[self.pos]

        return None

    def advance(self, match):
        """Advance the internal state based on a succesfull match."""
        self.lastpos = self.pos
        self.last_lnum = self.lnum

        matched = match.group(0)
        nls = matched.count('\n')
        self.pos = match.start(0) + len(matched)
        self.lnum += nls

        if nls == 0:
            self.char += len(matched)
        else:
            self.char = len(matched) - matched.rfind('\n') - 1

    def raise_error(self, msg):
        """Raise a lexer error with the given message."""
        raise LexerError(msg, self.pos, self.char, self.lnum, self.brace_level,
                         '')

    def raise_unexpected(self, token):
        """Raise an error for an unexpected token."""
        self.raise_error("Unexpected token '{0}'".format(token))

    def raise_unbalanced(self):
        """Raise an error for unbalanced braces."""
        self.raise_error("Unbalanced braces")

    def expect(self, token, strip_whitespace=True):
        """Expect a token, fail otherwise."""
        pattern, _ = self.patterns[token]
        m = pattern.search(self.string, self.pos)

        if not m:
            self.raise_unexpected(token)

        self.advance(m)
        token_value = m.group(0)

        if self.ignore_whitespace:
            token_value = token_value.strip()

        return self.make_token(token, token_value)

    def until(self, token):
        """Scan until a particular token is found."""
        if token == 'braces':
            pattern = re.compile('{|}')
        elif token == 'parens':
            pattern = re.compile('\(|\)')
        else:
            pattern, _ = self.patterns[token]

        m = pattern.search(self.string, self.pos)

        if m:
            scanned = m.group(0)
            self.advance(m)

            return self.string[self.lastpos:self.pos - 1], scanned
        else:
            rest = self.string[self.pos:]
            self.pos = len(self.string)

            return rest, ''

    def make_token(self, token_type, value):
        """Create a token of with a type and a value."""
        return Token(token_type, value, (self.last_lnum, self.lastpos),
                     (self.lnum, self.pos))

    def lex_string(self, value):
        return self.make_token('string', value)

    def lex_main(self):
        """Main internal lexer method."""
        for token_type, (pattern, handler) in self._iter_patterns:
            m = pattern.match(self.string, self.pos)

            if m:
                self.advance(m)
                value = m.group(0)

                if self.ignore_whitespace and token_type == 'space':
                    break

                if token_type != 'space':
                    value = value.strip()

                yield handler(value) if handler else\
                    self.make_token(token_type, value)

                break
        else:
            errline = self.string.splitlines()[self.lnum - 1]
            raise LexerError("Unmatched token at character {0}, line {1}"
                             .format(self.char, self.lnum),
                             self.pos, self.lnum, self.char, errline)

    def lex(self, string):
        """Generate tokens from a string."""
        self.reset(string)

        while not self.eos:
            for token in self.modes[self.mode]():
                yield token
