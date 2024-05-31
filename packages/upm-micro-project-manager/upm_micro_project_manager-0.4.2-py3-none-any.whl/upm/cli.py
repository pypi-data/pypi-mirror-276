#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
# author       # TecDroiD
# date         # 2022-12-02
# ---------------------------------------------------------------------------
# description  # simple python project management tool - cli
#              #
#              #
##############################################################################
import sys
from argparse import ArgumentParser
import logging

from upm import config
from upm import upm
from upm import __version__


def add_scan_parser(subs):
    """ create subparser to describe an item
    """
    parser = subs.add_parser('scan', help='create new template from directory')
    parser.add_argument(
        '-n', '--no-write',
        help='do not write template file',
        action='store_true'
    )
    parser.add_argument(
        '-d', '--description',
        help='optional template description',
        default=''
    )

    parser.add_argument('basedir', help='directory to scan')
    parser.add_argument('name', help='name of the new template')


def add_describe_parser(subs):
    """ create subparser to describe an item
    """
    parser = subs.add_parser('desc', help='describe item')
    parser.add_argument('item', help='Item to describe')


def add_init_parser(subs):
    """ create a subparser for initializing items
    """
    parser = subs.add_parser('init', help='initialize an item')
    parser.add_argument(
        '-p', '--parameter',
        nargs='*',
        help='parameters in form key=value'
    )
    parser.add_argument(
        '-n', '--no-replace',
        action='store_true',
        help='Do not expand pattern for enhancing existing templates'
    )
    parser.add_argument('item', help='Item to initialize')
    parser.add_argument(
        'destination',
        help='destination of the new item'
    )


def parse_arguments():
    """ creates an argument parser and parses arguments
    """
    parser = ArgumentParser(
        description='helps you generating python projects',
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='tell me more'
    )
    parser.add_argument(
        '-V', '--version',
        action='store_true',
        help='get the current version'
    )
    subs = parser.add_subparsers(
        dest='action',
        help='subfunctions'
    )
    subs.add_parser('list', help='list possible elements')
    add_describe_parser(subs)
    add_init_parser(subs)
    add_scan_parser(subs)
    return parser.parse_args()


def main():
    """ this is the main function who controls all the other things
    """
    args = parse_arguments()
    if args.version:
        print(__version__)
        return 0

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level)

    # load configuration
    cfg = config.load(['~/.upm/config', './.upm'])
    # do
    upm.run(cfg, args)


if __name__ == '__main__':
    sys.exit(main())
