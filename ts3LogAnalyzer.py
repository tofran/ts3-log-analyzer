"""
ts3LogAnalyzer.py

Usage:
    ts3LogAnalyzer.py -l <path> [-d <path>]
	ts3LogAnalyzer.py --version

Options:
    -l --logs <path>         Log file or folder to analyze
    -d --database <path>        Database to use or create
    -h --help		            Show this screen
	--version	               	Show version
"""

import os
import logging
import sqlite3
import glob
from docopt import docopt

cnn = None

def main():
    global cnn
    arguments = docopt(__doc__, version='2.0')
    logging.basicConfig(level=logging.DEBUG)
    print(arguments)

    #if no databse parameter, use databse.db
    database = 'database.db'
    if arguments['--database']:
        database = arguments['--database']

    #check if databse exits
    exists = os.path.exists(database)
    cnn = sqlite3.connect(database)
    if not exists:
        create_db(cnn)
        logging.info(database + ' created!')
    elif not arguments['--database']:
            logging.warning('-d not specified, using ' + database)

    #log files
    path = arguments['--logs']
    if os.path.isdir(path):
        for f in glob.glob("*_1.log"):
            loadFile(f)
    elif os.path.isfile(path):
        loadFile(path)

    #close db
    c.commit()
    c.close()

def create_db(cnn):
    with open('schema.sql', 'r') as f:
        sql = f.read()
        cur = cnn.cursor()
        cur.executescript(sql)

def loadFile(filepath):
    print(filepath)


if __name__ == "__main__":
    main()
