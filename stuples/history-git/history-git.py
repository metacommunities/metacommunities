#!/usr/bin/env python

import ConfigParser
import github_events as ge
import logging
import os
import MySQLdb
import requests
import textwrap
import time

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
ge.create_db(config=dict(config.items('mysql')))

# load list of repos to get history for
repo_file = 'repo_list'
repo = [line.rstrip('\n') for line in open(repo_file)]

logging.info("Collecting backlog for %i repos" % (len(repo)))

# request limiter (this should eventually become part of the requester)
limiter = ge.RequestLimiter(auth=dict(config.items('github')))


# earliest timestamp on the github archive on BigQuery
bq_start = '2012-03-11 06:36:13'
bq_start = time.mktime(time.strptime(bq_start, '%Y-%m-%d %H:%M:%S'))


# design requester

owner_repo = 'metacommunities/metacommunities'
url_base = 'https://api.github.com/repos/%s/events?page=%i'

# the general approach is to slowly go further and further back in time
# collecting all events

# so first we need to see if we have *any* events in the database for the
# given repo and if so what is the earliest timestamp. If there is a timestamp
# we'll assume that we have collected all events between that timestamp and
# the current date.



# connect to db
con = MySQLdb.connect(host=config.get("mysql", "host"),
  user=config.get("mysql", "usr"), passwd=config.get("mysql", "pwd"),
  db=config.get("mysql", "db"))
cur = con.cursor()

# any previous history
sql_prev_hist = """
  SELECT min(created_at)
  FROM event 
  WHERE owner_repo = '%s'
""" % (owner_repo)

cur.execute(sql_prev_hist)

start_ts = cur.fetchone()[0]

if not start_ts:
  start_ts = bq_start

# get a page
# ==========

#if limiter.ok:

page = 1

url = url_base % (owner_repo, page)

pg = requests.get(url, auth=(config.get("github", "usr"),
  config.get("github", "pwd")))

limiter.update()

# is page good?
#if pg.status_code == requests.codes.ok:
event_sql    = "INSERT INTO mytable (a,b,c) VALUES (%(qwe)s, %(asd)s, %(zxc)s);"
commmits_sql = "INSERT INTO mytable (a,b,c) VALUES (%(qwe)s, %(asd)s, %(zxc)s);"

# process the page
pg = pg.json()

# any events with a date before start_ts? if so process and save them.
keep_events = []
for i, event in enumerate(pg):
  # convert timestamp to unix timestamp
  event_ts = time.mktime(time.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ'))
  if event_ts < start_ts:
    # process the event
    info = ge.extract_event_info(event)
    # save
    cur.execute(event_sql, info['event'])
    # if event was a push event then we need to also save the commits
    if not info['commits']:
      cur.execute(commits_sql, info['commits'])
  

if keep_events:

else:










cursor.close()
con.close()

