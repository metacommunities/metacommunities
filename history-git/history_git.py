#!/usr/bin/env python

import github_api as ga
import os
import sys
import urllib

# dot folder for settings and log files
hg_path = os.path.expanduser('~/.history_git')

# initiate logger
logger = ga.create_logger(hg_path)

# Start
logger.info("Starting...")
history_git = ga.HistoryGit(hg_path) # drop_db=True

# Try to add names of any new repos to the repo table
#history_git.get_repo_names()

# Are there any specific repos that we need to collect info for?
owner_repo_file = 'owner_repo.txt'
owner_repo = [line.rstrip('\n') for line in open(owner_repo_file)]

# Add any 'owner/repo's from the command line
owner_repo.extend(sys.argv[1:])

# Start backlog for specific repos
logger.info("Collecting backlog for %i repos" % (len(owner_repo)))

try:
  for rp in owner_repo:
    history_git.get(rp)
except:
  logger.error("Lol, your code is the worst.")
  raise

# history_git.create_repo_summary(owner_repo)

# after downloading activity, would user like to upload this to BigQuery?
history_git.ask_upload()
