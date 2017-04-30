from setuptools import setup
import os

#get long description from readme
cur_dir = os.path.dirname(__file__)
try:
    long_description = open(os.path.join(cur_dir, 'README.md')).read()
except:
    long_description = ""

setup(
	name = 'ts3LogAnalyzer',
	version = '2.1',
	description = 'A cli utility for analyzing teamspeak 3 server logs.',
	ong_description = long_description,
	url = 'https://github.com/ToFran/TS3LogAnalyzer/',
	author = 'Francisco Marques AKA tofran',
	author_email = 'franscopcmarques@gmail.com',
	license = 'GPL V3',
	packages = ['ts3LogAnalyzer'],
	package_data = {'ts3LogAnalyzer': ['schema.sql']},
	zip_safe = False,
	install_requires = ['docopt>=0.6.2'],
    keywords='teamspeak ts3 ts3server ts',
	entry_points =
		"""
		    [console_scripts]
		    ts3LogAnalyzer = ts3LogAnalyzer.ts3LogAnalyzer:main
    	"""
	)
