#!/usr/bin/python
"""
ts3LogAnalyzer.py

Usage:
    ts3LogAnalyzer.py <database> -a <path> [--stats] [--no-ips] [--mergeable] [--debug] [--output-logging]
    ts3LogAnalyzer.py <database> --merge <c1> <c2> [--debug] [--output-logging]
    ts3LogAnalyzer.py <database> ([--stats] [--no-ips] [--mergeable]) [--debug] [--output-logging]
    ts3LogAnalyzer.py -h | --help
    ts3LogAnalyzer.py -v | --version

Options:
    -a --analyze <path>             Log file or folder to analyze
    -s --stats                      Generate statistic fields for every client
    -i --no-ips                     Remove ip's from the databse
    -m --mergeable                  Make the clients mergeable
    --output-logging                Output logging from THIS program to ts3LogAnalyzer.log
    --debug                         Output debug information
    -h --help                       Show this screen
    -v --version                    Show version

More info @github: https://github.com/ToFran/TS3LogAnalyzer
"""

__author__ = 'tofran'
__site__ = 'https://tofran.com/'
__version__ = '2.1.1'
__maintainer__ = 'tofran'
__email__ = 'me@tofran.com'
__license__ = 'GNU GPLv3'

import os
import sys
import ntpath
import logging
import sqlite3
import glob
import html
import codecs
import traceback
import pkg_resources
import SQLAlchemy
from docopt import docopt
from datetime import datetime

db = None
openConn = dict()
DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


def main():


if __name__ == '__main__':
    main()
