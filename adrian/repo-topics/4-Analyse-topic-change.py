# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ## Changing relations between domains over time
# 
# Do domain combine differently over time?

# <codecell>

%load_ext autoreload
%autoreload 2

# <codecell>

import redis
import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import re
import itertools
import numpy as np
import ConfigParser
import github as gh

# <codecell>

sys.path.append('..')
import RedisRepos as rr

# <codecell>

config = ConfigParser.ConfigParser()
config.read('/home/mackenza/.history_git/settings.conf')

user = config.get('github', 'user')
password = config.get('github', 'password')
gha = gh.Github(user, password)

# <codecell>

red  = redis.Redis(db='1')
rrr = rr.Repos()

# <codecell>

soc_sampe = rrr.load_repo_collection('repos:social_media')

# <codecell>

soc_sampe[0:10]

# <codecell>

# soc_sampe = red.srandmember('social_media', 100)
for i in soc_sampe[:10]:
    repos = gha.get_repo(i)
    print repos.created_at

