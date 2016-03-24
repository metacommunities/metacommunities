# coding: utf-8
""" Functions to load and plot repository forks
by creation dates"""


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn

# configure graphics
seaborn.set_style("whitegrid")
seaborn.set_style("ticks")
seaborn.despine(trim=True)


def load_fork_dataframe_and_group_by_week(forkfile = 'data/bootstrap_fork_events.csv'):
    """ Loads a fork dataframe
    @return: the fork dataframe and a dataframe grouped by repostory
    name and week"""

    # forkfile = 'data/bootstrap_fork_events.csv'
    # boot fork dataframe has repo names, repository_url, created_at
    print 'loading fork file' + forkfile
    fork_df = pd.read_csv(forkfile, parse_dates = True,  header=0, sep=',')
    # fork_df.columns
    # fork_df.head()
    fork_df.index = pd.to_datetime(fork_df['created_at'])

    #resample forks by the week
    fork_week = fork_df.groupby('repository_name').resample('W', how='count')
    fork_week.drop('repository_url', axis=1, inplace=True)
    fork_week.columns = ['fork_count']
    # fork_week_name = fork_week.ix[::2]
    # fork_week_name.head()
    # print fork_week_name.shapes
    # fork_week_name.index = fork_week_name.index.droplevel(1)
    return (fork_df, fork_week)

def fork_stackplot(fork, fork_week_name, fork_count=100):
    """ make a stackplot of the top fork_count forks
     using plain count data
    """
    #choose the top ones
    idx = fork_week_name.groupby(level=0).sum() > fork_count
    ind = idx.ix[idx['fork_count'] == True]
    fork_week_top = fork_week_name.ix[ind.index]
    df_fork_wide = fork_week_top.unstack(level=1).replace(np.NaN,0).ix[::2,]
    x3 = df_fork_wide.columns.levels[1]
    y3 = df_fork_wide.values
    plt.stackplot(x3, y3, baseline='sym')


def stackplot_forks_cumulative(fork_week_name, min_fork_count=1000):
    ## repos by cumulative sum
    fork_mcs= fork_week_name.groupby(level=0).cumsum()

    #choose repos with more than 2000 forks
    ind = fork_mcs.groupby(level=0).sum() > min_fork_count
    fork_mcs_top = fork_mcs.ix[ind[ind==True].index]
    df_fork_mcs_toplog = np.log10(fork_mcs_top)


    # for k in df_fork_mcs_toplog.index.levels[0]:
        # plt.plot(fork_mcs_toplog[k], label=k)
        # plt.title('{} repositories with more than {} forks since 2012'.format(fork, min_fork_count))

    # plt.legend(loc='best')
    # plt.show()

    # stackplot using log cumulative summed data
    df_fork_mcs_toplog_filled = df_fork_mcs_toplog.unstack().replace(np.NaN, 0)
    x2 = df_fork_mcs_toplog_filled.columns.levels[1]
    y2 = df_fork_mcs_toplog_filled.values
    plt.stackplot(x2,y2, baseline='sym')



