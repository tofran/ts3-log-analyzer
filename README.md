# TS3 Log Analyser 

[![pypi link](https://img.shields.io/pypi/v/ts3LogAnalyzer.svg)][pypi]
![Python version 3](https://img.shields.io/badge/Python-3-blue.svg)

**A Python utility for analyzing TeamSpeak 3 server logs.**

Analyze multiple log files or an entire log folder.
Stores info about all clients in a SQLite database for ease of use by other applications.

You can extract info like:
 - Who has the most cumulative connection time on the server / Time spent by each user on server
 - Longest connection time
 - First and last seen
 - Most used nicknames
 - Number of connections
 - and much more

## Installation
`pip install ts3LogAnalyzer`

Alternatively you can clone and setup using setuptools or simply call the file directly

## Usage
ts3LogAnalyzer.py
```
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
```

Example:

`ts3LogAnalyzer.py databse.db -a ../teamspeak3-server/logs/ --no-ips`

You can easily setup a cron job for automatic update.

## Discussion

Discussion in the teamspeak forum [thread].

## Licence
GNU General Public License v3.0

[thread]: http://forum.teamspeak.com/showthread.php/112796-RELEASE-TS3logAnalyser-Analyse-your-teamspeak-server-logs
[pypi]: https://pypi.python.org/pypi/ts3LogAnalyzer
[v1_java]: (https://github.com/ToFran/TS3LogAnalyzer/tree/v1_java)
