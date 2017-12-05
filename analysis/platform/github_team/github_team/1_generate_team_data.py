# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%load_ext autoreload
%autoreload 2

# <markdowncell>

# # Generate data on Github team

# <codecell>

from bs4 import BeautifulSoup
import pandas as pd
import urllib2
import seaborn
import ConfigParser
import github as gh

# <codecell>

#set up API access
#config file assumed to be in your home directory 
config = ConfigParser.ConfigParser()
config.read('/home/mackenza/.history_git/settings.conf')

user = config.get('github', 'user')
password = config.get('github', 'password')
github = gh.Github(user, password)

# <codecell>

# get the Github team page and scrape all urls
url = 'https://github.com/about/team'
resp = urllib2.urlopen(url)
soup = BeautifulSoup(resp.read(), from_encoding=resp.info().getparam('charset'))
links = []
for link in soup.find_all('a', href=True):
        links.append(link['href'])

# choose the URLS that are actually team names
team = links[12:]
team = team[:233]
team.append('/mojombo')
team = [t.replace('/', '') for t in team]

# <markdowncell>

# ## Retrieve data on Github team from Github API

# <codecell>

# use Github API to get data on these users -- only 230 of them, so not too hard
pre = 'https://github.com'
team_urls = [pre+t for t in team]
# this will take a few minutes as it relies on the GitHub API
team_df = pd.DataFrame([github.get_user(t).raw_data for t in team])
team_df.to_csv('data/github_team.csv', encoding='utf-8', sep='\t')

# <markdowncell>

# ## Retrieve repos used by the Github team

# <codecell>

# retrieve repo event activity for members of the team
def retrieve_repo_event_summary_from_BigQuery(team_list):
    # to retrieve all repositories and events for each team member
    # use Google BigQuery githubarchive timeline

    query = """SELECT actor, repository_url, type, count(type) as event_count 
                    FROM [githubarchive:github.timeline]
                     where  actor = '{}' group each by actor, repository_url, type order by event_count desc LIMIT 1000"""
    all_team_repos = pd.DataFrame()
    for t in team_list:
        team_query = query.format(t)
        print team_query
        df = pd.io.gbq.read_gbq(team_query)
        print df.shape
        all_team_repos = pd.concat([all_team_repos, df])
    print 'retrieved {} repositories for {} github users'.format(all_team_repos.shape[0], len(team_list))
    return all_team_repos

# <codecell>

# running this line will take quite a while as it is querying BigQuery several hundred times
all_team_repos = retrieve_repo_event_summary_from_BigQuery(team_df.login.values)
all_team_repos.to_csv('data/github_team_repos.csv', sep='\t')

# <markdowncell>

# ## Generate summary of events sorted by actor
# 
# This list of top 10,000 actors is just to help sort out where the Github team fits in the overall activity on Github. 

# <codecell>

evt_query = """SELECT actor, count(type) as event_count FROM [githubarchive:github.timeline] 
group each by actor
order by event_count desc
LIMIT 100000"""

evt_df = pd.io.gbq.read_gbq(evt_query)

# <codecell>

evt_df.to_csv('data/event_counts_top100k.csv', sep='\t')

