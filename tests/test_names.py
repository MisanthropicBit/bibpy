# -*- coding: utf-8 -*-

"""Test extraction of parts of names."""

import bibpy.name
import pytest
import sys


def name_from_string(s):
    return bibpy.name.Name.fromstring(s)


def test_zero_comma_names():
    name = name_from_string('')
    assert name.first == ''
    assert name.prefix == ''
    assert name.last == ''
    assert name.suffix == ''

    name = name_from_string('Louise')
    assert name.first == ''
    assert name.prefix == ''
    assert name.last == 'Louise'
    assert name.suffix == ''

    name = name_from_string('louise')
    assert name.first == ''
    assert name.prefix == ''
    assert name.last == 'louise'
    assert name.suffix == ''

    name = name_from_string('Catherine Crook de Camp')
    assert name.first == 'Catherine Crook'
    assert name.prefix == 'de'
    assert name.last == 'Camp'
    assert name.suffix == ''

    name = name_from_string('Jean de la Fontaine du Bois Joli')
    assert name.first == 'Jean'
    assert name.prefix == 'de la Fontaine du'
    assert name.last == 'Bois Joli'
    assert name.suffix == ''

    name = name_from_string('Jean de La Fontaine Du Bois Joli')
    assert name.first == 'Jean'
    assert name.prefix == 'de'
    assert name.last == 'La Fontaine Du Bois Joli'
    assert name.suffix == ''

    name = name_from_string('jean de la fontaine du bois joli')
    assert name.first == ''
    assert name.prefix == 'jean de la fontaine du bois'
    assert name.last == 'joli'
    assert name.suffix == ''

    name = name_from_string('Jean {de} la fontaine')
    assert name.first == 'Jean de'
    assert name.prefix == 'la'
    assert name.last == 'fontaine'
    assert name.suffix == ''

    name = name_from_string('jean {de} {la} fontaine')
    assert name.first == ''
    assert name.prefix == 'jean'
    assert name.last == 'de la fontaine'
    assert name.suffix == ''

    name = name_from_string('Jean {de} {la} fontaine')
    assert name.first == 'Jean de la'
    assert name.prefix == ''
    assert name.last == 'fontaine'
    assert name.suffix == ''

    name = name_from_string('Jean De La Fontaine')
    assert name.first == 'Jean De La'
    assert name.prefix == ''
    assert name.last == 'Fontaine'
    assert name.suffix == ''

    name = name_from_string('jean De la Fontaine')
    assert name.first == ''
    assert name.prefix == 'jean De la'
    assert name.last == 'Fontaine'
    assert name.suffix == ''

    name = name_from_string('Jean de La Fontaine')
    assert name.first == 'Jean'
    assert name.prefix == 'de'
    assert name.last == 'La Fontaine'
    assert name.suffix == ''

    name = name_from_string('Kim Stanley Robinson')
    assert name.first == 'Kim Stanley'
    assert name.prefix == ''
    assert name.last == 'Robinson'
    assert name.suffix == ''

    name = name_from_string('Michael {Marshall Smith}')
    assert name.first == 'Michael'
    assert name.prefix == ''
    assert name.last == 'Marshall Smith'
    assert name.suffix == ''

    name = name_from_string('Louis-Albert')
    assert name.first == ''
    assert name.prefix == ''
    assert name.last == 'Louis-Albert'
    assert name.suffix == ''

    name = name_from_string('Charles Louis Xavier Joseph de la '
                            'Vall{\’e}e Poussin')
    assert name.first == 'Charles Louis Xavier Joseph'
    assert name.prefix == 'de la'
    assert name.last == 'Vall\’ee Poussin'
    assert name.suffix == ''

    name = name_from_string('John Smith')
    assert name.first == 'John'
    assert name.prefix == ''
    assert name.last == 'Smith'
    assert name.suffix == ''

    name = name_from_string('J. R. R. Tolkien')
    assert name.first == 'J. R. R.'
    assert name.prefix == ''
    assert name.last == 'Tolkien'
    assert name.suffix == ''

    name = name_from_string('Jean Baptiste-Poquelin')
    assert name.first == 'Jean'
    assert name.prefix == ''
    assert name.last == 'Baptiste-Poquelin'
    assert name.suffix == ''

    name = name_from_string('Jean-Baptiste-Poquelin')
    assert name.first == ''
    assert name.prefix == ''
    assert name.last == 'Jean-Baptiste-Poquelin'
    assert name.suffix == ''

    name = name_from_string('R. J. Van de Graaff')
    assert name.first == 'R. J. Van'
    assert name.prefix == 'de'
    assert name.last == 'Graaff'
    assert name.suffix == ''


def test_one_comma_names():
    name = name_from_string('Brinch Hansen, Per')
    assert name.first == 'Per'
    assert name.prefix == ''
    assert name.last == 'Brinch Hansen'
    assert name.suffix == ''

    name = name_from_string('van der Graaf, Horace Q.')
    assert name.first == 'Horace Q.'
    assert name.prefix == 'van der'
    assert name.last == 'Graaf'
    assert name.suffix == ''

    name = name_from_string('van der graaf, Horace Q.')
    assert name.first == 'Horace Q.'
    assert name.prefix == 'van der'
    assert name.last == 'graaf'
    assert name.suffix == ''

    name = name_from_string('Smith, John')
    assert name.first == 'John'
    assert name.prefix == ''
    assert name.last == 'Smith'
    assert name.suffix == ''

    name = name_from_string('{Phillips Bong}, Kevin ')
    assert name.first == 'Kevin'
    assert name.prefix == ''
    assert name.last == 'Phillips Bong'
    assert name.suffix == ''

    name = name_from_string('jean de la fontaine,')
    assert name.first == ''
    assert name.prefix == 'jean de la'
    assert name.last == 'fontaine'
    assert name.suffix == ''

    name = name_from_string('de la fontaine, Jean')
    assert name.first == 'Jean'
    assert name.prefix == 'de la'
    assert name.last == 'fontaine'
    assert name.suffix == ''

    name = name_from_string('De La Fontaine, Jean')
    assert name.first == 'Jean'
    assert name.prefix == ''
    assert name.last == 'De La Fontaine'
    assert name.suffix == ''

    name = name_from_string('De la Fontaine, Jean')
    assert name.first == 'Jean'
    assert name.prefix == 'De la'
    assert name.last == 'Fontaine'
    assert name.suffix == ''

    name = name_from_string('de La Fontaine, Jean')
    assert name.first == 'Jean'
    assert name.prefix == 'de'
    assert name.last == 'La Fontaine'
    assert name.suffix == ''


def test_two_comma_names():
    name = name_from_string('{Foo, Bar, and Sons}')
    assert name.first == ''
    assert name.prefix == ''
    assert name.last == 'Foo, Bar, and Sons'
    assert name.suffix == ''

    name = name_from_string('Doe, Jr., John')
    assert name.first == 'John'
    assert name.prefix == ''
    assert name.last == 'Doe'
    assert name.suffix == 'Jr.'

    name = name_from_string('von der Doe, Jr., John')
    assert name.first == 'John'
    assert name.prefix == 'von der'
    assert name.last == 'Doe'
    assert name.suffix == 'Jr.'


def test_excess_comma_names():
    name = name_from_string('Doe, Jr., John, Excess')
    assert name.first == 'John'
    assert name.prefix == ''
    assert name.last == 'Doe'
    assert name.suffix == 'Jr.'


def test_whitespace_in_names():
    name = name_from_string('  Nigel   Incubator-Jones')
    assert name.first == 'Nigel'
    assert name.prefix == ''
    assert name.last == 'Incubator-Jones'
    assert name.suffix == ''

    name = name_from_string('   Charles Louis \nXavier Joseph    de \t   la '
                            'Vall{\’e}e Poussin \t\r\n')
    assert name.first == 'Charles Louis Xavier Joseph'
    assert name.prefix == 'de la'
    assert name.last == 'Vall\’ee Poussin'
    assert name.suffix == ''

    name = name_from_string('    Catherine \n\n  Crook \r\n  de \tCamp  \t')
    assert name.first == 'Catherine Crook'
    assert name.prefix == 'de'
    assert name.last == 'Camp'
    assert name.suffix == ''


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

    assert str(name2) == 'Doermann Møllenbach'


@pytest.mark.skipif(sys.version_info[0] < 3, reason="requires Python 3.x")
def test_name_repr():
    name1 = name_from_string(u'Møllenbach, Doermann')
    name1 = name_from_string('Sterling, Archer')

    assert repr(name1) ==\
        'Name(first=Doermann, prefix=, last=Møllenbach, suffix=)'

    assert repr(name2) ==\
        "Name(first=Archer, prefix=b'', last=Sterling, suffix=b'')"


@pytest.mark.skipif(sys.version_info[0] > 2, reason="Only on Python 2.x")
def test_name_repr():
    print(sys.version_info)
    name1 = name_from_string(u'Møllenbach, Doermann')
    name2 = name_from_string('Sterling, Archer')

    assert repr(name1) ==\
        'Name(first=Doermann, prefix=, last=Møllenbach, suffix=)'

    assert repr(name2) == 'Name(first=Archer, prefix=, last=Sterling, suffix=)'
