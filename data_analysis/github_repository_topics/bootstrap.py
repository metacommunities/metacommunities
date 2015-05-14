# coding: utf-8

import pandas as pd
query = """SELECT repository_url, repository_name, created_at\nFROM [githubarchive:github.timeline] \nwhere type='ForkEvent' and lower(repository_name) contains 'bootstrap'\norder by created_at asc\nLIMIT 200000"""
boot= pd.io.gbq.read_gbq(query)
boot.shape
boot.head
boot.head()
boot.repository_name.value_counts()
boot
boot.created_at.order()
boot.created_at = pd.to_datetime(boot.created_at)
boot.created_at.order()
boot.groupby('created_at').count()
boot.groupby('created_at')
boot.groupby('repository_name').count()
boot.groupby('repository_name').count().order()
boot_fork_countdf = boot.groupby('repository_name').count()
boot_fork_countdf.head()
boot_fork_countdf = boot.groupby('repository_name')['created_at'].min()
boot.groupby('repository_name')['created_at'].min()
boot.groupby('repository_name')['created_at'].max()
boot.groupby('repository_name')['created_at'].range()
boot.groupby('repository_name')['created_at'].mean()
boot.groupby('repository_name')['created_at'].values
boot.groupby('repository_name')['created_at'].values()
boot.groupby('repository_name')['created_at'].min()
boot.groupby('repository_name')['created_at'].count()
boot.groupby('repository_name')['created_at'].count()>1
boot
boot.head()
boot.drop_duplicates().shape
boot.shape
boot.drop_duplicates(inplace=True)
boot.head()
boot.groupby('repository_name')['created_at'].count()
boot.groupby('repository_name')['created_at'].count().order()
boot.groupby('repository_name')['created_at'].count().order(ascending=False)
boot.groupby('repository_name')['created_at'].count().order(ascending=False).sum()
boot.groupby('repository_name')['created_at'].sum()
boot.groupby('created_at')
boot.groupby('created_at')['repository_name'].count()
boot['created_at].groupby(lambda x:x.month)['repository_name'].count()
boot['created_at'].groupby(lambda x:x.month)['repository_name'].count()
boot.set_index(boot['created_at'], inplace=True)
boot.resample('1month')
boot.resample('month')
boot.resample('2hours')
boot.resample('2hr')
boot.resample('D')
boot.resample('D')['repository_name'].count()
boot['repository_name']
ts = boot['repository_name']
type(ts)
type(ts.index)
ts.resample('D')
ts.resample('D', how='count')
ts.resample('M', how='count')
ts.resample('M', how='count').plot()
get_ipython().magic(u'matplotlib')
ts.resample('M', how='count').plot()
import seaborn
ts.resample('M', how='count').plot()
ts.resample('M', how='count').plot()
ts.resample('M', how='count').plot()
ts.resample('W', how='count').plot()
ts.resample('D', how='count').plot()
ts.resample('H', how='count').plot()
ts.resample('H', how='count').plot()
ts.resample('W', how='count').plot()
ts.resample('W', how='count').plot(ylabel='forks')
get_ipython().set_next_input(u"ts.resample('W', how='count').plot");get_ipython().magic(u'pinfo plot')
get_ipython().set_next_input(u"ts.resample('W', how='count').plot");get_ipython().magic(u'pinfo plot')
ts.resample('W', how='count').plot(kind='bar')
ts.resample('W', how='count').plot()
get_ipython().magic(u'history ')
get_ipython().magic(u'pwd ')
get_ipython().magic(u'cd ~/R/metacommunities/adrian/')
get_ipython().magic(u'ls ')
get_ipython().magic(u'lsmagic')
get_ipython().magic(u'pinfo save')
get_ipython().magic(u'lsmagic')
get_ipython().magic(u'who ')
get_ipython().magic(u'pinfo save')
get_ipython().magic(u'pinfo history')
get_ipython().magic(u'history ')
len(history)
len(history())
len(%history)
get_ipython().magic(u'history')
get_ipython().magic(u'history 20')
get_ipython().magic(u'history 0-20')
get_ipython().magic(u'history -20')
get_ipython().magic(u'history 100')
get_ipython().magic(u'pinfo history')
get_ipython().magic(u'history -n')
get_ipython().magic(u'save 0-73 bootstrap_analysis.py')
get_ipython().magic(u'save 0-73')
get_ipython().magic(u"save 0-73 'bootstrap.py'")
get_ipython().magic(u'pinfo %save')
get_ipython().magic(u"save 0-73 'bootstrap.py'")
get_ipython().magic(u'save bootstrap_analysis.py 0-73')
dir
dir()
get_ipython().magic(u'ls ')
get_ipython().magic(u'edit bootstrap_analysis.py')
get_ipython().magic(u'ed bootstrap_analysis.py')
get_ipython().magic(u'ed bootstrap_analysis.py')
ts.resample('W', how='count').plot()
get_ipython().magic(u'ed bootstrap_analysis.py')
ts.resample('W', how='count').plot()
get_ipython().magic(u'ed bootstrap_analysis.py')
ts.resample('W', how='count').plot()
get_ipython().magic(u'ed bootstrap_analysis.py')
get_ipython().magic(u'ed bootstrap_analysis.py')
ts
ts.groupby()
ts['bootstrap']
boot.index
boot.groupby('repository_name').plot()
boot.groupby('repository_name').count()
boot.groupby('repository_name').count() > 4
boot_count = boot.groupby('repository_name').count()
boot_count
boot_count.columns
boot_count.head()
get_ipython().magic(u'pinfo boot.pivot')
boot_count.icol[1]
boot_count.icol(1)
boot_count = boot_count.icol(1)
boot_count
boot_count>4
boot_count[boot_count>4]
boot_count[boot_count>4].order(ascending=False)
boot_count = boot_count[boot_count>4].order(ascending=False)
boot_count.ix[0:100]
get_ipython().magic(u'edit ~/vimcheat.txt')
get_ipython().magic(u"edit '~/vim.txt'")
boot_count.ix[0:100]
get_ipython().magic(u'pinfo pd.DataFrame.sum')
boot.groupby('repository_name')['created_at'].resample('M', how='count')
boot_count.ix[0:100]
boot_count = boot_count[boot_count>100].order(ascending=False)
boot_count.shape
get_ipython().magic(u'history -n')
boot_count
boot_count['repository_name']
boot_count.index
boot_count.index.values()
boot_count.index.values
boot_count.index.values.to_list()
boot_count.index.values.tolist()
most_forked_repos = boot_count.index.values.tolist()
.groupby('repository_name')['created_at'].resample('M', how='count')
get_ipython().magic(u'history -n')
boot.ix[most_forked_repos]
most_forked_repos
boot.ix[most_forked_repos]
boot.ix[most_forked_repos,]
boot.ix[most_forked_repos,:]
boot[most_forked_repos,:]
boot.[most_forked_repos,:]
boot.loc[most_forked_repos,:]
boot.iloc[most_forked_repos,:]
boot.iloc[most_forked_repos]
boot
boot.columns
boot.set_index('repository_name').ix[most_forked_repos]
boot.set_index('repository_name').ix[most_forked_repos].head()
top_boot_set = boot.set_index('repository_name').ix[most_forked_repos].head()
top_boot_set.head()
top_boot_set.tail()
top_boot_set.shape
top_boot_set = boot.set_index('repository_name').ix[most_forked_repos]
top_boot_set.shape
get_ipython().magic(u'history -n')
get_ipython().magic(u'save boot2.py 141-173')
get_ipython().magic(u'edit boot2.py')
get_ipython().magic(u'history -n')
get_ipython().magic(u'edit bootstrap_analysis.py')
get_ipython().magic(u'history -n')
get_ipython().magic(u'edit bootstrap_analysis.py')
boot_count = boot.groupby('repository_name').count()
boot_count>100
get_ipython().magic(u'edit bootstrap_analysis.py')
boot_count_top = boot_count[boot_count>100].order(ascending=False)
boot_count_top = boot_count[boot_count>100]
get_ipython().magic(u'edit bootstrap_analysis.py')
top_boot_set
top_boot_set
top_boot_set.plot()
top_boot_set
type(top_boot_set)
top_boot_set.set_index('created_at', inplace=True)
top_boot_set.plot()
top_boot_set
get_ipython().magic(u'edit bootstrap_analysis.py')
top_boot_set
top_boot_set['dummy'] = 1
top_boot_set
top_boot_set.set_index('created_at', inplace=True)
top_boot_set
top_boot_set.reset_index(inplace=True)
top_boot_set
get_ipython().magic(u'edit bootstrap_analysis.py')
top_boot_set
get_ipython().magic(u'edit bootstrap_analysis.py')
get_ipython().magic(u'edit bootstrap_analysis.py')
top_boot_set
get_ipython().magic(u'edit bootstrap_analysis.py')
top_boot_set
get_ipython().magic(u'edit bootstrap_analysis.py')
top_boot_set.head()
top_boot_set.reset_index()
top_boot_set.reset_index().head()
tbs  =top_boot_set.reset_index()
tbs['created_at'].resample('M', 'count')
tbs = tbs.set_index('created_at')
tbs.head()
tbs.groupby('repository_name').resample('M', how='count')
tbs_month = tbs.groupby('repository_name').resample('M', how='count')
tbs_month.head()
tbs_month..ix[0]
tbs_month.ix[0]
tbs_month.ix[1]
tbs_month.ix[2]
tbs_month.columns
tbs_month[1:10]
tbs_month.head(



/
)
tbs.icol(0:3)
tbs.icol[0:3]
tbs.icol(1)
tbs.icol(0)
tbs['repository_name'].groupby('repository_name').resample('M', how='count')
tbs.col('repository_name').groupby('repository_name').resample('M', how='count')
tbs.ix['repository_name']
tbs.ix[:,'repository_name']
tbs.ix[:,'repository_name'].groupby('repository_name').resample('M', how='count')
tbs.ix[:,'repository_url'].groupby('repository_name').resample('M', how='count')
tbs.ix[:,'repository_name'].groupby('repository_name').resample('M', how='count')
tbs.colums
tbs.columns
tbs_month.head()
tbs_month[tbs_month>1]
tbs_month['bootstrap']
tbs_month['bootstrap']['repository_name']
tbs_month['bootstrap'][:10]
tbs_month['bootstrap'][:10][0]
tbs_month['bootstrap'].cumsum()
tbs_month['bootstrap'].cumsum().plot()
tbs_month['bootstrap'].cumsum()
tbs_month[:10]
get_ipython().magic(u'history -n')
tbs.icol([0,1])
tbs.icol([0,2])
tbs.shape
get_ipython().magic(u'history ')
tbs  =top_boot_set.reset_index()
tbs = tbs.set_index('created_at')
tbs_month = tbs.groupby('repository_name').resample('M', how='count')
tbs.shape
tbs.icol([0,1])
tbs.icol([0,2])
tbs.icol([0,1])
tbs.index
tbs.head()
tbs.icol(1)
tbs.icol(0)
tbs.icol(0).head().groupby('repository_name').resample('M', how='count')
tbs.icol(1).head().groupby('repository_name').resample('M', how='count')
tbs.icol([0,1]).head().groupby('repository_name').resample('M', how='count')
tbs.head().groupby('repository_name').resample('M', how='count')['repository_name']
tbs.head().groupby('repository_name').resample('M', how='count')['repository_url']
tbs.head().groupby('repository_name').resample('M', how='count')[0]
tbs.head().groupby('repository_name').resample('M', how='count')[0:10,0:10]
tbs.head().groupby('repository_name').resample('M', how='count')
tbs.head().groupby('repository_name').resample('M', how='count')
top_boot_set.describe()
top_boot_set.repository_url.unique()
top_boot_set.repository_url.unique().shape
top_boot_set.repository_name.unique().shape
top_boot_set.index
top_boot_set.index.unique().shape
top_boot_set.shape
top_boot_set.head()
get_ipython().magic(u'ls ')
dir()
tbs_month
tbs_month.index
get_ipython().magic(u'pinfo tbs_month.index')
tbs_month.index(levels=0)
tbs_month.index[0]
tbs_month.index[1]
tbs_month.index[2]
tbs_month.index[3]
tbs_month.index[4]
tbs_month.index[5]
tbs_month.index[5][1]
tbs_month.index[:][2]
tbs_month.index[:,2]
tbs_month.index
tbs_month.index.levels
tbs_month.index.levels[0]
tbs_month.index.levels[1]
tbs_month.index.levels[2]
tbs_month.index.levels[:][1]
tbs_month.index.levels[:][0]
tbs_month.index.levels[0]
get_ipython().magic(u'pinfo tbs.groupby')
tbs.groupby(level=0)
tbs.shape
tbs.head
tbs.head()
tbs.groupby(level=0).resample('M', how='count')
tbs.index.levels[0]
tbs.index.level[0]
tbs_month.index
tbs_month.groupby(level=1)['repository_url'].count()
tbs_month.groupby(level=1)['repository_url']
tbs_month.groupby(level=1)
tbs_month.groupby(level=1, 'repository_url')
tbs_month.groupby(level=1).count()
tbs_month.groupby(level=1).cumsum()
tbs_month.groupby(level=1).cumsum()['bootstrap']
tbs_month[0]
tbs_month.ix[0]
tbs_month.ix[0:4]
tbs_month.ix[0:1]
tbs_month.ix[0:2]
tbs_month.ix[0::2]
tbs_month.ix[1::2]
tbs_month.ix[1::2]['bootstrap']
tbs_month.ix[1::2]['bootstrap'].cumsum()
tbs_month.ix[1::2]['bootstrap'].cumsum().plot()
tbs_month.ix[1::2]['bootstrap'].cumsum().values
v = tbs_month.ix[1::2]['bootstrap'].cumsum().values
x = tbs_month.index[1::2]
x
x.levels[1]
x = x.levels[1]
x
v
plt.plot(x,v)
v
plt.plot(x,v, title = 'bootstrap')
plt.plot(x,v)
top_boot_set
v2 = tbs_month.ix[1::2]['5minbootstrap'].cumsum().values
plt.plot(x,v2)
plt.plot(x,v2)
x.shape
v2.shape
v2 = tbs_month.ix[1::2]['5minbootstrap'].cumsum()
v2.shape
v2
plt.plot(v2.index, v2.values)
plt.plot(v2.index.levels[0], v2.values)
plt.plot(v
)
v2
v2.index.shape
v2.shape
v2[:4]
v2.values
v2.index
v2.index.levels[0]
get_ipython().magic(u'history ')
get_ipython().magic(u'pwd ')
boot.to_csv('data/bootstrap_fork_events.csv')
get_ipython().magic(u'ls ')
mdkir data
mdkir /data
get_ipython().magic(u'mkdir data')
boot.to_csv('data/bootstrap_fork_events.csv')
pd.from_csv('data/bootstrap_fork_events.csv', header=False)
pd.read_csv('data/bootstrap_fork_events.csv', header=False)
tbs_month
get_ipython().magic(u'pinfo tbs_month.drop')
tbs_month.index.levels
tbs_month.ix[::2]
tbs_month.ix[1::2]
tbs_month.ix[::2]
tbs_month_name = tbs_month.ix[::2]
tbs_month_name
tbs_month_name.groupby(level=0).cumsum()
tbs_month_name_cumsum = tbs_month_name.groupby(level=0).cumsum()
tbs_month_name_cumsum['bootstrap']
get_ipython().magic(u'history ')
tbs_month_name_cumsum.index
for key, grp in tbs_month_name_cumsum.groupby(level = 0):
   print key, grp

for key, grp in tbs_month_name_cumsum.groupby(level = 0):
   print key

for key, grp in tbs_month_name_cumsum.groupby(level = 0)[0]:
   print grp

for key, grp in tbs_month_name_cumsum.groupby(level = 0):
   print grp

for key, grp in tbs_month_name_cumsum.groupby(level = 0):
   print grp

for key, grp in tbs_month_name_cumsum.groupby(level = 0):
  >>        plt.plot(grp, label=key)
          #plt.plot(grp['D'], label='rolling ({k})'.format(k=key))
>>        plt.legend(loc='best')⋅⋅⋅⋅
>>        plt.show()
get_ipython().magic(u'paste')
for key, grp in tbs_month_name_cumsum.groupby(level = 0):
        plt.plot(grp, label=key)
        #plt.plot(grp['D'], label='rolling ({k})'.format(k=key))
  >>    plt.legend(loc='best')⋅⋅⋅⋅
      plt.show()
get_ipython().magic(u'paste')
for key, grp in tbs_month_name_cumsum.groupby(level = 0):
        plt.plot(grp, label=key)
        #plt.plot(grp['D'], label='rolling ({k})'.format(k=key))
        plt.legend(loc='best')
        plt.show()

tbs_month_name_cumsum[0]
get_ipython().magic(u'pinfo tbs_month_name_cumsum')
tbs_month_name_cumsum[0:10]
tbs_month_name_cumsum.index.labels
tbs_month_name_cumsum.index.get_level_values
tbs_month_name_cumsum[0:100].groupby(level=0)
for k, g in tbs_month_name_cumsum[0:100].groupby(level=0)
for k, g in tbs_month_name_cumsum[0:100].groupby(level=0):
    print k, g

for k, g in tbs_month_name_cumsum[0:10].groupby(level=0):
    print k, g

for k, g in tbs_month_name_cumsum[0:10].groupby(level=0):

    plt.plot(g, label=k)

for k, g in tbs_month_name_cumsum[0:10].groupby(level=0):

    plt.plot(g, label=k)

for k, g in tbs_month_name_cumsum[0:10].groupby(level=0):
    print k, g

repos = tbs_month_name_cumsum.groupby(level=0)
repos[:10]
repos
repos.sum()
repos.sum()>200
repos[repos.sum()>200]
repos.ix[repos.sum()>200]
repos.apply(repos.sum()>200)
repos
repos.cumsum()
repos.sum()
tbs_month_name_cumsum = tbs_month_name.groupby(level=0, as_index=False).cumsum()
tbs_month = tbs.icol(0).head().groupby('repository_name',  as_index=False).resample('M', how='count')
tbs_month = tbs.icol(0).head().groupby('repository_name').resample('M', how='count')
tbs_month = tbs.groupby('repository_name').resample('M', how='count'
)
tbs_month.head()
)name.groupby(level=0).cumsum()
tbs_mcs= tbs_month_name.groupby(level=0).cumsum()
tbs_mcs
tbs_mcs.groupby(level=0).sum()
tbs_mcs.groupby(level=0).sum() > 10
ind = tbs_mcs.groupby(level=0).sum() > 10
ind
sum(ind)
len(ind)
ind = tbs_mcs.groupby(level=0).sum() > 50
sum(ind)
ind = tbs_mcs.groupby(level=0).sum() > 100
sum(ind)
ind.shape
tbs_mcs.ix[0:10]
tbs_mcs.ix[ind]
tbs_mcs.shape
ind=True
ind = tbs_mcs.groupby(level=0).sum() > 100
ind is True
ind == True
tbs_mcs[ind == True]
tbs_mcs[ind]
tbs_mcs.shape
tbs_mcs.ix[ind]
tbs_mcs.ix[ind==True]
tbs_mcs.ix['bootstrap']
ind = tbs_mcs.groupby(level=0).sum() > 400
ind == True
ind[ind==True]
ind = tbs_mcs.groupby(level=0).sum() > 1000
ind[ind==True]
ind = tbs_mcs.groupby(level=0).sum() > 2000
ind[ind==True]
ind = tbs_mcs.groupby(level=0).sum() > 3000
ind[ind==True]
ind[ind==True].index
tbs_mcs[ind[ind==True].index]
tbs_mcs.ix[ind[ind==True].index]
tbs_mcs_top = tbs_mcs.ix[ind[ind==True].index]
tbs_mcs_top.index
tbs_mcs_top['Android-Bootstrap']
tbs_mcs_top['Android-Bootstrap'].plot(label = 'Android-Bootstrap')
for k in tbs_mcs_top.index(level=0):
    plt.plot(tbs_mcs_top[k], label=k)

for k in tbs_mcs_top.index.levels[0]:
    plt.plot(tbs_mcs_top[k], label=k)

for k in tbs_mcs_top.index.levels[0]:
    plt.plot(tbs_mcs_top[k], label=k)
    print k

for k in tbs_mcs_top.index.levels[0]:
    plt.plot(tbs_mcs_top[k].log(), label=k)

tbs_mcs_top = tbs_mcs.ix[ind[ind==True].index]
tbs_mcs_top
tbs_mcs_top.log()
import numpy as np
np.log10(tbs_mcs_top)
tbs_mcs_toplog = np.log10(tbs_mcs_top)
for k in tbs_mcs_toplog.index.levels[0]:
    plt.plot(tbs_mcs_toplog[k], label=k)

for k in tbs_mcs_toplog.index.levels[0]:
    plt.plot(tbs_mcs_toplog[k], label=k)

ind = tbs_mcs.groupby(level=0).sum() > 2000
tbs_mcs_top = tbs_mcs.ix[ind[ind==True].index]
tbs_mcs_toplog = np.log10(tbs_mcs_top)
for k in tbs_mcs_toplog.index.levels[0]:
    plt.plot(tbs_mcs_toplog[k], label=k)

plt.title('bootstrap repositories with more than 2000 forks since 2012')
get_ipython().magic(u'pinfo plt.xscale')
get_ipython().magic(u'pinfo plt.yscale')
plt.yscale('log')
plt.yscale('log10')
get_ipython().magic(u'pinfo plt.yscale')
plt.yscale('log', 10)
get_ipython().magic(u'pinfo plt.yscale')
plt.yscale(scale='log', basex=10)
plt.yscale(scale='log', *10)
plt.yscale(scale='log', *[10])
plt.yscale('log', *[10])
plt.yscale('log')
get_ipython().magic(u'history ')
get_ipython().magic(u'history -n')
get_ipython().magic(u'pinfo plt.stackplot')
