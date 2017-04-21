#!/usr/bin/python
"""
ts3LogAnalyzer.py

Usage:
    ts3LogAnalyzer.py <log>
    ts3LogAnalyzer.py <log> [-d <databse>] [--hide-ip] [--debug] [--output-logging]
    ts3LogAnalyzer.py -h | --help
    ts3LogAnalyzer.py -v | --version

Options:
    -d --database <databse>     Database to use or create (database.db used by default)
    --hide-ip                   Don't save ips
    --output-logging            Output logging from THIS program to ts3LogAnalyzer.log
    --debug                     Output debug information
    -h --help                   Show this screen
    -v --version                Show version
"""

__author__ = 'ToFran'
__site__ = 'http://tofran.com/'

__version__ = '2.0'
__maintainer__ = 'ToFran'
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
from datetime import datetime
from docopt import docopt

db = None
hideIp = False
openConn = dict()

def main():
    global db, HIDEIP
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    arguments = docopt(__doc__, version='2.0')
    logging.basicConfig( \
            format = "%(levelname)s: %(message)s", \
            level = logging.DEBUG if arguments['--debug'] else logging.INFO, \
            handlers = [logging.FileHandler( "ts3LogAnalyzer.log", 'w', 'utf-8')] if arguments['--output-logging'] else None \
        )

    hideIp = arguments['--hide-ip']
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
            logging.warning("-d not specified, using existing " + database)

    #log files
    path = arguments['<log>']
    if os.path.isdir(path):
        logging.debug(path + " is a folder.")
        for f in glob.glob(arguments['<log>'] + '/*.log'):
            analyseFile(f)
    elif os.path.isfile(path):
        logging.debug(path + " is a file.")
        analyseFile(path)
    else:
        logging.critical(path + " does not exist! Terminating...")
        sys.exit()

    db.commit()
    db.close()

def analyseFile(filepath):
    #check if logfile already analyzed
    savedLog = checkLog(filepath)
    size = os.path.getsize(filepath)
    if savedLog and size <= savedLog[2]:
        logging.info("Skipping " + filepath)
        return
    else:
        lineN = 0
        time = None
        lineArr = []
        openConn.clear()

        if savedLog:
            logId = savedLog[0]
            deleteConnections(logId)
        else:
            logId = insertLog(filepath)

        logging.info("Analyzing log " + str(logId) + ": " + filepath)

        with open(filepath, 'r', encoding='utf8') as f:
            for line in f:
                lineN += 1
                if len(line.strip()) > 0:
                    logging.debug("Line " + str(lineN))
                    lineArr = splitLine(line)
                    message = slpitMessage(lineArr[4])
                    time = lineArr[0]

                    if (lineArr[2] == 'VirtualServerBase' and
                        len(message) >= 4 and
                        message[0] == 'client'):
                            if message[1] == 'connected':
                                clientConnected(time, getId(message[3]), getIp(message[5]), message[2])
                            elif message[1] == 'disconnected':
                                clientDisconnected(time, getId(message[3]), getReason(message[5]), logId, message[2])

            #end for
        #end with

        #close remaining opened connections
        if len(openConn) > 0:
            logging.debug("Closing " + str(len(openConn)) + " unclosed connections: " + str(openConn))
            for id in openConn:
                insertConnection(id, openConn[id]['connected'], time, "Dropped at the end of the log", openConn[id]['ip'], logId)

        updateLog(logId, lineN, size)
        logging.info("Analyzed " + str(lineN) + " lines from " + str(logId) + ": " + filepath)


#################
#PARSING
def splitLine(line):
    line = line.strip()
    nSlash = 1
    arr = []
    pos = line.find('|')

    while nSlash <= 4 and pos != -1:
        arr.append(line[:pos].strip())
        line = line[pos+1:]
        nSlash += 1
        pos = line.find('|')
    arr.append(line)
    return arr

def slpitMessage(message):
    logging.debug("slpitMessage(" + message + "):")
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

        arr.append(html.unescape(message[0:pos].strip()))
        message = message[pos+1:]
        pos = message.find(' ')
    logging.debug(":" + str(arr))
    return arr

def getId(string):
    if len(string) > 5 and string.startswith("(id:"):
        return int(string[4:-1])
    logging.error("Couln't parse ID from: " + string)
    return -1

def getIp(string):
    pos = string.find(':')
    if pos != -1:
        return string[0:pos]
    logging.error("Couln't parse IP from: " + string)
    return "0.0.0.0"

def getReason(string):
    #todo improve reason handeling
    return string

#################
#ACTIONS
def clientConnected(when, id, ip, nickname = None):
    logging.debug("ClientConnected(" + when + ", " + str(id) + ", " + nickname + ip)
    #check if client exist
    if not clientExists(id):
        insertClient(id)

    #check if there is already a connecton opened
    if id in openConn:
        openConn[id]['count'] += 1
    else:
        openConn[id] = {'connected': when, 'ip': ip, 'count': 1}

    if nickname:
        nicknameUsed(id, nickname)

def clientDisconnected(when, id, reason, logId, nickname = None):
    if not id in openConn:
        logging.error("Client dictonnected without connecting!")
        return False

    if openConn[id]['count'] > 1:
        logging.debug("Closed 1 connection for client " + str(id) + ", ramaining: " + str(openConn[id]['count']))
        openConn[id]['count'] -= 1
    else:
        logging.debug('Client ' + str(id) + ' disconnected')
        insertConnection(id, openConn[id]['connected'], when, reason, openConn[id]['ip'], logId)
        del openConn[id]

    if nickname:
        nicknameUsed(id, nickname)
    return True

#################
#DATABSE
def create_db(conection):
    with open("schema.sql", 'r') as f:
        schema = f.read()
        cur = conection.cursor()
        conection.executescript(schema)

def insertConnection(client_id, connected, disconnected, reason, ip, log):
    cur = db.cursor()
    duration = (datetime.strptime(disconnected, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(connected, '%Y-%m-%d %H:%M:%S.%f')).seconds
    cur.execute( \
        "INSERT INTO connection (client, connected, disconnected, duration, reason, ip, log) " + \
        "VALUES (?, ?, ?, ?, ?, ?, ?)", \
        [client_id, connected, disconnected, duration, reason, "0.0.0.0" if hideIp else ip, log] \
        )
    return cur.lastrowid

def deleteConnections(logId):
    cur = db.cursor()
    cur.execute("DELETE FROM connection WHERE log = ?", [logId])

def insertClient(id):
    logging.debug("Creating new client " + str(id))
    cur = db.cursor()
    cur.execute("INSERT INTO client (id) VALUES (?)", [id])

def clientExists(id):
    cur = db.cursor()
    cur.execute("SELECT id FROM client WHERE client.id = ?", [id])
    if cur.fetchone() is not None:
        return True
    return False

def nicknameUsed(client_id, nickname):
    cur = db.cursor()
    cur.execute("INSERT OR IGNORE INTO nickname (client, nickname, used) VALUES (?, ?, 0)", [client_id, nickname])
    cur = db.cursor()
    cur.execute("UPDATE nickname SET used = used + 1 WHERE client = ? AND nickname = ?", [client_id, nickname])

def insertLog(filepath, wSize = False):
    cur = db.cursor()
    cur.execute( \
            "INSERT INTO log (name, size) VALUES (?, ?)", \
            [ntpath.basename(filepath), os.path.getsize(filepath) if wSize else 0] \
        )
    return cur.lastrowid

def updateLog(id, lines, size = None):
    cur = db.cursor()
    if size:
        cur.execute("UPDATE log SET lines = ?, size = ? WHERE id = ?", [lines, size, id])
    else:
        cur.execute("UPDATE log SET lines = ? WHERE id = ?", [lines, id])

def checkLog(filepath):
    cur = db.cursor()
    cur.execute("SELECT id, lines, size FROM log WHERE log.name = ?", [ntpath.basename(filepath)])
    return cur.fetchone()

def getNickname(client_id, ammount = 1):
    cur = db.cursor()
    cur.execute("SELECT nickname FROM nickname WHERE client = ? ORDER BY used DESC LIMIT ?", [client_id, ammount])
    return cur.fetchall()

def getCumulativeTime(client_id):
    cur = db.cursor()
    cur.execute("SELECT * FROM connection WHERE client = ? GROUP BY client ORDER BY SUM(duration) DESC LIMIT 1", [client_id])
    return cur.fetchone()

def getlongestCnn(client_id):
    cur = db.cursor()
    cur.execute("SELECT id, connected, disconnected, SUM(duration) FROM connection WHERE client = ? GROUP BY client LIMIT 1", [client_id])
    return cur.fetchone()

def countCnn(client_id):
    cur = db.cursor()
    cur.execute("SELECT COUNT(connection) FROM connection WHERE client = ?", [client_id])
    return cur.fetchone()

def mergeClients():
    #TODO
    #"SELECT nickname, m from nickname WHERE n >= 2 GROUP BY nickname ORDER BY COUNT(nickname) AS n DESC"
    #SELECT nickname, client from nickname where nickname = "natodroid"

if __name__ == '__main__':
    main()
