# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import github as gh
import redis
import time
import ConfigParser
import os

path = '/home/mackenza/.history_git/'
conf = ConfigParser.ConfigParser()
conf.read(os.path.join(path, 'settings.conf'))
# github
git = gh.Github(login_or_token = conf.get('github', 'user'),
                        password = conf.get('github', 'password'))

red = redis.Redis(db ='1')

def get_creation_dates(query, number):
    repos = red.srandmember(query,number)
    repo_dates = {}
    for r in repos:
        try:
            res = git.get_repo(r)
            # print res.created_at
            #store datetime as milliseconds since epoch
            # to reverse: time.gmtime(t)
            repo_dates[r] = time.mktime(res.created_at)
        except Exception, e:
            print e
    return repo_dates

# <codecell>

## get creation dates for 100000 server projects

number = 10000
rdates = get_creation_dates('servers', number)

