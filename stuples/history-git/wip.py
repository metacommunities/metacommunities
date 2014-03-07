#!/usr/bin/env python

import ConfigParser
import github
import MySQLdb
import os
import time

hg_path = os.path.expanduser('~/.history-git')

# conf
conf = ConfigParser.ConfigParser()
conf.read(os.path.join(hg_path, 'settings.conf'))

gh = dict(conf.items('github'))

## START!
# other get_* functions:
# get_branches            # repo: maybe count the number of branches?
# get_collaborators
# get_comments
# get_commits             # Done!
# get_contributors        # list of users who own a commit?
# get_forks               # Done!
# get_issues              # Done!
# get_issues_events       # dont bother
# get_issues_comments     # dont bother
# get_languages           # repo: useful for repo info
# get_pulls               # Done!

g = github.Github(gh['usr'],gh['pwd'],timeout=20)

# carry on from previous scrapping by setting "since = max repo id"

repos = []
for rp in g.get_repos():
  repos.append(rp)
  break















owner = "metacommunities"
repo = "metacommunities"

owner = "hadley"
repo = "ggplot2"

owner_repo = '/'.join([owner, repo])

repo = g.get_user(owner).get_repo(repo)

ts = [time.time()]
events = []
n = 0
for eve in repo.get_pulls(state="all"):
  events.append(eve)
  n += 1
  if n == 1000:
    break

[ eve.state for eve in events ]

ts.append(time.time())

1 / ((ts[1] - ts[0]) / len(events))

# duration of a pull request
duration = [ eve.closed_at - eve.created_at  for eve in events ]
[ dur.days for dur in duration ]


