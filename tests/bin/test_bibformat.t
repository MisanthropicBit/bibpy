Set up PYTHONPATH

    $ PYTHONPATH="$TESTDIR/../.." && export PYTHONPATH

Test version number

    $ $TESTDIR/../../bin/bibformat --version
    bibformat v0.1.0

Test alphabetic ordering

    $ $TESTDIR/../../bin/bibformat --order=true $TESTDIR/../data/all_bibpy_entry_types.bib
    @unpublished{unpubkey,
        author = {Somebody McPerson},
        title = {How To Parse BibTex},
        year = {2011}
    }
    
    @string{variable = "value"}
    
    @preamble{\textbf{\latex}}
    
    @comment{Anything is possible with comments!}

Test specific ordering

    $ $TESTDIR/../../bin/bibformat --order=year,author,title $TESTDIR/../data/all_bibpy_entry_types.bib
    @unpublished{unpubkey,
        year = {2011},
        author = {Somebody McPerson},
        title = {How To Parse BibTex}
    }
    
    @string{variable = "value"}
    
    @preamble{\textbf{\latex}}
    
    @comment{Anything is possible with comments!}

Test ordering with align

    $ $TESTDIR/../../bin/bibformat --order=title,author,year --align $TESTDIR/../data/all_bibpy_entry_types.bib
    @unpublished{unpubkey,
        title  = {How To Parse BibTex},
        author = {Somebody McPerson},
        year   = {2011}
    }
    
    @string{variable = "value"}
    
    @preamble{\textbf{\latex}}
    
    @comment{Anything is possible with comments!}

Verify json output

    $ echo $($TESTDIR/../../bin/bibformat --export=json $TESTDIR/../data/small1.bib) | python -m json.tool > /dev/null

Verify xml output

    $ echo $($TESTDIR/../../bin/bibformat --export=xml $TESTDIR/../data/small1.bib) | python -m xml.dom.minidom > /dev/null
