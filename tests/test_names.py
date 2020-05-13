# -*- coding: utf-8 -*-

"""Test extraction of parts of names."""

import bibpy.name
from bibpy.lexers.base_lexer import LexerError
import pytest
import sys


def name_from_string(s):
    return bibpy.name.Name.fromstring(s)


def test_zero_comma_names():
    name = name_from_string('')
    assert name.first == name.given == ''
    assert name.prefix == name.von == ''
    assert name.last == name.family == ''
    assert name.suffix == name.junior == ''

    name = name_from_string('Louise')
    assert name.first == name.given == ''
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Louise'
    assert name.suffix == name.junior == ''

    name = name_from_string('louise')
    assert name.first == name.given == ''
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'louise'
    assert name.suffix == name.junior == ''

    name = name_from_string('Catherine Crook de Camp')
    assert name.first == name.given == 'Catherine Crook'
    assert name.prefix == name.von == 'de'
    assert name.last == name.family == 'Camp'
    assert name.suffix == name.junior == ''

    name = name_from_string('Jean de la Fontaine du Bois Joli')
    assert name.first == name.given == 'Jean'
    assert name.prefix == name.von == 'de la Fontaine du'
    assert name.last == name.family == 'Bois Joli'
    assert name.suffix == name.junior == ''

    name = name_from_string('Jean de La Fontaine Du Bois Joli')
    assert name.first == name.given == 'Jean'
    assert name.prefix == name.von == 'de'
    assert name.last == name.family == 'La Fontaine Du Bois Joli'
    assert name.suffix == name.junior == ''

    name = name_from_string('jean de la fontaine du bois joli')
    assert name.first == name.given == ''
    assert name.prefix == name.von == 'jean de la fontaine du bois'
    assert name.last == name.family == 'joli'
    assert name.suffix == name.junior == ''

    name = name_from_string('Jean {de} la fontaine')
    assert name.first == name.given == 'Jean de'
    assert name.prefix == name.von == 'la'
    assert name.last == name.family == 'fontaine'
    assert name.suffix == name.junior == ''

    name = name_from_string('jean {de} {la} fontaine')
    assert name.first == name.given == ''
    assert name.prefix == name.von == 'jean'
    assert name.last == name.family == 'de la fontaine'
    assert name.suffix == name.junior == ''

    name = name_from_string('Jean {de} {la} fontaine')
    assert name.first == name.given == 'Jean de la'
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'fontaine'
    assert name.suffix == name.junior == ''

    name = name_from_string('Jean De La Fontaine')
    assert name.first == name.given == 'Jean De La'
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Fontaine'
    assert name.suffix == name.junior == ''

    name = name_from_string('jean De la Fontaine')
    assert name.first == name.given == ''
    assert name.prefix == name.von == 'jean De la'
    assert name.last == name.family == 'Fontaine'
    assert name.suffix == name.junior == ''

    name = name_from_string('Jean de La Fontaine')
    assert name.first == name.given == 'Jean'
    assert name.prefix == name.von == 'de'
    assert name.last == name.family == 'La Fontaine'
    assert name.suffix == name.junior == ''

    name = name_from_string('Kim Stanley Robinson')
    assert name.first == name.given == 'Kim Stanley'
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Robinson'
    assert name.suffix == name.junior == ''

    name = name_from_string('Michael {Marshall Smith}')
    assert name.first == name.given == 'Michael'
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Marshall Smith'
    assert name.suffix == name.junior == ''

    name = name_from_string('Louis-Albert')
    assert name.first == name.given == ''
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Louis-Albert'
    assert name.suffix == name.junior == ''

    name = name_from_string(u'Charles Louis Xavier Joseph de la '
                            u'Vall{\’e}e Poussin')
    assert name.first == name.given == u'Charles Louis Xavier Joseph'
    assert name.prefix == name.von == u'de la'
    assert name.last == name.family == u'Vall\’ee Poussin'
    assert name.suffix == name.junior == u''

    name = name_from_string('John Smith')
    assert name.first == name.given == 'John'
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Smith'
    assert name.suffix == name.junior == ''

    name = name_from_string('J. R. R. Tolkien')
    assert name.first == name.given == 'J. R. R.'
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Tolkien'
    assert name.suffix == name.junior == ''

    name = name_from_string('Jean Baptiste-Poquelin')
    assert name.first == name.given == 'Jean'
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Baptiste-Poquelin'
    assert name.suffix == name.junior == ''

    name = name_from_string('Jean-Baptiste-Poquelin')
    assert name.first == name.given == ''
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Jean-Baptiste-Poquelin'
    assert name.suffix == name.junior == ''

    name = name_from_string('R. J. Van de Graaff')
    assert name.first == name.given == 'R. J. Van'
    assert name.prefix == name.von == 'de'
    assert name.last == name.family == 'Graaff'
    assert name.suffix == name.junior == ''


def test_one_comma_names():
    name = name_from_string('Brinch Hansen, Per')
    assert name.first == name.given == 'Per'
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Brinch Hansen'
    assert name.suffix == name.junior == ''

    name = name_from_string('van der Graaf, Horace Q.')
    assert name.first == name.given == 'Horace Q.'
    assert name.prefix == name.von == 'van der'
    assert name.last == name.family == 'Graaf'
    assert name.suffix == name.junior == ''

    name = name_from_string('van der graaf, Horace Q.')
    assert name.first == name.given == 'Horace Q.'
    assert name.prefix == name.von == 'van der'
    assert name.last == name.family == 'graaf'
    assert name.suffix == name.junior == ''

    name = name_from_string('Smith, John')
    assert name.first == name.given == 'John'
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Smith'
    assert name.suffix == name.junior == ''

    name = name_from_string('{Phillips Bong}, Kevin ')
    assert name.first == name.given == 'Kevin'
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Phillips Bong'
    assert name.suffix == name.junior == ''

    name = name_from_string('jean de la fontaine,')
    assert name.first == name.given == ''
    assert name.prefix == name.von == 'jean de la'
    assert name.last == name.family == 'fontaine'
    assert name.suffix == name.junior == ''

    name = name_from_string('de la fontaine, Jean')
    assert name.first == name.given == 'Jean'
    assert name.prefix == name.von == 'de la'
    assert name.last == name.family == 'fontaine'
    assert name.suffix == name.junior == ''

    name = name_from_string('De La Fontaine, Jean')
    assert name.first == name.given == 'Jean'
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'De La Fontaine'
    assert name.suffix == name.junior == ''

    name = name_from_string('De la Fontaine, Jean')
    assert name.first == name.given == 'Jean'
    assert name.prefix == name.von == 'De la'
    assert name.last == name.family == 'Fontaine'
    assert name.suffix == name.junior == ''

    name = name_from_string('de La Fontaine, Jean')
    assert name.first == name.given == 'Jean'
    assert name.prefix == name.von == 'de'
    assert name.last == name.family == 'La Fontaine'
    assert name.suffix == name.junior == ''


def test_two_comma_names():
    name = name_from_string('{Foo, Bar, and Sons}')
    assert name.first == name.given == ''
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Foo, Bar, and Sons'
    assert name.suffix == name.junior == ''

    name = name_from_string('Doe, Jr., John')
    assert name.first == name.given == 'John'
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Doe'
    assert name.suffix == name.junior == 'Jr.'

    name = name_from_string('von der Doe, Jr., John')
    assert name.first == name.given == 'John'
    assert name.prefix == name.von == 'von der'
    assert name.last == name.family == 'Doe'
    assert name.suffix == name.junior == 'Jr.'


def test_excess_comma_names():
    name = name_from_string('Doe, Jr., John, Excess')
    assert name.first == name.given == 'John'
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Doe'
    assert name.suffix == name.junior == 'Jr.'


def test_whitespace_in_names():
    name = name_from_string('  Nigel   Incubator-Jones')
    assert name.first == name.given == 'Nigel'
    assert name.prefix == name.von == ''
    assert name.last == name.family == 'Incubator-Jones'
    assert name.suffix == name.junior == ''

    name = name_from_string(u'   Charles Louis \nXavier Joseph    de \t   la '
                            u'Vall{\’e}e Poussin \t\r\n')
    assert name.first == name.given == u'Charles Louis Xavier Joseph'
    assert name.prefix == name.von == u'de la'
    assert name.last == name.family == u'Vall\’ee Poussin'
    assert name.suffix == name.junior == u''

    name = name_from_string('    Catherine \n\n  Crook \r\n  de \tCamp  \t')
    assert name.first == name.given == 'Catherine Crook'
    assert name.prefix == name.von == 'de'
    assert name.last == name.family == 'Camp'
    assert name.suffix == name.junior == ''


def test_name_formatting():
    name1 = name_from_string(u'Møllenbach, Doermann')
    name2 = name_from_string('Sterling, Archer')
    name3 = name_from_string('Doe, Jr., John')
    name4 = name_from_string('von der Doe, Jr., John')

    assert name1.format(style='first-last') == u'Doermann Møllenbach'
    assert name2.format(style='first-last') == 'Archer Sterling'
    assert name3.format(style='first-last') == 'John Doe Jr.'
    assert name4.format(style='first-last') == 'John von der Doe Jr.'
    assert name1.format(style='last-first') == u'Møllenbach, Doermann'
    assert name2.format(style='last-first') == 'Sterling, Archer'
    assert name3.format(style='last-first') == 'Doe, Jr., John'
    assert name4.format(style='last-first') == 'von der Doe, Jr., John'

    assert name1.format(style='first-last', initials=True) == u'D. Møllenbach'
    assert name2.format(style='first-last', initials=True) == 'A. Sterling'
    assert name3.format(style='first-last', initials=True) == 'J. Doe Jr.'
    assert name4.format(style='first-last', initials=True) ==\
        'J. von der Doe Jr.'
    assert name1.format(style='last-first', initials=True) == u'Møllenbach, D.'
    assert name2.format(style='last-first', initials=True) == 'Sterling, A.'
    assert name3.format(style='last-first', initials=True) == 'Doe, Jr., J.'
    assert name4.format(style='last-first', initials=True) ==\
        'von der Doe, Jr., J.'

    with pytest.raises(ValueError):
        name1.format(style='unknown')


def test_name_properties():
    name1 = name_from_string('Doermann')
    name2 = name_from_string(u'Møllenbach, Doermann')
    name3 = name_from_string('Sterling, Archer')
    name4 = name_from_string(u'de la Møllenbach, Doermann')
    name5 = name_from_string('von der Doe, Jr., John')
    name6 = name_from_string(u'Møllenbach, Doermann')

    assert len(name1) == 1
    assert len(name2) == 2
    assert len(name3) == 2
    assert len(name4) == 3
    assert len(name5) == 4
    assert len(name6) == 2

    assert name1 != name2
    assert name1 != name3
    assert name1 == name1
    assert name2 == name6
    assert name1 != tuple()

    assert str(name2) == 'Doermann Møllenbach'


@pytest.mark.skipif(sys.version_info[0] < 3, reason="requires Python 3.x")
def test_name_repr_py3():
    name1 = name_from_string(u'Møllenbach, Doermann')
    name2 = name_from_string('Sterling, Archer')

    assert repr(name1) ==\
        'Name(first=Doermann, prefix=, last=Møllenbach, suffix=)'

    assert repr(name2) ==\
        "Name(first=Archer, prefix=, last=Sterling, suffix=)"


@pytest.mark.skipif(sys.version_info[0] > 2, reason="Only on Python 2.x")
def test_name_repr_py2():
    name1 = name_from_string(u'Møllenbach, Doermann')
    name2 = name_from_string(u'Sterling, Archer')

    assert repr(name1) ==\
        'Name(first=Doermann, prefix=, last=Møllenbach, suffix=)'

    assert repr(name2) == 'Name(first=Archer, prefix=, last=Sterling, suffix=)'


def test_discover_unbalanced_braces():
    with pytest.raises(LexerError):
        name_from_string('Sterling, }Archer')
