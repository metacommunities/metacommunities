#!/usr/bin/env python

import ConfigParser
import github
import MySQLdb
import numpy as np
import os
import time

hg_path = os.path.expanduser('~/.history-git')

# conf
conf = ConfigParser.ConfigParser()
conf.read(os.path.join(hg_path, 'settings.conf'))

gh = dict(conf.items('github'))

# open connection to mysql
con = MySQLdb.connect(host=conf.get('mysql', 'host'),
                          user=conf.get('mysql', 'usr'),
                          passwd=conf.get('mysql', 'pwd'),
                          db=conf.get('mysql', 'db'))
cur = con.cursor()

## START!
g = github.Github(gh['usr'],gh['pwd'],timeout=20)

owner = "hadley"
repo = "ggplot2"
owner_repo = '/'.join([owner, repo])

repo = g.get_user(owner).get_repo(repo)

# other get_* functions:
# get_forks
# get_commits
# get_issues_events
# get_issues_comments

def clean(cm):
  x = {
    'owner': owner,
    'repo': repo,
    'owner_repo': owner_repo
  }
  
  x['sha'] = cm.sha
  
  if cm.author is None:
    x['author_login'] = cm.commit.author.name
  else:
    x['author_login'] = cm.author.login
  
  x['author_date'] = cm.commit.author.date
  
  if cm.committer is None:
    x['committer_login'] = cm.commit.committer.name
  else:
    x['committer_login'] = cm.committer.login
  
  x['committer_date']  = cm.commit.committer.date
  x['files_n']         = len(cm.files)  
  x['stats_additions'] = cm.stats.additions
  x['stats_deletions'] = cm.stats.deletions
  x['stats_total']     = cm.stats.total
  
  return(x)

ts = [time.time()]
commits = []
for cm in repo.get_commits():
  commit = clean(cm)
  commits.append(commit)

ts.append(time.time())

ts[1] - ts[0]
