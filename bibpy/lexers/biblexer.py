# -*- coding: utf-8 -*-

"""Custom bib(la)tex lexer for funcparserlib.

Port of the lexer from bibtex-ruby with a few changes. This lexer also supports
parentheses instead of braces for string, preamble and comment entries, e.g.
@string(var = 1) and generates tokens rather returning a list.

"""

from bibpy.lexers.base_lexer import BaseLexer


class BibLexer(BaseLexer):
    """Lexer for generating bib tokens.

    A custom lexer is necessary as funcparserlib's lexing infrastructure is not
    up to the task of lexing bib(la)tex's somewhat complicated
    context-dependent structure like nested braces and comments.

    """

    def __init__(self):
        super(BibLexer, self).__init__()
        self.reset('')
        self.mode = 'comment'

        self._modes = {
            'bib':     self.lex_main,
            'entry':   self.lex_entry,
            'value':   self.lex_braced,
            'parens':  self.lex_parens,
            'comment': self.lex_comment
        }

        self._compile_regexes([
            ('lbrace',    (u'{', self.lex_lbrace)),
            ('rbrace',    (u'}', self.lex_rbrace)),
            ('equals',    (u'\s*(=)\s*', None)),
            ('comma',     (u',', None)),
            ('number',    (u'-?(0|([1-9][0-9]*))', None)),
            ('name',      (ur"\s*[\w\-:?'\.]+\s*", None)),
            ('entry',     (u'@', self.found_entry)),
            ('string',    (u'"[^"]+"', self.lex_string)),
            ('lparen',    (u'\(', self.lex_lparen)),
            ('rparen',    (u'\)', self.lex_rparen)),
            ('concat',    (u'#', None)),
            ('space',     (u'[ \t\r\n]+', None)),
        ])

    def reset(self, string):
        """Reset the internal state of the lexer."""
        super(BibLexer, self).reset(string)
        self.in_entry = False

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

        return self.make_token('lbrace', value)

    def lex_rbrace(self, value):
        self.brace_level -= 1

        if self.brace_level == 0:
            self.in_entry = False
            self.mode = 'comment'
        elif self.brace_level < 0:
            raise self.raise_unbalanced()

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
            elif token == '}':
                self.brace_level -= 1
                content += before

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
                    self.raise_unbalanced()
                else:
                    content += token

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
