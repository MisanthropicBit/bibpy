FAQ
===

**Q: Why are the key and type properties of entries prefixed with 'bib'?**

In bibtex and biblatex, there are already :code:`key` and a :code:`type`
fields. Per the bibtex documentation, the :code:`key` field is:

    *Used for alphabetizing, cross referencing, and creating a label when the
    “author” information (described in Section 4) is missing.*

and the :code:`type` field is:

    *The type of a technical report—for example, “Research Note”.*

**Q: Why are there no conversion functions from and to JSON, XML etc.?**

There are already a ton of excellent tools for the job such as `pandoc
<https://pandoc.org/>`__, and I did not want to reinvent the wheel. Moreover,
there are none or few standardised bibliography formats for the other file
formats, making it hard to support.

**Q: Why does bibpy replace my string variables with the empty string?**

This is likely because a string variable was missing. The default behaviour of
both bibtex and biblatex is to issue a warning regarding empty string
substitution and perform the substitution.
