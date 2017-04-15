#!/usr/bin/python
"""
ts3LogAnalyzer.py

Usage:
    ts3LogAnalyzer.py <log> [-d <path>]
    ts3LogAnalyzer.py --version

Options:
    -d --database <path>        Database to use or create
    -h --help                   Show this screen
	-v --version                Show version
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

db = None

def main():
    global db
    arguments = docopt(__doc__, version='2.0')
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logging.debug('arguments: ' + str(arguments))

    #if no databse parameter, use databse.db
    database = 'database.db'
    if arguments['--database']:
        database = arguments['--database']

    #check if databse exits
    exists = os.path.exists(database)
    db = sqlite3.connect(database)
    if not exists:
        create_db(db)
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
    db.commit()
    db.close()

def create_db(conection):
    with open('schema.sql', 'r') as f:
        schema = f.read()
        cur = conection.cursor()
        conection.executescript(schema)

def analyseFile(filepath):
    print(filepath)
    lineN = 0
    lineArr = []
    connection = dict()
    with open(filepath, 'r') as f:
        for line in f:
            if len(line.strip()) > 1:
                lineN += 1
                logging.debug('line' + str(lineN))
                lineArr = line.strip().split('|')
                message = slpitMessage(lineArr[4])
                #time = datetime.datetime.strptime(lineArr[0], '%Y-%m-%d %H:%M:%S.%f')

                if (lineArr[2] == 'VirtualServerBase' and
                    len(message) >= 4 and
                    message[0] == 'client'):
                        if message[1] == 'connected':
                            clientConnected(lineArr[0], getId(message[3]), message[2], getIp(message[5]))
                        elif message[1] == 'disconnected':
                            clientDisconnected(lineArr[0], getId(message[3]), message[2], getReason(message[5]))


def slpitMessage(message):
    logging.debug('slpitMessage(' + message + '):')
    message = message.strip()
    i = 0
    arr = []
    while len(message) > 0:
        if message.startswith("'"):
            message = message[1:]
            pos = message.find("'(")
            if pos == -1:
                pos = message.find("'")

        else:
            pos = message.find(' ')
            if pos == -1:
                pos = len(message)-1

        arr.append(message[0:pos])
        message = message[pos+1:]
        pos = message.find(' ')
    logging.debug(":" + str(arr))
    return arr

def getId(string):
    string.strip()
    if len(string) > 5 and string.startswith('(id:'):
        return int(string[3:-1])
    logging.debug("Couln't parse ID from: " + string + " !")
    return -1

def getIp(string):
    string.strip()
    pos = string.find(":")
    if pos != -1:
        return string[0:pos]
    logging.debug("Couln't parse IP from: " + string + " !")
    return "0.0.0.0"

def getReason(string):
    string.strip()
    pos = string.find("=")
    if pos != -1:
        return string[pos:]
    logging.debug("Couln't get reason from: " + string + " !")
    return "NONE"

def clientConnected(when, id, nickname, ip):
    if not userExists():
        logging.debug("New user " + id)
    userExists(id)
    print("cn")

def clientDisconnected(when, id, nickname, reason):
    print("dc")

def usedNickname(id, nickname):
    cur = db.cursor()
    cur.execute("INSERT INTO nickname VALUES (?,?)", [id])

def userExists():
    cur = db.cursor()
    cur.execute("SELECT id FROM user WHERE user.id = ?", [id])
    if cur.fetchone() is not None:
        return True
    return False


if __name__ == "__main__":
    main()
