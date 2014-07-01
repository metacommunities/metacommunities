# coding: utf-8
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

boot_count = boot_count[boot_count>100].order(ascending=False)
most_forked_repos = boot_count.index.values.tolist()
top_boot_set = boot.set_index('repository_name').ix[most_forked_repos]

tbs = top_boot_set.reset_index()
tbs = tbs.set_index('created_at')
tbs_month = tbs.groupby('repository_name',  as_index=False).resample('M', how='count')
#get rid of URLS for the moment
tbs_month_name = tbs_month.ix[::2]

tbs_mcs= tbs_month_name.groupby(level=0).cumsum()

#choose repos with more than 2000 forks
ind = tbs_mcs.groupby(level=0).sum() > 2000
tbs_mcs_top = tbs_mcs.ix[ind[ind==True].index]
df_tbs_mcs_toplog = np.log10(tbs_mcs_top)


for k in tbs_mcs_toplog.index.levels[0]:
    plt.plot(tbs_mcs_toplog[k], label=k)
    plt.title('bootstrap repositories with more than 2000 forks since 2012')


plt.legend(loc='best')
plt.show()

# stackplot using log cumulative summed data
df_tbs_mcs_toplog_filled = df_tbs_mcs_toplog.unstack().replace(np.NaN, 0)
x2 = df_tbs_mcs_toplog_filled.columns.levels[1]
y2 = df_tbs_mcs_toplog_filled.values
plt.stackplot(x2,y2, baseline='sym')
plt.title('bootstrap repositories with more than 2000 forks since 2012')
# stackplot using plain count data

df_tbs_wide = tbs_month.unstack(level=1).replace(np.NaN,0).ix[::2,]
x3 = df_tbs_wide.columns
y3 = df_tbs_wide.values
plt.stackplot(x3, y3, baseline='sym')
plt.title('bootstrap repositories with more than 2000 forks since 2012')
