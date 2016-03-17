# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from bs4 import BeautifulSoup
import pandas as pd
import urllib2
import seaborn
import ConfigParser
import github as gh

# <codecell>

#Load team description: I added the countries in manually, so load this to see team members (including )
team_df = pd.read_csv('data/github_team_with_countries.csv', sep='\t')

# Load team repository descriptions
all_team_repos = pd.read_csv('data/github_team_repos.csv', sep='\t')

# Load general event descriptions
all_events = pd.read_csv('data/event_counts_top100k.csv', sep = '\t')

# <markdowncell>

# ## Clean up countries and cities

# <codecell>

team_df['location'] = team_df.location.str.lower().str.replace(',.*', '')

# <codecell>

team_df.to_csv('data/github_team_with_countries.csv', sep='\t')

# <markdowncell>

# ## Clean up team repos names

# <codecell>

all_team_repos['repository_name'] = all_team_repos['repository_url'].str.replace('.*/', '')
all_team_repos.to_csv('data/github_team_repos.csv')

