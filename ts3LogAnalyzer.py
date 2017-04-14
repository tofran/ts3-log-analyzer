#!/usr/bin/python
"""
ts3LogAnalyzer.py

Usage:
    ts3LogAnalyzer.py <log> [-d <path>]
	ts3LogAnalyzer.py --version

Options:
    -d --database <path>        Database to use or create
    -h --help		            Show this screen
	--version	               	Show version
"""

__author__ = 'ToFran'
__site__ = 'http://tofran.com/'

__version__ = "2.0"
__maintainer__ = "ToFran"
__email__ = "me@tofran.com"
__license__ = "GNU GPLv3"

import os
import sys
import logging
import sqlite3
import glob
from docopt import docopt


cnn = None

def main():
    global cnn
    arguments = docopt(__doc__, version='2.0')
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logging.debug('arguments: ' + str(arguments))

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
    path = arguments['<log>']
    if os.path.isdir(path):
        logging.debug(path + ' is a folder.')
        for f in glob.glob("*.log"):
            analyseFile(f)
    elif os.path.isfile(path):
        logging.debug(path + ' is a file.')
        analyseFile(path)
    else:
        logging.critical(path + " does not exist! Terminating...")
        sys.exit()

    #close db
    cnn.commit()
    cnn.close()

def create_db(cnn):
    with open('schema.sql', 'r') as f:
        sql = f.read()
        cur = cnn.cursor()
        cur.executescript(sql)

def analyseFile(filepath):
    print(filepath)
    #slpitMessage("client connected 'user'(id:2) from 0.0.0.0:36634")

    lineN = 0
    lineArr = []
    with open(filepath, 'r') as f:
        for line in f:
            if len(line.strip()) > 1:
                lineN += 1
                logging.debug('line' + str(lineN))
                lineArr = line.strip().split('|')
                message = slpitMessage(lineArr[4])
                #time = datetime.datetime.strptime(lineArr[0], '%Y-%m-%d %H:%M:%S.%f')

                if (lineArr[2] == 'VirtualServerBase' and
                    len(message) >= 4 and message[0] == 'client' and
                    (message[1] == 'connected' or message[1] == 'disconnected')):
                        print(clientInfo[1] + ' ' + clientInfo[0])
                        '''
                        if message[1] == 'connected':
                                clientConnected(time, clientInfo[1], clientInfo[0], message[-1].split(':')[0])
                            elif message[1] == 'disconnected':
                                clientDisconnected(time, clientInfo[1], clientInfo[0])
                        '''


def slpitMessage(message):
    i = 0
    arr = []
    pos = message.index(' ')
    while pos != -1:
        arr.append(message[0:pos])
        message = message[pos+1:]
        pos = message.find(' ')
    logging.debug('slpitMessage(' + message + ') = ' + str(arr))
    return arr

if __name__ == "__main__":
    main()
