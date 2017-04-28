#!/usr/bin/python
"""
ts3LogAnalyzer.py

Usage:
    ts3LogAnalyzer.py <database> -a <path> [--stats] [--no-ips] [--debug] [--output-logging]
    ts3LogAnalyzer.py <database> --merge <c1> <c2> [--debug] [--output-logging]
    ts3LogAnalyzer.py <database> (--stats | --no-ips) [--debug] [--output-logging]
    ts3LogAnalyzer.py -h | --help
    ts3LogAnalyzer.py -v | --version

Options:
    -a --analyze <path>             Log file or folder to analyze
    -s --stats                      Generate statistic fields for every client
    -i --no-ips                     Remove ip's from the databse
    --output-logging                Output logging from THIS program to ts3LogAnalyzer.log
    --debug                         Output debug information
    -h --help                       Show this screen
    -v --version                    Show version

More info @github: https://github.com/ToFran/TS3LogAnalyzer
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
import pkg_resources
from docopt import docopt
from datetime import datetime

db = None
openConn = dict()

def main():
    global db
    #sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    arguments = docopt(__doc__, version='2.0')
    logging.basicConfig( \
            format = "%(levelname)s: %(message)s", \
            level = logging.DEBUG if arguments['--debug'] else logging.INFO, \
            handlers = [logging.FileHandler( "ts3LogAnalyzer.log", 'w', 'utf-8')] if arguments['--output-logging'] else None \
        )

    database = arguments['<database>']
    logpath = arguments['--analyze']
    client_id_1 = arguments['<c1>']
    client_id_2 = arguments['<c2>']

    import time
    start_time = time.time()

    #database
    exists = os.path.exists(database)
    db = sqlite3.connect(database)
    if not exists:
        setupDB()
        logging.info(database + ' created!')

    if logpath:
        analyze(logpath)
    elif client_id_1 and client_id_2:
        try:
            client_id_1 = int(client_id_1)
            client_id_2 = int(client_id_2)
        except Exception as e:
            logging.critical("Invalid merge input!")
            sys.exit()
        mergeClients(client_id_1, client_id_2)

    if arguments['--hide-ip']:
        removeIps()
    if arguments["--stats"]:
        generateStats()

    db.commit()
    db.close()
    logging.debug("Finished! Execution time: " + str(time.time() - start_time) + "s")
    return

def analyze(path):
    if os.path.isdir(path):
        logging.debug(path + " is a folder.")
        for f in glob.glob(path + '/*.log'):
            analyseFile(f)
    elif os.path.isfile(path):
        logging.debug(path + " is a file.")
        analyseFile(path)
    else:
        logging.critical(logpath + " does not exist! Terminating...")
        sys.exit()
    return

def analyseFile(filepath):
    global openConn
    #check if logfile already analyzed
    savedLog = getLog(filepath)
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
    return


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
    return

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
def setupDB():
    resource_path = '/'.join(('schema.sql',))
    schema = str(pkg_resources.resource_string(__name__, resource_path), 'utf-8')
    cur = db.cursor()
    cur.executescript(schema)
    return

#Connection
def insertConnection(client_id, connected, disconnected, reason, ip, log):
    cur = db.cursor()
    duration = (datetime.strptime(disconnected, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(connected, '%Y-%m-%d %H:%M:%S.%f')).seconds
    cur.execute( \
        "INSERT INTO connection (client_id, connected, disconnected, duration, reason, ip, logfile) " + \
        "VALUES (?, ?, ?, ?, ?, ?, ?)", \
        [client_id, connected, disconnected, duration, reason, ip, log] \
        )
    return cur.lastrowid

def deleteConnections(logId):
    cur = db.cursor()
    cur.execute("DELETE FROM connection WHERE log_id = ?", [logId])
    return

def insertClient(client_id):
    logging.debug("Creating new client " + str(client_id))
    cur = db.cursor()
    cur.execute("INSERT INTO client (client_id) VALUES (?)", [client_id])
    return

#Client
def clientExists(client_id):
    return getClient(client_id) is not None

def getClient(client_id):
    cur = db.cursor()
    cur.execute("SELECT * FROM client WHERE client_id= ?", [client_id])
    return cur.fetchone()

#Nickname
def nicknameUsed(client_id, nickname):
    cur = db.cursor()
    cur.execute("INSERT OR IGNORE INTO nickname (client_id, nickname, used) VALUES (?, ?, 0)", [client_id, nickname])
    cur = db.cursor()
    cur.execute("UPDATE nickname SET used = used + 1 WHERE client_id = ? AND nickname = ?", [client_id, nickname])
    return

def getNickname(client_id, ammount = 1):
    cur = db.cursor()
    cur.execute("SELECT nickname FROM nickname WHERE client_id = ? ORDER BY used DESC LIMIT ?", [client_id, ammount])
    return cur.fetchall()

#Log
def insertLog(filepath, wSize = False):
    cur = db.cursor()
    cur.execute( \
            "INSERT INTO log (filename, size) VALUES (?, ?)", \
            [ntpath.basename(filepath), os.path.getsize(filepath) if wSize else 0] \
        )
    return cur.lastrowid

def updateLog(log_id, lines, size = None):
    cur = db.cursor()
    if size:
        cur.execute("UPDATE log SET lines = ?, size = ? WHERE log_id = ?", [lines, size, log_id])
    else:
        cur.execute("UPDATE log SET lines = ? WHERE log_id = ?", [lines, log_id])
    return

def getLog(filepath):
    cur = db.cursor()
    cur.execute("SELECT log_id, lines, size FROM log WHERE filename = ?", [ntpath.basename(filepath)])
    return cur.fetchone()

#User
def getUser(client_id):
    cur = db.cursor()
    cur.execute("SELECT user_id FROM client WHERE client_id = ?", [client_id])
    return cur.fetchone()

def setUser(client_id, user_id = None):
    cur = db.cursor()
    if user_id: #create user
        cur.execute("INSERT INTO user () VALUES ()")
        user_id = cur.lastrowid

    cur = db.cursor()
    cur.execute("UPDATE client SET user_id = ? WHERE client_id = ?", [user_id, client_id])
    return user_id

def generateStats():
    logging.debug("Generating statistics")
    cur = db.cursor()
    cur.execute("SELECT client_id FROM client") #get all crientid's
    for tup_id in cur: #set statistics for each one
        client_id = str(tup_id[0])
        cur = db.cursor()
        cur.execute(
                "UPDATE client SET " + \
                    "mainNickname = (SELECT nickname FROM nickname WHERE client_id = :client_id ORDER BY used DESC LIMIT 1), " + \
                    "nCon = (SELECT COUNT(*) FROM connection WHERE client_id = :client_id), " + \
                    "totalTime = (SELECT SUM(duration) FROM connection WHERE client_id = :client_id), " \
                    "maxTime = (SELECT MAX(duration) FROM connection WHERE client_id = :client_id) " \
                "WHERE client_id = :client_id;",
                {"client_id": client_id}
            )
    return

def removeIps():
    cur = db.cursor()
    cur.execute("UPDATE connection SET ip = '0.0.0.0'")
    return

def mergeClients(client_id_1, client_id_2):
    logging.debug("Merging client " + client_id_1 + " with " + client_id_2)
    user1 = getUser(client_id_1)
    user2 = getUser(client_id_2)

    if(user1 and user2):
        logging.error(
            "Client " + client_id_1 + " and " + client_id_2  + \
            " are both assigned to an user (" + user1 + " and " + user2 + ")" \
            )
        return False
    elif(user1):
        setUser(client_id_2, user1)
    elif(user2):
        setUser(client_id_1, user2)
    else:
        setUser(client_id_2, setUser(client_id_1))

    logging.info("Client " + client_id_1 + " and " + client_id_2  + " merged.")
    return True

# ----

if __name__ == '__main__':
    main()
