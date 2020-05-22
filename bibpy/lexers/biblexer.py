# -*- coding: utf-8 -*-

"""Lexer for bib(la)tex.

Port of the lexer from bibtex-ruby with a few changes. This lexer also supports
parentheses instead of braces for string, preamble and comment entries, e.g.
'@string(var = 1)' and generates tokens rather returning a list.

"""

from bibpy.lexers.base_lexer import BaseLexer


# A custom lexer is necessary as funcparserlib's lexing infrastructure is
# not up to the task of lexing bib(la)tex's somewhat complicated
# context-dependent structure like nested braces and comments.
class BibLexer(BaseLexer):
    """Lexer for generating bib tokens."""

    def __init__(self):
        """Initialise the lexer."""
        super().__init__()
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
            ('lbrace', (r'{',                    self.lex_lbrace)),
            ('rbrace', (r'}',                    self.lex_rbrace)),
            ('equals', (r'\s*(=)\s*',            None)),
            ('comma',  (r',',                    None)),
            ('number', (r'-?(0|([1-9][0-9]*))',  None)),
            ('name',   (r"[ ]*[\w\-:?'\.]+[ ]*", None)),
            ('entry',  (r'@',                    self.found_entry)),
            ('string', (r'"[^"]+"',              self.lex_string)),
            ('lparen', (r'\(',                   self.lex_lparen)),
            ('rparen', (r'\)',                   self.lex_rparen)),
            ('concat', (r'[ ]*#[ ]*',            None)),
            ('space',  (r'[ \t\r\n]+',           None)),
        ])

    def reset(self, string):
        """Reset the internal state of the lexer."""
        super().reset(string)
        self.in_entry = False

    def found_entry(self, value):
        """Handler for finding a bibliographic entry."""
        self.in_entry = True
        self.ignore_whitespace = True

        return self.make_token('entry', value)

    def lex_lbrace(self, value):
        """Lex a left brace."""
        self.brace_level += 1

        if self.brace_level == 1 and self.bibtype in ('comment', 'preamble'):
            self.mode = 'value'
        elif self.brace_level > 1:
            self.mode = 'value'

        return self.make_token('lbrace', value)

    def lex_rbrace(self, value):
        """Lex a right brace."""
        self.brace_level -= 1

        if self.brace_level == 0:
            self.in_entry = False
            self.mode = 'comment'
        elif self.brace_level < 0:
            raise self.raise_unbalanced()

        return self.make_token('rbrace', value)

    def lex_lparen(self, value):
        """Lex a left parenthesis."""
        if self.bibtype == 'string':
            self.mode = 'bib'
            self.ignore_whitespace = True
        elif self.bibtype in ('comment', 'preamble'):
            self.mode = 'parens'

        return self.make_token('lparen', value)

    def lex_rparen(self, value):
        """Lex a right parenthesis."""
        return self.make_token('rparen', value)

    def lex_parens(self):
        """Lex a set of possibly nested parentheses and its contents."""
        paren_level = 1
        content = ''

        while True:
            before, token = self.until('parens')

            if token == '(':
                paren_level += 1
                content += before + token
            elif token == ')':
                paren_level -= 1
                content += before

                if paren_level == 0:
                    yield self.make_token('content', content)
                    yield self.make_token('rparen', token)
                    self.mode = 'bib'
                    break

    def lex_braced(self):
        """Lex a possibly nested braced expression and its contents."""
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
                    self.bibtype = None
                    break
                elif self.brace_level == 1 and self.bibtype not in\
                        ('comment', 'string', 'preamble'):
                    yield self.make_token('content', content)
                    yield self.make_token('rbrace', token)
                    self.mode = 'bib'
                    break
                else:
                    content += token

    def lex_comment(self):
        """Lex a non-entry comment."""
        comment, entry = self.until('entry')

        if comment:
            yield self.make_token('comment', comment)

        if entry == '@':
            self.mode = 'entry'
            self.in_entry = True
            self.ignore_whitespace = True
            yield self.make_token('entry', entry)

    def lex_entry(self):
        """Lex a bibliographic entry."""
        self.brace_level = 0
        bibtype = self.expect('name')
        entry_type = bibtype.value.lower()

        if entry_type in ('comment', 'preamble', 'string'):
            self.bibtype = entry_type
        else:
            self.bibtype = 'entry'

        yield bibtype
        self.mode = 'bib'
        self.ignore_whitespace = True

    def lex_main(self):
        for _, token in self.scan(search_type='match'):
            if token is not None:
                yield token
            else:
                self.raise_error('Unmatched characters')
