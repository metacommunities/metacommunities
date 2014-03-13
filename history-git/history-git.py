#!/usr/bin/env python

import github_events as ge
import logging
import os
import urllib

# dot folder for settings and log files
hg_path = os.path.expanduser('~/.history-git')

# initiate logger
log_file = os.path.join(hg_path, 'history_git.log')
logger = logging.getLogger('history_git')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler(log_file)
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s  %(levelname)s  %(message)s',
                              '%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

# Start
logger.info("Starting...")
history_git = ge.HistoryGit(hg_path) # drop_db=True

# Add any new repos to the repo table
while True:
  try:
    history_git.populate_repo()
    break
  except urllib.error.URLError, e:
    logger.error(e.reason)
    logger.info("Sleep for 10 minutes.")
    time.sleep(600) # 10 mins
    logger.info("Trying again.")
    pass


# Are there any specific repos that we need to collect info for?
owner_repo_file = 'owner_repo_list'
owner_repo = [line.rstrip('\n') for line in open(owner_repo_file)]

logger.info("Collecting backlog for %i repos" % (len(owner_repo)))

try:
  for rp in owner_repo:
    history_git.get(rp)
except:
  logger.error("Lol, your code is the worst.")
  raise
