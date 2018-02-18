Detailed installation process
=============================

Table of contents
-----------------

<!-- TOC -->

- [Overview](#overview)
    - [Pre-requisites](#pre-requisites)
    - [Main steps](#main-steps)
- [Starting point: github](#starting-point-github)
- [Initial setup](#initial-setup)
    - [`make init`](#make-init)
    - [`pipenv shell`](#pipenv-shell)
    - [`make vars` & `make test`](#make-vars--make-test)
- [Command Line Interface (CLI)](#command-line-interface-cli)
- [Dependencies](#dependencies)

<!-- /TOC -->

## Overview

### Pre-requisites

If you do not have them already, install

1. [GNU make](https://www.gnu.org/software/make/)
1. [pipenv](http://pipenv.readthedocs.io/en/latest/)
1. [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

You can test what you have with the following commands:

    $ make --version
    GNU Make 3.81
    ...
    $ pipenv --version
    pipenv, version 9.0.3
    $ git --version
    git version 2.12.2

### Main steps

1. Download (or fork) this repo and run `make init`
1. Activate your virtual environment with `pipenv shell`
1. run `make init`. You can check the resulting configuration with `make vars`
1. Run `make test`

## Starting point: github

You may download, clone or fork the project.

The following line clone it, and change your current working directory into it:

    $ git clone git@github.com:ebreton/pybootstrap.git your-app-name
    ...
    $ cd your-app-name

For a new project, just replace the .git files with new ones:

    $ rm -rf .git
    $ git init
    $ git add .
    $ git commit -m "initial revision"
    ...

## Initial setup

### `make init`

    $ make init
    cp .env.sample .env
    echo PYTHONPATH=`pwd`/src >> .env
    pipenv --update
    All good!
    pipenv update --dev --python 3
    Creating a virtualenv for this project…
    ...
    All dependencies are now up-to-date!


### `pipenv shell`

    $ pipenv shell
    ...

### `make vars` & `make test`

Once you have set up your `.env` file, you may activate your virtual environment, and control what values will be used with

    $ pipenv shell
    (pybootstrap-xxx) $ make vars
    Environment-related vars:
        PYTHONPATH=/Users/emb/Documents/git-repos/your-app-name/src

## Command Line Interface (CLI)

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

## Dependencies

pipenv will give you all the details

    $ pipenv graph
    autopep8==1.3.4
    - pycodestyle [required: >=2.3, installed: 2.3.1]
    docopt-dispatch==0.0.2
    - docopt [required: Any, installed: 0.6.2]
    flake8==3.5.0
    - mccabe [required: >=0.6.0,<0.7.0, installed: 0.6.1]
    - pycodestyle [required: >=2.0.0,<2.4.0, installed: 2.3.1]
    - pyflakes [required: <1.7.0,>=1.5.0, installed: 1.6.0]
    pytest-cov==2.5.1
    - coverage [required: >=3.7.1, installed: 4.5.1]
    - pytest [required: >=2.6.0, installed: 3.4.0]
        - attrs [required: >=17.2.0, installed: 17.4.0]
        - pluggy [required: >=0.5,<0.7, installed: 0.6.0]
        - py [required: >=1.5.0, installed: 1.5.2]
        - setuptools [required: Any, installed: 38.5.1]
        - six [required: >=1.10.0, installed: 1.11.0]
    PyYAML==3.12