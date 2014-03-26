import ConfigParser
import github
import logging
import MySQLdb
import os
import re

license = {
    """
    Dictionary of the main families of open source licenses. Each family
    contains the regular expressions that will be used to identify if a repo
    uses a license from that particular family.
    """
    
    "apache": [
        "Apache[- ]License[- ]2.0",
        "Apache[- ]2.0",
    ],
    "bsd": [
        "BSD[- ]3"
        "BSD[- ]Simplified",
        "BSD[- ]New",
        "BSD[- ]2",
        "FreeBSD"
    ],
    "cc": [
        "Creative Commons",
        "CC BY",
        "CC BY-SA",
        "CC BY-ND",
        "CC BY-NC",
        "CC BY-NC-SA",
        "CC BY-NC-ND"
    ],
    "epl": [
        "Eclipse Public License",
        "EPL[- ]1.0"
    ],
    "gpl": [
        "General Public License",
        "GPL"
    ],
    "lgpl": [
        "Lesser General Public License",
        "LGPL"
    ],
    "mit": [
        "MIT"
    ],
    "mpl": [
        "Mozilla Public License",
        "MPL[- ]2.0"
    ]
}

# create logger
log_file = 'collect_repo_licenses.log'
logger = logging.getLogger('rep_license')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler(log_file)
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
ts = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('%(asctime)s  %(levelname)s  %(message)s', ts)
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


# grab settings for github and mysql from history_git
conf = ConfigParser.ConfigParser()
conf.read(os.path.expanduser('~/.history_git/settings.conf'))

gh = github.Github(login_or_token = conf.get('github', 'user'),
                   password = conf.get('github', 'passwd'))

con = MySQLdb.connect(host=conf.get('mysql', 'host'),
                      user=conf.get('mysql', 'user'),
                      passwd=conf.get('mysql', 'passwd'),
                      db=conf.get('mysql', 'db'),
                      charset='utf8')
cur = con.cursor()

# create table to store results
cur.execute("DROP TABLE IF EXISTS repo_license;")
create_table = """
    CREATE TABLE repo_license (
        owner_repo  TINYTEXT NOT NULL,
        license     CHAR(6) NOT NULL
    );
"""
cur.execute(create_table)


### start searching for licenses!
for res in gh.search_repositories("GNU GENERAL PUBLIC LICENSE"):
    print(res)


