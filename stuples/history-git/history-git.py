#!/usr/bin/env python

import ConfigParser
import github_api_events as ghe
import logging
import os
import requests
import textwrap

# dot folder for settings and log files
hg_path = os.path.expanduser('~/.history-git')

# initiate logger
logging.basicConfig(filename=os.path.join(hg_path, 'loggy.log'),
  level=logging.DEBUG)
logging.info("Starting...")

# load settings
config = ConfigParser.ConfigParser()
config.read(os.path.join(hg_path, 'settings.conf'))

# does the database exist? if not then create it
ghe.create_db(config=dict(config.items('mysql')))

# load list of repos to get history for
repo_file = 'repo_list'
repo = [line.rstrip('\n') for line in open(repo_file)]

logging.info("Collecting backlog for %i repos" % (len(repo)))

# request limiter (this should eventually become part of the requester)
limiter = ghe.RequestLimiter(auth=dict(config.items('github')))


# what was the last observed date for this repo in BigQuery?




# design requester

owner_repo = 'metacommunities/metacommunities'
page = 1
url = 'https://api.github.com/repos/%s/events?page=%i' % (owner_repo, page)

# the general approach is to slowly go further and further back in time
# collecting all events

# so first we need to see if we have *any* events in the database for the
# given repo and if so what is the earliest timestamp



# connect to db
config = dict(config.items('mysql'))

con = MySQLdb.connect(host=config['host'], user=config['usr'],
  passwd=config['pwd'], db=config['db'])
cur = con.cursor()


# get a page

#if limiter.ok:

pg = requests.get(url, auth=(config.get("github", "usr"),
  config.get("github", "pwd")))

limiter.update()

# is page good?
if pg.status_code == requests.codes.ok:
  event_sql    = "INSERT INTO mytable (a,b,c) VALUES (%(qwe)s, %(asd)s, %(zxc)s);"
  commmits_sql = "INSERT INTO mytable (a,b,c) VALUES (%(qwe)s, %(asd)s, %(zxc)s);"
  
  # process the page
  pg = pg.json()
  for event in pg:
    info = ghe.extract_event_info(event)
    # save to the db
    cursor.execute(event_sql, info['event'])
    if not commits:
      cursor.execute(commits_sql, info['commits'])









cursor.close()
con.close()

