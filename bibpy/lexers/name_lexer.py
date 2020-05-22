# -*- coding: utf-8 -*-

"""Bib(la)tex lexer for names."""

from bibpy.lexers.base_lexer import BaseLexer


class NameLexer(BaseLexer):
    """Lexer that splits names into parts.

    Any whitespace is stripped.

    """

    def __init__(self):
        """Initialise the lexer."""
        super().__init__()
        self.reset('')
        self.mode = 'normal'
        self._modes = {
            'normal': self.lex_name,
        }

        self._compile_regexes([
            ('ws_or_braces', (r'\s+|{|}|,', None))
        ])

    def reset(self, string):
        """Reset the internal state of the lexer."""
        super().reset(string)
        self._commas = 0

    @property
    def commas(self):
        """Return the indices of commas found at brace-level zero."""
        return self._commas

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
                                part.append(
                                    self.make_token(
                                        'content',
                                        content + before.strip()
                                    )
                                )
                                content = ''
                            else:
                                part.append(
                                    self.make_token('content', before.strip())
                                )
