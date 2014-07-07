# coding: utf-8
import fork_plotting as fp
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys
import seaborn

testing = False

if testing:
    repo_name = 'bootstrap'
else:
    repo_name = sys.argv[1]


fork_df, fork_week = fp.load_fork_dataframe_and_group_by_week('data/{}_fork_events.csv'.format(repo_name))
print 'plotting {} repository forks'.format(repo_name)
forkcount = 333
if fork_df['repository_url'].unique().shape[0] < forkcount:
    forkcount = fork_df['repository_url'].unique().shape[0]
plt.figure(figsize = (16,10))
fp.fork_stackplot(fork_week, forkcount)
plt.title('{} {} and related repository forks since 2012'.format(forkcount, repo_name))
plt.ylabel('forks/week')
#plt.show()
plt.savefig('plots/{0}_stackplot_{1}.png'.format(repo_name, datetime.datetime.strftime(datetime.datetime.now(), format = '%Y-%m-%d-%H-%M')))
plt.close()

print 'plotting {} repo forks without {} itself'.format(forkcount, repo_name) 
plt.figure(figsize = (16,10))
forks_minus_repo_name = fork_week[fork_week.index.get_level_values(0) !=repo_name]
fp.fork_stackplot(forks_minus_repo_name)
plt.title('{} {}-related repository forks since 2012'.format(forkcount, repo_name))
plt.ylabel('forks/week')
#plt.show()

plt.savefig('plots/{0}_stackplot_no_{0}_{1}.png'.format(repo_name, datetime.datetime.strftime(datetime.datetime.now(), format = '%Y-%m-%d-%H-%M')))
plt.close()
