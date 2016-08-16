# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import github as gh
import redis
import pandas as pd
import ConfigParser
import os

path = '/home/mackenza/.history_git/'
conf = ConfigParser.ConfigParser()
conf.read(os.path.join(path, 'settings.conf'))
# github
gh = gh.Github(login_or_token = conf.get('github', 'user'),
                        password = conf.get('github', 'password'))

# <markdowncell>

# ## A heavily forked repo -- octocat/Spoon-Knife

# <codecell>

spoon = gh.get_repo('octocat/Spoon-Knife')
forkcount = spoon.forks_count
pages = forkcount/30
forks = spoon.get_forks()

# <codecell>

fork_repos = []
for page in range(0, pages):
    print 'getting page {}'.format(page)
    fs = forks.get_page(page)
    fork_repos.extend(fs)
    

# <codecell>

r = fork_repos[0]
r.created_at

