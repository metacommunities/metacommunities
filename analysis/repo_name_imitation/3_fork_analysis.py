
# coding: utf-8

# In[24]:

get_ipython().magic(u'load_ext autoreload')
get_ipython().magic(u'autoreload 2')


# In[25]:


import fork_plotting as fp
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys
import seaborn

seaborn.set_style("whitegrid")
seaborn.set_style("ticks")
seaborn.despine(trim=True)

testing = False
fork_count = 333
if testing:
    repo_name = 'bootstrap'
else:
    repo_name = sys.argv[1]
    fork_count = sys.argv[2]

print 'loading {} repository fork data and grouping by weeks'.format(repo_name)
fork_df, fork_week = fp.load_fork_dataframe_and_group_by_week('data/{}_fork_events.csv'.format(repo_name))

# for low count forks, use the actual numbers of forks
if fork_df['repository_url'].unique().shape[0] < fork_count:
    fork_count = fork_df['repository_url'].unique().shape[0]

print 'plotting {} {} repository forks'.format(fork_count, repo_name)
plt.figure(figsize = (16,10))
fp.fork_stackplot(repo_name, fork_week, fork_count)
plt.title('{0} {1} and related repository forks since 2012'.format(fork_count, repo_name))
plt.ylabel('forks/week')
plt.savefig('plots/{0}_stackplot_{1}.png'.format(repo_name, datetime.datetime.strftime(datetime.datetime.now(), format = '%Y-%m-%d-%H-%M')))
plt.savefig('plots/{0}_stackplot_{1}.svg'.format(repo_name, datetime.datetime.strftime(datetime.datetime.now(), format = '%Y-%m-%d-%H-%M')))
plt.close()

print 'plotting {} repo forks without {} itself'.format(fork_count, repo_name)
plt.figure(figsize = (16,10))
forks_minus_repo_name = fork_week[fork_week.index.get_level_values(0) !=repo_name]
fp.fork_stackplot(repo_name, forks_minus_repo_name)
plt.ylabel('forks/week')

plt.title('{0} {1}-related repository forks since 2012'.format(fork_count, repo_name))
plt.savefig('plots/{0}_stackplot_no_{0}_{1}.png'.format(repo_name, datetime.datetime.strftime(datetime.datetime.now(), format = '%Y-%m-%d-%H-%M')), figsize=(10,12))
plt.savefig('plots/{0}_stackplot_no_{0}_{1}.svg'.format(repo_name, datetime.datetime.strftime(datetime.datetime.now(), format = '%Y-%m-%d-%H-%M')), figsize=(10,12))
plt.close()

print 'finished plots'
