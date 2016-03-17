# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn
import github as gh
import scipy.spatial.distance as dist
import scipy.cluster.hierarchy as hier

# <markdowncell>

# # Analysis of repositories in terms of how geography, temporality and networks create Github as a platform
# 
# The question I am after here is: **how much can we tell about Github as a hub or platform from the work that Github team/staff do on it?** 

# <markdowncell>

# ## Load the data

# <codecell>

#Load team description: I added the countries in manually, so load this to see team members (including )
team_df = pd.read_csv('data/github_team_with_countries.csv', sep='\t')

# Load team repository descriptions
all_team_repos = pd.read_csv('data/github_team_repos.csv', sep='\t')

# Load general event descriptions
all_events = pd.read_csv('data/event_counts_top100k.csv', sep = '\t')

# <markdowncell>

# ## Claims about decentralized work
# 
# Github claims to be about remote working from many places

# <codecell>

country_counts = team_df.country.value_counts()
print 'There are {} different countries in the team'.format(country_counts.shape)
fig1 = plt.figure(figsize = (12,10))
fig1.add_subplot(121)
country_counts.plot(kind='barh',title = 'Locations of Github team (countries)')
fig1.add_subplot(122)
city_counts = team_df.location.value_counts()
sp = city_counts.plot(kind='barh', title = 'Locations of Github team (cities)')

# <codecell>

fig1.savefig('plots/locations.svg')
fig1.savefig('plots/locations.png')

# <codecell>


team_df[['name', 'login', 'id', 'created_at', 'followers', 'location']].sort([ 'followers', 'created_at'], ascending=False).head(20)
# team_df.followers.hist(bins=100)

# <markdowncell>

# ## Weighting the events
# 
# The Github team has produced around 350k events since early 2012 working on 17000 repositories. 

# <codecell>

# to weight the events 

evts = all_team_repos.groupby('type')['event_count'].sum()


print 'Roughly {} events have been performed by the Github team on {} repositories'.format(evts.sum(), +
               len(all_team_repos.repository_url.unique()))

print("The repo events in descending order")

evts = evts.order(ascending=False)
print evts
# plot the events in barchart

# <codecell>

fig1a = plt.figure(figsize=(10,6))
colrs = 'rgbkymc' 
y_pos = np.arange(evts.shape[0])
plt.barh(y_pos, evts)
plt.yticks(y_pos, evts.index)

plt.title('Event types on Github team public repositories')

# <codecell>

sp1a = evts.plot(kind='barh', title = 'Event counts for Github team', colors=colrs)

# <codecell>

fig1a.savefig( 'plots/events_github_team.svg')
fig1a.savefig( 'plots/events_github_team.png')

# <codecell>


# repo count by URLs
repos_by_event_count = all_team_repos.groupby('repository_url')['event_count'].sum().order(ascending=False)
fig2 = plt.figure(figsize=(14,10))
fig2.add_subplot(121)

sp1 = repos_by_event_count[:50].plot(kind='barh', title = 'Repositories worked on by Github team (since 2012)', color='r')
sp1.set_xlabel('Number of events')
sp1.set_ylabel('Repository url')
## to focus on repo names
repo_name_by_event_count = all_team_repos.groupby('repository_name')['event_count'].sum().order(ascending=False)
fig2.add_subplot(122)
sp2 = repo_name_by_event_count[:50].plot(kind='barh', 
                                        title = 'Unique Repositories worked on by Github team (since 2012)', color = 'g')
sp2.set_xlabel('Number of events')
sp2.set_ylabel('Repository name')

# <codecell>

fig2.savefig('plots/github_team_repos_by_event_count.svg')
fig2.savefig('plots/github_team_repos_by_event_count.png')

# <markdowncell>

# ## Collaborative work on repos
# 
# 2 main questions here:
# 
# 1. which actors work together (and does this relate to geography)?
# 2. which repositories link different actors together?
# 
# 
# Need to transform data so that it has a row for each actor and columns for each repository name, with counts of events on each repo

# <codecell>

# choose top 100 repos by total event count

top_repos = repos_by_event_count.index[:300]
top_repo_events = all_team_repos.ix[all_team_repos['repository_url'].isin(top_repos.values.tolist())]

# <codecell>

top_repo_events.ix[:,[1,3,4,2]].head(20)

# <codecell>

#sum all the events for each actor for each repository
actor_top_repos = top_repo_events.groupby(['actor', 'repository_name'])['event_count'].sum().reset_index()
actor_top_repos.head()

# <codecell>

# put actor and repos into wide format
actor_repos_df = actor_top_repos.pivot(index='actor', columns = 'repository_name', values = 'event_count')
actor_repos_df.fillna(0, inplace=True)
actor_repos_df.to_csv('data/actor_repos_top_wide.csv', sep='\t')
actor_repos_df.shape

# <codecell>

#to get event counts for each actor across all repos
actor_repos_df.sum(axis=1).order(ascending=False)[:30]

# <codecell>

# calculate distance matrix between actors
actor_distances = dist.pdist(actor_repos_df.values,'canberra')
dist.squareform(actor_distances)[10]

# <codecell>

actor_distances[:10]

# <codecell>

fig3 = plt.figure(figsize=(12,20))
link_matrix = hier.linkage(actor_distances, method='average')
# hier.fcluster(link_matrix)

dendro = hier.dendrogram(link_matrix, orientation='right',labels = actor_repos_df.index.values)

# <codecell>

# to look at actor-actor neighbours more directly
actor_actor_df = actor_repos_df.dot(actor_repos_df.transpose())
actor_actor_df.fillna(0, inplace=True)
actor_actor_df.head()
actor_actor = actor_actor_df.values
np.fill_diagonal(actor_actor, 0)
actor_actor_df_zeroed = pd.DataFrame(actor_actor, columns = actor_actor_df.columns, index = actor_actor_df.index)
actor_actor_df_zeroed.head()
actor_actor_df_zeroed.to_csv('data/actor_actor.csv', sep='\t')

# <codecell>

actor_actor_df_zeroed.index.name = 'actor1'
# actor_actor_df_zeroed.columns.name = 'actor2'

# <codecell>

#stack the actor-actor relations
actor_actor_stacked = actor_actor_df_zeroed.stack()

# <codecell>

actor_actor_stacked_df = pd.DataFrame(actor_actor_stacked)
actor_actor_stacked_df.head()

# <codecell>

# to look at repo-repo connections more directly
repo_repo_df = actor_repos_df.transpose().dot(actor_repos_df)
repo_repo_df.fillna( 0, inplace=True)
repo_repo_df.head()

# <codecell>

repo_repo = repo_repo_df.values
np.fill_diagonal(repo_repo, 0)
repo_repo_df_zeroed = pd.DataFrame(repo_repo, columns = repo_repo_df.columns, index = repo_repo_df.index)
repo_repo_df_zeroed.head()
repo_repo_df_zeroed.to_csv('data/repo_repo.csv', sep='\t')

# <markdowncell>

# ## Events might be distributed differently for different members of the team

# <codecell>

all_team_repos.columns
all_team_repos.head()

# <codecell>

events_by_team = all_team_repos.groupby(['type', 'actor'])['event_count'].sum()

# <codecell>

events_by_team['PullRequestEvent'].order(ascending=False).head()

# <codecell>

events_by_team['PushEvent'].head()

# <codecell>

ct = pd.crosstab(all_team_repos.actor, all_team_repos.repository_name)
ct.shape

# <codecell>

evt_df.head(30)
evt_df['event_count_log'] = np.log10(evt_df.event_count.values)
evt_df.event_count_log.plot()

