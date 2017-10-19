# TS3 Log Analyser

[![pypi link](https://img.shields.io/pypi/v/ts3LogAnalyzer.svg)][pypi]
![Python version 3](https://img.shields.io/badge/Python-3-blue.svg)

**A Python utility for analyzing TeamSpeak 3 server logs.**

Analyze multiple log files or an entire log folder.
Stores info about all clients and respective connections and nicknames in a SQLite database for ease of use by other applications.

Can be used for extracting information like:
 - Who has the most cumulative connection time on the server / Time spent by each user on server
 - Longest connection time for each user
 - First and last seen
 - Most used nicknames
 - Total number of connections
 - Merge users with different identities
 - and much more...

Generate useful/fun statistics like the ones you can [find here][ToFran's server statistics] for my server:

[![preview](https://i.gyazo.com/c6c4689ed2f69cf98cf295619b0235f2.png)][ToFran's server statistics]


It can also 'merge' identities out of the box, this way you can combine stats for users that have multiple identities - as seen in the [example][ToFran's server statistics] (If you belive that everyone should backup their identities, and if they don't do it, it's their fault - you can ignore this feature :D )

**Disclaimer:** The aim of this project/repo is the log analyzer This repo does not include the web viewer. I'm still developing it, and currently it is not published. This means that you can only generate the DB, and build your own web application. Hopefully I will release [mine](https://github.com/tofran/ts3LogAnalyzer-viwer).

Analy**s**e VS Analy**z**e: Look, English is not my main language, therefore I only found out that anali*s*e could be spelled with an `s` or `z` much after creating and publishing this project. I do not believe that one is better over another. If you cannot live with ts3LogAnaly**z**er with `z` you can always alias it :P.

## Usage

### Installation

Python 3 only.

`pip install ts3LogAnalyzer`

Alternatively you can clone and setup using setuptools or simply call the file directly.

### Examples

  * Analyze a file:

  `$ ts3LogAnalyzer databse.db -a ts3server_2017-02-12__11_46_44.016222_1.log`

  * Analyze a folder:

  `$ ts3LogAnalyzer databse.db -a ts3server/logs`

  * Analyze a folder, make it mergeable and generate statistics and hide IP's:

  `$ ts3LogAnalyzer databse.db -a . -msi`

  * Be nice to the system when running:

  `$ nice -n 19 ts3LogAnalyzer db.db -a /path/ -msi`

  * Merge two clients:

  `$ ts3LogAnalyzer databse.db --merge 13 37`


### Options
```
ts3LogAnalyzer.py
Usage:
    ts3LogAnalyzer.py <database> -a <path> [--stats] [--no-ips] [--mergeable] [--debug] [--output-logging]
    ts3LogAnalyzer.py <database> --merge <c1> <c2> [--debug] [--output-logging]
    ts3LogAnalyzer.py <database> ([--stats] | [--no-ips]) [--debug] [--output-logging]
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
```

## Todo

 - [ ] Performance improvements #3
 - [ ] Support for other DB's other than SQLite #5
 - [ ] Python 2 compatibility

## Discussion

Feature requests and bugs: [issues]

Other discussion: TeamSpeak forum [thread]

## Licence
GNU General Public License v3.0

## Contact/Donate
Contact me at [tofran.com](https://tofran.com).

[ToFran's server statistics]: http://tofran.com/ts/stats/
[thread]: http://forum.teamspeak.com/showthread.php/112796-RELEASE-TS3logAnalyser-Analyse-your-teamspeak-server-logs
[pypi]: https://pypi.python.org/pypi/ts3LogAnalyzer
[issues]: https://github.com/tofran/ts3LogAnalyzer/issues
[v1_java]: (https://github.com/ToFran/TS3LogAnalyzer/tree/v1_java)
