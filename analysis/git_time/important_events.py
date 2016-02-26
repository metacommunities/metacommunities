# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Important events
# 
# I've got a couple of different candidate of what might be important events:
# 
# 1. the repositories set up and used by Github staff members in 2008 -- what were they for and what do they do today?
# 2. the $100 million venture capital Github received in 2012 --- does this coincide with any growth or change?
# 3. the flagship projects that have moved to Github -- linux, rails, django, etc?

# <markdowncell>

# ## Founding events
# 
# The 270 or so Githubbers (staff) do a lot of things to Github on Github. Given software developers' propensity to work recursively, the early repos set up by these developers might tell us something about the advent of Github itself.
# 
# _Some_ of the user names here are:
# 
# - defunkt
# - drnic
# - halorgium
# - kballard
# - maddox
# - mojombo
# - schacon
# 
# I queried the githubarchive timeline for the 1st 2000 repositories by creation date. This does not guarantee that we have the earliest date as repositories that have no events since April 2011, the start of the timeline dataset, will not appear. But it should give some idea of what people were doing on Github in 2008 when Github first came online. No doubt much work had been done on Github prior to this, but it is very likely that Github developers were using Github itself to do their coding work.  

# <codecell>

import bq
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn
import graphtool
from ggplot import *


# <codecell>

# to get the data from BigQuery
client = bq.Client.Get()

query = "select * from metacommunities:github.TBA"
fields, data = client.ReadSchemaAndRows(client.Query(query)['configuration']['query']['destinationTable'], max_rows = 100000)
colnames = [f['name'] for f in fields]
early_repos_df = pd.DataFrame(data, columns = colnames)

# <codecell>

# load locally cached version of the dataset
early_repos_df = pd.DataFrame.from_csv('../data/repos_1st_2000_created.csv', sep='\t')

# <codecell>

early_repos_df.reset_index(inplace=True)
print(early_repos_df.columns)
early_repos_df.head()

# <codecell>

# converts date to datetimes
early_repos_df.repository_created_at = pd.to_datetime(early_repos_df.repository_created_at)

# <codecell>

early_repos_df.set_index('repository_created_at', inplace=True)

# <markdowncell>

# ## Duplicated or forking of repos
# 
# There are bursts of forking of repos in the first days. Its seems as if small groups were involved in forking certain repos. They are nearly all Ruby language and related to the web development frameworks 'Ruby on Rails.' I guess this is what Github was using (and maybe still is?). 

# <codecell>

# forking of repos  -- what was being forked most
early_repos_df.repository_name.value_counts()[:20]

# <markdowncell>

# Similarly looking at the overall event counts, the repositories that appear to attract most activity, whether in the parent or the fork, have a strongly Ruby feel -- rails, spree, rubinius, paperclip, prawn, haml, 

# <codecell>

early_repos_df['event_count'].groupby(early_repos_df['repository_name']).sum().order(ascending=False)[:30]

# <codecell>

repo_create = early_repos_df.truncate(before = '1/1/2008').groupby(level=0)['repository_name'].count()

# <codecell>

sp = repo_create.plot(figsize = (14,6), title = 'First 2000 repositories created in Github')
la = sp.set_ylabel('number of repositories created')

# <codecell>

by_week = repo_create.groupby(lambda x: x.week).count()
by_week.plot(title = 'Repositories created each week')
sp.plot(by_week)
la = sp.set_ylabel('Repositories created')

