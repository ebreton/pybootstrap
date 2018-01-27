pybootstrap
===

basic scaffolding for python command line interfaces (CLI)

<!-- TOC -->

- [Objective](#objective)
- [What you will get](#what-you-will-get)
- [Pre-requisites](#pre-requisites)
- [Setup](#setup)
- [Development](#development)
- [A note on utils & tests](#a-note-on-utils--tests)

<!-- /TOC -->

## Objective

Kick-starting a python CLI in a controlled environment

    $ git clone https://github.com/ebreton/pybootstrap.git
    ...
    $ cd pybootstrap && make venv
    ...
    $ pipenv shell
    ...
    (pybootstrap-xxx) $ python src/commands.py -h
    A basic scaffolding for a python CLI

    Usage:
        commands.py hello  [--name=<TXT>] [-q | -d]
        commands.py -h
        commands.py -v

    Options:
        -h, --help       display this message and exit
        -v, --version    display version
        -n, --name=TXT   greeting name [default: You]
        -q, --quiet      set log level to WARNING [default: INFO]
        -d, --debug      set log level to DEBUG [default: INFO]

With a few safety nets in place:

    (pybootstrap-xxx) $ make dev
    flake8 src --max-line-length=120
    pytest --cov=. -x test
    ======================== test session starts =========================
    platform darwin -- Python 3.6.4, pytest-3.3.2, py-1.5.2, pluggy-0.6.0
    rootdir: /Users/emb/Documents/git-repositories/pybootstrap, inifile:
    plugins: cov-2.5.1
    collected 6 items

    test/test_utils.py ......                                      [100%]

    ---------- coverage: platform darwin, python 3.6.4-final-0 -----------
    Name                       Stmts   Miss Branch BrPart  Cover
    ------------------------------------------------------------
    src/utils/__init__.py          7      0      0      0   100%
    src/utils/csv.py              14      0      2      0   100%
    src/utils/env.py              12      0      4      0   100%
    src/utils/logging.py          10      8      4      0    14%
    src/utils/maintenance.py       8      6      0      0    25%
    src/utils/runner.py           21     12      2      0    39%
    src/utils/yaml.py             29     23      8      0    16%
    ------------------------------------------------------------
    TOTAL                        101     49     20      0    48%


    ====================== 6 passed in 0.11 seconds ======================

## What you will get

- `flake8` for conventions
- `pytest` for testing
- `coverage` for test coverage
- `yaml` because it is always convenient
- `docopt` for the CLI itself
- `yaml` because it is convenient

pipenv will give you all the details

    $ pipenv graph
    docopt-dispatch==0.0.2
    - docopt [required: Any, installed: 0.6.2]
    flake8==3.5.0
    - mccabe [required: >=0.6.0,<0.7.0, installed: 0.6.1]
    - pycodestyle [required: >=2.0.0,<2.4.0, installed: 2.3.1]
    - pyflakes [required: <1.7.0,>=1.5.0, installed: 1.6.0]
    pytest-cov==2.5.1
    - coverage [required: >=3.7.1, installed: 4.4.2]
    - pytest [required: >=2.6.0, installed: 3.3.2]
        - attrs [required: >=17.2.0, installed: 17.4.0]
        - pluggy [required: >=0.5,<0.7, installed: 0.6.0]
        - py [required: >=1.5.0, installed: 1.5.2]
        - setuptools [required: Any, installed: 38.4.0]
        - six [required: >=1.10.0, installed: 1.11.0]
    PyYAML==3.12

## Pre-requisites

You will need a few tools (that you probably already have for most of them):

- git
- make
- pipenv

## Setup

Well, it is really nothing more than

    $ git clone https://github.com/ebreton/pybootstrap.git
    ...
    $ cd pybootstrap && make venv
    ...

This a one-off setup. You will then just have to activate your environment when you wish to code:

    $ pipenv shell
    ...
    (pybootstrap-xxx) $

## Development

You will find a `Makefile` to simplify development. Just run

- `make` while coding  (or `make dev` if you like to be explicit)
- `make test` before pushing

The second one generates HTML file for the coverage, and open the index in your favorite browser

## A note on utils & tests

A few helpers are included in this repo, more for illustration than anything else, a bit for (my) conveniency also...

A few tests come along with them, only to make the scaffolder more readable, and to give you some practical examples.

It's up to you to raise the coverage ratio, or not. And to trash what you will not use.
