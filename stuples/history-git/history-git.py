#!/usr/bin/env python

import github_events as ge
import logging
import os

# dot folder for settings and log files
hg_path = os.path.expanduser('~/.history-git')

# initiate logger
logging.basicConfig(filename=os.path.join(hg_path, 'loggy.log'),
  level=logging.INFO)
logging.info("Starting...")

# load list of repos to get history for
repo_file = 'repo_list'
repo = [line.rstrip('\n') for line in open(repo_file)]

logging.info("Collecting backlog for %i repos" % (len(repo)))

# start the retrieval run using the History Git
history_git = ge.HistoryGit(hg_path, drop_db=True)

# testing
# 1
owner_repo = 'metacommunities/metacommunities'
history_git.get(owner_repo)
# 2
#owner_repo = 'hadley/ggplot2'
#history_git.get(owner_repo)
# 3
#owner_repo = 'torvalds/linux'
#history_git.get(owner_repo)
