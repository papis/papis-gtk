# -*- coding: utf-8 -*-
#
# you can install this to a local test virtualenv like so:
#   virtualenv venv
#   ./venv/bin/pip install --editable .
#   ./venv/bin/pip install --editable .[dev]  # with dev requirements, too

import sys

main_dependencies = [
    "setuptools"
]

for dep in main_dependencies:
    try:
        __import__(dep)
    except ImportError:
        print(
            "Error: You do not have %s installed, please\n"
            "       install it. For example doing\n"
            "\n"
            "       pip3 install %s\n" % (dep, dep)
        )
        sys.exit(1)


from setuptools import setup
import gui


setup(
    name='papis-gtk',
    version=gui.__version__,
    maintainer=gui.__author__,
    maintainer_email=gui.__email__,
    author=gui.__author__,
    author_email=gui.__email__,
    license=gui.__license__,
    url='https://github.com/papis/papis-gtk',
    install_requires=[
        "papis>=0.6.0",
    ],
    python_requires='>=3',
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    extras_require=dict(
        # List additional groups of dependencies here (e.g. development
        # dependencies). You can install these using the following syntax,
        # for example:
        # $ pip install -e .[develop]
        optional=[],
        develop=[
            'sphinx',
            'sphinx-argparse',
            'sphinx_rtd_theme',
            'pytest',
        ]
    ),
    description='Gtk based graphical user interface for papis',
    long_description='',
    keywords=[
        'document',
        'books',
        'bibtex',
        'management',
        'papis',
        'zotero',
        'mendeley',
        'cli',
        'biliography'
    ],

    data_files=[

        ("share/doc/papis-gtk/", [
            "README.md",
            "LICENSE.txt",
        ]),

        ("share/applications", [
            "contrib/papis-gtk.desktop",
        ]),

    ],

    #test_suite="gui.tests",

    entry_points=dict(
        console_scripts=[
            'papis-gtk=gui.main:main'
        ]
    ),

    platforms=['linux', 'osx'],

)
