# -*- coding: utf-8 -*-

"""Custom bib(la)tex lexer for funcparserlib.

Port of the lexer from bibtex-ruby with a few changes. This lexer also supports
parentheses instead of braces for string, preamble and comment entries, e.g.
@string(var = 1) and generates tokens rather returning a list.

"""

import funcparserlib.lexer as lexer
import re


class LexerError(ValueError):
    """General lexer error."""

    def __init__(self, msg, pos, char, lnum):
        self.msg = msg
        self.pos = pos
        self.char = char
        self.lnum = lnum

    def __str__(self):
        return "Failed at line {0}, char {1}, position {2}"\
            .format(self.lnum, self.char, self.pos)


class BibLexer(object):
    """Lexer for generating bib tokens.

    A custom lexer is necessary as funcparserlib's lexing infrastructure is not
    up to the task of lexing bib(la)tex's somewhat complicated
    context-dependent structure like nested braces and comments.

    """

    def __init__(self):
        self.reset('')

        self._modes = {
            'bib':     self.lex_main,
            'entry':   self.lex_entry,
            'value':   self.lex_braced,
            'parens':  self.lex_parens,
            'comment': self.lex_comment
        }

    def reset(self, string):
        """Reset the internal state of the lexer."""
        self.mode = 'comment'
        self.in_entry = False
        self.pos = 0
        self.lastpos = 0
        self.maxpos = len(string)
        self.char = 1
        self.lnum = 1
        self.last_lnum = 1
        self.brace_level = 0
        self.string = string
        self.ignore_whitespace = True

        self.patterns = dict([(name, (re.compile(pattern, re.UNICODE), f))
                              for name, (pattern, f) in [
            ('lbrace',    (u'{', self.lex_lbrace)),
            ('rbrace',    (u'}', self.lex_rbrace)),
            ('equals',    (u'\s*(=)\s*', None)),
            ('comma',     (u',', None)),
            ('number',    (u'-?(0|([1-9][0-9]*))', None)),
            ('name',      (u'\s*[\w\-:?\'\.]+\s*', None)),
            ('entry',     (u'@', self.found_entry)),
            ('string',    (u'"[^"]+"', self.lex_string)),
            ('lparen',    (u'\(', self.lex_lparen)),
            ('rparen',    (u'\)', self.lex_rparen)),
            ('concat',    (u'#', None)),
            ('space',     (u'[ \t\r\n]+', None)),
        ]])

    def eos(self):
        """Return True if we have reached the end of the string."""
        return self.pos >= self.maxpos

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

    def unexpected(self, token):
        """Raise an error for an unexpected token."""
        raise LexerError("Unexpected token '{0}' at character {1}, line {2}"
                         .format(token, self.char, self.lnum),
                         self.pos, self.char, self.lnum)

    def unbalanced(self):
        """Raise an error for unbalanced braces."""
        raise LexerError("Unbalanced braces at character {0}, line {1}"
                         .format(self.char, self.lnum), self.pos, self.lnum)

    def expect(self, token, strip_whitespace=True):
        """Expect a token, fail otherwise."""
        pattern, _ = self.patterns[token]
        m = pattern.search(self.string, self.pos)

        if not m:
            self.unexpected(token)

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
        return lexer.Token(token_type, value,
                           (self.last_lnum, self.lastpos),
                           (self.lnum, self.pos))

    def found_entry(self, value):
        self.in_entry = True
        self.ignore_whitespace = True

        return self.make_token('entry', value)

    def lex_string(self, value):
        return self.make_token('string', value)

    def lex_lbrace(self, value):
        self.brace_level += 1

        if self.brace_level == 1 and self.entry_type in ('comment',
                                                         'preamble'):
            self.mode = 'value'
        elif self.brace_level > 1:
            self.mode = 'value'

        return self.make_token("lbrace", value)

    def lex_rbrace(self, value):
        self.brace_level -= 1

        if self.brace_level == 0:
            self.in_entry = False
            self.mode = 'comment'
        elif self.brace_level < 0:
            raise self.unbalanced()

        return self.make_token('rbrace', value)

    def lex_lparen(self, value):
        if self.entry_type in ('string'):
            self.mode = 'bib'
            self.ignore_whitespace = True
        elif self.entry_type in ('comment', 'preamble'):
            self.mode = 'parens'

        return self.make_token('lparen', value)

    def lex_rparen(self, value):
        return self.make_token('rparen', value)

    def lex_parens(self):
        paren_level = 1

        while True:
            before, token = self.until('parens')

            if token == '(':
                paren_level += 1
                yield self.make_token('content', before)
                yield self.make_token('lparen', token)
            elif token == ')':
                paren_level -= 1
                yield self.make_token('content', before)
                yield self.make_token('rparen', token)

                if paren_level == 0:
                    self.mode = 'bib'
                    break

    def lex_braced(self):
        content = ''

        while True:
            before, token = self.until('braces')

            if token == '{':
                self.brace_level += 1
                content += before + token
                # yield self.make_token('content', before)
                # yield self.make_token('lbrace', token)
            elif token == '}':
                self.brace_level -= 1
                content += before
                # yield self.make_token('content', before)

                if self.brace_level == 0:
                    yield self.make_token('content', content)
                    yield self.make_token('rbrace', token)
                    self.in_entry = False
                    self.ignore_whitespace = False
                    self.mode = 'comment'
                    self.entry_type = None
                    break
                elif self.brace_level == 1 and self.entry_type not in\
                        ('comment', 'string', 'preamble'):
                    yield self.make_token('content', content)
                    yield self.make_token('rbrace', token)
                    self.mode = 'bib'
                    break
                elif self.brace_level < 0:
                    self.unbalanced()
                else:
                    content += token
                    # yield self.make_token('rbrace', token)

    def lex_main(self):
        for token_type, (pattern, handler) in self.patterns.items():
            m = pattern.match(self.string, self.pos)

            if m:
                self.advance(m)
                value = m.group(0)

                if self.ignore_whitespace and token_type == 'space':
                    break

                if token_type != 'space':
                    value = value.strip()

                if handler:
                    yield handler(value)
                else:
                    yield lexer.Token(token_type, value,
                                      (self.last_lnum, self.lastpos),
                                      (self.lnum, self.pos))

                break
        else:
            # errline = self.string.splitlines()[self.lnum - 1]
            raise LexerError("Unmatched token at character {0}, line {1}"
                             .format(self.char, self.lnum),
                             self.pos, self.lnum, self.char)

    def lex_comment(self):
        comment, entry = self.until('entry')

        if comment:
            yield self.make_token('comment', comment)

        if entry == '@':
            self.mode = 'entry'
            self.in_entry = True
            self.ignore_whitespace = True
            yield self.make_token('entry', entry)

    def lex_entry(self):
        self.brace_level = 0
        entry_type = self.expect('name')

        if entry_type.value == 'comment':
            self.entry_type = 'comment'
        elif entry_type.value == 'string':
            self.entry_type = 'string'
        elif entry_type.value == 'preamble':
            self.entry_type = 'preamble'
        else:
            self.entry_type = 'entry'

        yield entry_type
        self.mode = 'bib'
        self.ignore_whitespace = True

    def lex(self, string):
        """Generate tokens from a string."""
        self.reset(string)

        while not self.eos():
            for token in self._modes[self.mode]():
                yield token
