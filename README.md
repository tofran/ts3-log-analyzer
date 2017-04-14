# TS3 Log Analyser 

[![Author](http://img.shields.io/badge/author-ToFran-336699.svg)](https://github.com/ToFran)

Python library to analyze TeamSpeak 3 logs
Original version made in Java ([v1_java]), v2.0 in python is currently in development.

Discussion in the teamspeak forum [thread].

## Funcionality

Analyze multiple log files or an entire folder loaded with them;

Store info about all clients in a MySQL database, providing querys like: 
 - Cumulative connection time
 - Most used nickname
 - Maximum connection time
 - Number of connections
 - Count of timeouts
 - and much more

## Usage
ts3LogAnalyzer.py
```
Usage:
    ts3LogAnalyzer.py <log> [-d <path>]
    ts3LogAnalyzer.py --version

Options:
    -d --database <path>    Database to use or create
    -h --help               Show this screen
    --version               Show version
```


## Licence
GNU General Public License v3.0

## Acknowledgements
[Docopt](https://github.com/docopt/docopt)

[thread]: http://forum.teamspeak.com/showthread.php/112796-RELEASE-TS3logAnalyser-Analyse-your-teamspeak-server-logs
[v1_java]: (https://github.com/ToFran/TS3LogAnalyzer/tree/v1_java)
