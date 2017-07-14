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
