#!/usr/bin/env python

import ConfigParser
import github_events as ge
import logging
import os


# dot folder for settings and log files
hg_path = os.path.expanduser('~/.history-git')

# initiate logger
logging.basicConfig(filename=os.path.join(hg_path, 'loggy.log'),
  level=logging.DEBUG)
logging.info("Starting...")

# load settings
config = ConfigParser.ConfigParser()
config.read(os.path.join(hg_path, 'settings.conf'))

# load list of repos to get history for
repo_file = 'repo_list'
repo = [line.rstrip('\n') for line in open(repo_file)]

logging.info("Collecting backlog for %i repos" % (len(repo)))

# start the retrieval run using the History Git
history_git = ge.HistoryGit(config, drop_db=True)

# testing
# 1
owner_repo = 'eru/dotfiles'
history_git.get(owner_repo)
# 2
owner_repo = 'metacommunities/metacommunities'
history_git.get(owner_repo)
# 3
owner_repo = 'torvalds/linux'
history_git.get(owner_repo)

