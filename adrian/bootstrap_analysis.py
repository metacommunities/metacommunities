# coding: utf-8

import seaborn
import pandas as pd
import matplotlib.pyplot as plt
# get bootstrap forks from BigQuery
query = """SELECT repository_url, repository_name, created_at\nFROM [githubarchive:github.timeline] \nwhere type='ForkEvent' and lower(repository_name) contains 'bootstrap'\norder by created_at asc\nLIMIT 200000"""

#boot= pd.io.gbq.read_gbq(query)

#local saving and loading
boot.to_csv('data/bootstrap_fork_events.csv')
boot = pd.read_csv('data/bootstrap_fork_events.csv', header=False)

boot.drop_duplicates(inplace=True)
boot.created_at = pd.to_datetime(boot.created_at)
boot_fork_countdf = boot.groupby('repository_name').count()
boot.groupby('repository_name')['created_at'].count().order(ascending=False)
#ts.resample('M', how='count').plot()
#ts.resample('D', how='count').plot()
#ts.resample('H', how='count').plot()

def plot_overall_growth():
    ts = boot['repository_name']
    ts.resample('W', how='count').plot()
    plt.title('Bootstrap repository fork growth')


#plot_overall_growth()


def plot_growth_by_repos():
    boot_count = boot.groupby('repository_name').count()
    boot_count_top = boot_count[boot_count>100]
    most_forked_repos = boot_count_top.index.values.tolist()
    top_boot_set = boot.set_index('repository_name').ix[most_forked_repos]
    return top_boot_set

top_boot_set = plot_growth_by_repos()



