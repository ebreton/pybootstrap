"""A basic scaffolding for a python CLI

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
"""
import logging

from docopt import docopt
from docopt_dispatch import dispatch

from utils import set_logging_config
from settings import VERSION


@dispatch.on('hello')
def do_list(name=None, **kwargs):
    print("Hello, {}!". format(name))


if __name__ == '__main__':
    kwargs = docopt(__doc__)
    set_logging_config(kwargs)
    logging.debug(kwargs)
    dispatch(__doc__, version=VERSION)
