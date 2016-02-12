"""
ts3LogAnalyzer.py

Usage:
    ts3LogAnalyzer.py [-l <path>] -i <path> <output>
	ts3LogAnalyzer.py --version

Options:
    -i --import <path>          Log file or folder to analyze
    -l --load <file>            Load a previously generated data
    -h --help		            Show this screen
	--version	               	Show version

"""
from docopt import docopt

arguments = docopt(__doc__, version='2.0')
print(arguments)
