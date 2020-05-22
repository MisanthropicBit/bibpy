# -*- coding: utf-8 -*-

"""Base class for all lexers."""

import re
from funcparserlib.lexer import Token


class LexerError(Exception):
    """General lexer error."""

    def __init__(self, msg, pos, char, lnum, brace_level, line):
        """Initialise with information on where the error occurred."""
        self.msg = msg
        self.pos = pos
        self.char = char
        self.lnum = lnum
        self.brace_level = brace_level
        self.line = line

    def __str__(self):
        return "Failed at line {0}, char '{1}', position {2}, "\
            "brace level {3}: {4} (line: '{5}')"\
            .format(
                self.lnum,
                self.char,
                self.pos,
                self.brace_level,
                self.msg,
                self.line,
            )


class BaseLexer:
    """Base class for all bibpy lexers."""

    def __init__(self):
        """Initialise the lexer."""
        self._modes = {}
        self._patterns = None

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
        """Compile a set of patterns into regular expressions."""
        # Save a copy of the patterns that respects the order. We could also
        # use a collections.OrderedDict, but this actually affected performance
        # ever so slighty
        self._iter_patterns = [
            (name, (re.compile(pattern), f)) for name, (pattern, f) in patterns
        ]

        # This is used for lookups
        self._patterns = dict(self._iter_patterns)

    @property
    def patterns(self):
        """All patterns recognised by the lexer."""
        return self._patterns

    @property
    def mode(self):
        """Return the current mode of the lexer."""
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value

    @property
    def modes(self):
        """Return all modes that the lexer has."""
        return self._modes

    @property
    def eos(self):
        """Return True if we have reached the end of the string."""
        return self.pos >= self.maxpos

    @property
    def current_char(self):
        """Return the current character or None if no such character."""
        if self.string and self.pos >= 0 and not self.eos:
            return self.string[self.pos]

        return None

    def advance(self, match):
        """Advance the internal state based on a successful match."""
        self.lastpos = self.pos
        self.last_lnum = self.lnum

        matched = match.group(0)
        newlines = matched.count('\n')
        self.pos = match.start(0) + len(matched)
        self.lnum += newlines

        if newlines == 0:
            self.char += len(matched)
        else:
            self.char = len(matched) - matched.rfind('\n') - 1

    def raise_error(self, msg):
        """Raise a lexer error with the given message."""
        errline = self.string.splitlines()[self.lnum - 1]

        raise LexerError(
            msg, self.pos, self.char, self.lnum, self.brace_level, errline
        )

    def raise_unexpected(self, token):
        """Raise an error for an unexpected token."""
        self.raise_error("Did not find expected token '{0}'".format(token))

    def raise_unbalanced(self):
        """Raise an error for unbalanced braces."""
        self.raise_error('Unbalanced braces')

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
        """Scan until a particular token is found.

        Return the part of the string that was scanned past and the string
        value of the token. The latter is the entire rest of the string if the
        token was not found.

        """
        if token == 'braces':
            pattern = re.compile(r'{|}')
        elif token == 'parens':
            pattern = re.compile(r'\(|\)')
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
        """Create a token type with a value."""
        return Token(
            token_type,
            value,
            (self.last_lnum, self.lastpos),
            (self.lnum, self.pos)
        )

    def lex_string(self, value):
        """Lex a string and return a single token for it."""
        return self.make_token('string', value)

    def scan(self, search_type='search'):
        """Scan until any token recognised by this lexer is found.

        Return the part of the string that was scanned past and the token
        itself. The latter is the entire rest of the string if the token was
        not found.

        """
        for token_type, (pattern, handler) in self._iter_patterns:
            # Not the most elegant but re.Pattern only exists in Python 3.7+ so
            # we cannot pass the method as an argument
            m = getattr(pattern, search_type)(self.string, self.pos)

            if m:
                self.advance(m)
                value = m.group(0)

                if self.ignore_whitespace and token_type == 'space':
                    break

                token = handler(value) if handler else\
                    self.make_token(token_type, value)

                yield self.string[self.lastpos:self.pos - len(value)], token
                break
        else:
            rest = self.string[self.pos:]
            self.pos = len(self.string)

            yield rest, None

    def lex(self, string):
        """Lex a string and generate tokens."""
        self.reset(string)

        while not self.eos:
            yield from self.modes[self.mode]()
