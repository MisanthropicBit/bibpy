Set up PYTHONPATH

    $ PYTHONPATH="$TESTDIR/../.." && export PYTHONPATH

Test version number

    $ $TESTDIR/../../bin/bibgrep --version
    bibgrep v0.1.0

    $ $TESTDIR/../../bin/bibgrep --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:4

Test counting

    $ $TESTDIR/../../bin/bibgrep --entry="book" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:1

    $ $TESTDIR/../../bin/bibgrep --entry="book,inproceedings" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:2

    $ $TESTDIR/../../bin/bibgrep --field="issue=3" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:1

    $ $TESTDIR/../../bin/bibgrep --ignore-case --field="journal~logic" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:1

    $ $TESTDIR/../../bin/bibgrep --key="~Co" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:2

    $ $TESTDIR/../../bin/bibgrep --ignore-case --key="~Co" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:2

Test piping

    $ $TESTDIR/../../bin/bibgrep --entry="book" $TESTDIR/../data/small1.bib | $TESTDIR/../../bin/bibgrep --count --no-filenames
    1

    $ $TESTDIR/../../bin/bibgrep --entry="book,inproceedings" $TESTDIR/../data/small1.bib | $TESTDIR/../../bin/bibgrep --count --no-filenames
    2

Test multiple files

    $ $TESTDIR/../../bin/bibgrep --entry="article" --count --no-filenames $TESTDIR/../data/small1.bib $TESTDIR/../data/simple_1.bib
    3

    $ $TESTDIR/../../bin/bibgrep --entry="article" --count --abbreviate-filenames $TESTDIR/../data/small1.bib $TESTDIR/../data/simple_1.bib
    small1.bib:2
    simple_1.bib:1

Test removing duplicate

    $ $TESTDIR/../../bin/bibgrep --count --unique --abbreviate-filenames $TESTDIR/../data/duplicates.bib
    duplicates.bib:1

Test single comparison

    $ $TESTDIR/../../bin/bibgrep --field="year>=2000" --count --abbreviate-filenames $TESTDIR/../data/simple_1.bib
    simple_1.bib:1

Test interval comparison

    $ $TESTDIR/../../bin/bibgrep --field="year=2007-2011" --count --abbreviate-filenames $TESTDIR/../data/simple_1.bib
    simple_1.bib:1

Test range comparison

    $ $TESTDIR/../../bin/bibgrep --field="2007<=year<2011" --count --abbreviate-filenames $TESTDIR/../data/simple_1.bib
    simple_1.bib:1

Test single comparison failure

    $ $TESTDIR/../../bin/bibgrep --field="author>=2000" $TESTDIR/../data/small1.bib
    bibgrep: Cannot compare '2000' with 'Bernd Meyer'

Test interval comparison failure

    $ $TESTDIR/../../bin/bibgrep --field="author=2007-2011" --count $TESTDIR/../data/small1.bib
    bibgrep: Cannot compare 'Bernd Meyer' with interval [2007, 2011]

Test range comparison failure

    $ $TESTDIR/../../bin/bibgrep --field="2007<=author<2011" --count $TESTDIR/../data/small1.bib
    bibgrep: Cannot compare 'Bernd Meyer' with range 2007 <= field < 2011
