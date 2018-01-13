# -*- coding: utf-8 -*-

"""Lexer for splitting names on zero brace-level 'and'."""

from bibpy.compat import u
from bibpy.lexers.base_lexer import BaseLexer


class NamelistLexer(BaseLexer):
    """Lexer for splitting names on zero brace-level 'and'."""

    def __init__(self):
        super(NamelistLexer, self).__init__()
        self.reset('')
        self.mode = 'normal'
        self._modes = {
            'normal': self.lex_namelist,
        }

        self._compile_regexes([('braces',    (u('{|}'), None)),
                               ('delimiter', (u('\\band\\b'), None))])

    def reset(self, string):
        """Reset the internal state of the lexer."""
        super(NamelistLexer, self).reset(string)

    def lex_namelist(self):
        """Lex a list of names, preserving braces for later name parsing."""
        content = ''

        for before, token in self.scan():
            if token == '{':
                self.brace_level += 1
                content += before + token
            elif token == '}':
                self.brace_level -= 1
                content += before + token

                if self.brace_level < 0:
                    self.raise_unbalanced()
            elif token == 'and':
                if self.brace_level > 0:
                    content += before + token
                else:
                    yield (content + before).strip()
                    content = ''
            else:
                assert token is None
                yield (content + before).strip()
