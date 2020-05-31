"""bibpy module setup script for distribution."""

from __future__ import with_statement

import os
from setuptools import setup


def get_version(filename):
    with open(filename) as fh:
        for line in fh:
            if line.startswith('__version__'):
                return line.split('=')[-1].strip()[1:-1]


setup(
    name='bibpy',
    version=get_version(os.path.join('bibpy', '__init__.py')),
    author='Alexander Asp Bock',
    author_email='albo.developer@gmail.com',
    platforms='All',
    python_requires='>=3.5',
    install_requires=['funcparserlib>=0.3.6'],
    tests_require=[
        'coverage>=5.1',
        'coveralls>=2.0.0',
        'cram>=0.7',
        'pydocstyle',
        'pytest>4.6',
        'vcrpy>=4.0.2',
    ],
    description=('Bib(la)tex parsing and useful tools'),
    license='BSD 3-Clause License',
    keywords='bibpy, bibtex, biblatex, parser',
    url='https://bibpy.readthedocs.io/en/latest/',
    packages=[
        'bibpy',
        'bibpy.doi',
        'bibpy.entry',
        'bibpy.lexers',
        'bibpy.scripts'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    project_urls={
        'Issue Tracker': 'https://github.com/MisanthropicBit/bibpy/issues',
        'Documentation': 'https://bibpy.readthedocs.io/en/latest/',
        'Source': 'https://github.com/MisanthropicBit/bibpy',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    entry_points={
        'console_scripts': [
            'bibformat = bibpy.scripts.bibformat:main',
            'bibgrep = bibpy.scripts.bibgrep:main',
            'bibstats = bibpy.scripts.bibstats:main',
        ]
    }
)
