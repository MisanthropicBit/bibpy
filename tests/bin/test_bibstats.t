Set up PYTHONPATH

    $ PYTHONPATH="$TESTDIR/../.." && export PYTHONPATH

Test version number

    $ $TESTDIR/../../bin/bibstats --version
    bibstats v0.1.0

Test output

    $ $TESTDIR/../../bin/bibstats --sort-entries $TESTDIR/../data/graphs.bib
    Entry                Count               
    -----------------------------------------
    article              881
    book                 56
    booklet              1
    inbook               3
    incollection         7
    inproceedings        256
    manual               1
    mastersthesis        4
    misc                 21
    phdthesis            30
    techreport           113
    unpublished          86
    
    Total entries: 1459

Test output with percentages

    $ $TESTDIR/../../bin/bibstats --percentages --sort-entries $TESTDIR/../data/graphs.bib
    Entry                Count               
    -----------------------------------------
    article              881 (60.38%)
    book                 56 (3.84%)
    booklet              1 (0.07%)
    inbook               3 (0.21%)
    incollection         7 (0.48%)
    inproceedings        256 (17.55%)
    manual               1 (0.07%)
    mastersthesis        4 (0.27%)
    misc                 21 (1.44%)
    phdthesis            30 (2.06%)
    techreport           113 (7.75%)
    unpublished          86 (5.89%)
    
    Total entries: 1459

Test output with count

    $ $TESTDIR/../../bin/bibstats --count $TESTDIR/../data/small1.bib
    4

Test porcelain output

    $ $TESTDIR/../../bin/bibstats --porcelain --sort-entries $TESTDIR/../data/small1.bib
    article              2
    book                 1
    inproceedings        1

Test --top option

    $ $TESTDIR/../../bin/bibstats --top=3 --sort-entries $TESTDIR/../data/small1.bib
    Entry                Count               
    -----------------------------------------
    article              2
    book                 1
    inproceedings        1
    
    Total entries: 4
