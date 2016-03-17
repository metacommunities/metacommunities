# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import os.path
import seaborn
import sys

testing = False

if testing:
    repo_name = 'bootstrap'
else:
    repo_name = sys.argv[1]

file_name = 'data/{}_fork_events.csv'.format(repo_name)


# configure graphics
seaborn.set_style("whitegrid")
seaborn.set_style("ticks")
seaborn.despine(trim=True)

# get repo forks from BigQuery
# this assumes you setup access to the BigQuery githubarchive dataset

query = """SELECT repository_url, repository_name, created_at FROM 
[githubarchive:github.timeline] where type='ForkEvent' and lower(repository_name) 
contains '{}'order by created_at asc""".format(repo_name)

if os.path.isfile(file_name):
    forks = pd.read_csv(file_name, header=False)
    print 'reading ' + file_name
else:
    forks= pd.io.gbq.read_gbq(query)
    #local saving and loading
    forks.drop_duplicates(inplace=True)
    print 'writing BigQuery results to {}'.format(file_name)
    forks.to_csv(file_name, index=False)


def plot_overall_growth(forks, repo_name, cumulative = False):
    """ Plots the number of forks created
    per week for the given repository"""
    ts = forks['repository_name']
    ts.index = pd.to_datetime(forks['created_at'])
    if cumulative:
        ts.resample('W', how='count').cumsum().plot(label=repo_name, linewidth=3.0)
    else:
        ts.resample('W', how='count').plot(label=repo_name, linewidth=3.0)
    plt.title('{} repository fork growth'.format(repo_name))
    plt.ylabel('Repository forks')
    plt.xlabel('Date created')

def plot_growth_by_repos(forks):
    forks_count = forks.groupby('repository_name').count()
    forks_count_top = forks_count[forks_count>100]
    most_forked_repos = forks_count_top.index.values.tolist()
    top_forks_set = forks.set_index('repository_name').ix[most_forked_repos]
    return top_forks_set

#top_forks_set = plot_growth_by_repos(forks)
plot_overall_growth(forks, repo_name)
plt.legend(loc='upper left')
plt.savefig('plots/{}_fork_growth.png'.format(repo_name), figsize=(10,12))
plt.close()
