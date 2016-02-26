# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Repository census
# 
# A basic count of the number of distinct repositories in the timelines is a baseline for this work. It is somewhere around 10 million. 

# <codecell>

import redis
import matplotlib.pyplot as plt, mpld3
import seaborn
from bs4 import BeautifulSoup
import pandas as pd
import re
mpld3.enable_notebook()

# <codecell>

red = redis.Redis(db='1')

# <codecell>

repo_table = 'metacommunities:github_proper.repo_list'

query = """SELECT count(distinct(repository_url)) FROM [githubarchive:github.timeline] 
"""

repo_count_df = pd.io.gbq.read_gbq(query)
repo_count_df.ix[0]

# <codecell>

red.set('repos:count_timeline', repo_count_df.ix[0].values[0])

# <codecell>

query_sample = """select repository_owner, repository_name,
if (hash(repository_url) % 100000 == 0, 'True', 'False') as included
from [githubarchive:github.timeline]  limit 100"""
repos_sample = pd.io.gbq.read_gbq(query_sample)
repos_sample.head(10)

# <markdowncell>

# We know that there are more on Github, but this is a reasonable number to work with -- 10M. 

# <codecell>

query = """SELECT count(distinct(full_name)) FROM [metacommunities:github_proper.repo_list] 
"""

full_repo_count_df = pd.io.gbq.read_gbq(query)

# <codecell>

full_repo_count_df.ix[0].values[0]

# <codecell>

print full_repo_count_df.ix[0]
red.set('repos:count_api', full_repo_count_df.ix[0].values[0])

