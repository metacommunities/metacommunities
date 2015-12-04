from bs4 import BeautifulSoup
import ConfigParser
import requests
import logging
import MySQLdb
import os
import re

path = {
    'readme':  "+path:readme&type=Code",
    'license': "+path:license&type=Code",
    'copying': "+path:copying&type=Code",
    'meta': "&type=repo"
}


#Dictionary of the main families of open source licenses. Each family
#contains the regular expressions that will be used to identify if a repo
#uses a license from that particular family.
license = {
    "apache": [
        "Apache License 2.0",
        "Apache-License-2.0",
        "Apache-2.0",
        "Apache 2.0",
        "Apache2.0"
    ],
    "bsd": [
        "BSD 3"
        "BSD-3",
        "BSD3",
        "BSD Simplified",
        "BSD-Simplified",
        "Simplified-BSD",
        "Simplified BSD",
        "BSD-New",
        "BSD New",
        "BSD 2",
        "BSD-2",
        "BSD2",
        "FreeBSD"
    ],
    "cc": [
        "Creative Commons",
        "CC BY",
        "CC BY-SA",
        "CC BY SA",
        "CC BY-ND",
        "CC BY ND",
        "CC BY-NC",
        "CC BY NC",
        "CC BY-NC-SA",
        "CC BY NC SA",
        "CC BY-NC-ND",
        "CC BY NC ND"
    ],
    "epl": [
        "Eclipse Public License",
        "EPL 1.0",
        "EPL-1.0",
        "EPL1.0"
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
        "MPL 2.0",
        "MPL-2.0",
        "MPL2.0"
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
repos = []

url_base  = "https://github.com/search?q="

license_keys = license.keys()
license_keys.sort()

for lk in license_keys:
    for query in license[lk]:
        for pth in path:
            url_main = "%s'%s'%s" % (url_base, query, pth)
            page=1
            
            while True:
                url = "%s&p=%i" % (url_main, page)
                r = requests.get(url)
                r.raise_for_status()
                soup = BeautifulSoup(r.text)
                
                for result in soup.find_all("div", class_="code-list-item public "):
                    title  = result.find("p", class_="title")
                    repo = re.search(ur'\n(.*) \u2013', title.text).group(1)
                    repo = str(repo)
                    repos.append((repo, lk))
                
                page += 1

