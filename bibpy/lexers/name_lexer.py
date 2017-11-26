# -*- coding: utf-8 -*-

"""Custom bib(la)tex lexer for funcparserlib.

Port of the lexer from bibtex-ruby with a few changes. This lexer also supports
parentheses instead of braces for string, preamble and comment entries, e.g.
@string(var = 1) and generates tokens rather returning a list.

"""

from bibpy.compat import u
from bibpy.lexers.base_lexer import BaseLexer


class NameLexer(BaseLexer):
    """Lexer for generating name tokens from author names etc.

    Leading, trailing and consecutive whitespace are stripped.

    """

    def __init__(self):
        super(NameLexer, self).__init__()
        self.reset('')
        self.mode = 'normal'
        self._modes = {
            'normal': self.lex_name,
        }

        self._compile_regexes([('ws_or_braces',
                                (u('\s+|{|}|,'), None))])

    def reset(self, string):
        """Reset the internal state of the lexer."""
        super(NameLexer, self).reset(string)

        self.token_count = 0
        self._commas = 0

    @property
    def commas(self):
        """Return the indices of commas at brace-level zero."""
        return self._commas

    def _update_commas(self, token):
        if ',' in token:
            self.commas.append(self.token_count)

    def lex_name(self):
        """Lex a name and return its tokens."""
        part = []
        content = ''
        was_command = False

        while True:
            before, token = self.until('ws_or_braces')

            if not token:
                # We hit the end of the string
                if before:
                    part.append(self.make_token('content', before))

                yield self.make_token('part', part)
                break

            if token == '{':
                self.brace_level += 1
                content += before
                was_command = self.current_char == '\\'
            elif token == '}':
                self.brace_level -= 1

                if was_command:
                    was_command = False
                    content += before
                else:
                    if self.brace_level == 0:
                        content += before
                        part.append(self.make_token('braced', content))
                        content = ''
                    elif self.brace_level < 0:
                        self.raise_unbalanced()
            else:
                if self.brace_level > 0:
                    content += before + token
                else:
                    if token == ',':
                        self._commas += 1

                        if before:
                            part.append(self.make_token('content', before))

                        yield self.make_token('part', part)
                        part = []
                        content = ''
                    else:
                        # Token is whitespace
                        if before.strip():
                            if content:
                                part.append(self.make_token('content',
                                            content + before.strip()))
                                content = ''
                            else:
                                part.append(self.make_token('content',
                                                            before.strip()))
