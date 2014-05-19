# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Analysis of repo topic data coverage
# 
# The first objective here is to see whether it is possible to account for most of the repos on github using topics gleaned from names and descriptions

# <codecell>

import redis
import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import re
import itertools
import numpy as np
# import mpld3
# mpld3.enable_notebook()

# <codecell>

red = redis.Redis(db='1')

# <codecell>

#get all keys
keys_all = set(red.keys('*'))
#get the intersection keys
keys_int = set(red.keys('*:*'))
#isolate the topic keys
keys = keys_all.difference(keys_int)
keys = list(keys)

# <codecell>

keys

# <codecell>

un =red.sunionstore('repos:union', *keys)

# <codecell>


key_sizes = {k:red.scard(k) for k in keys}
index = key_sizes.keys()
repos_df  = pd.DataFrame(key_sizes.values(), index = index, columns=['repo_count'])
plt = repos_df.repo_count.plot(kind='barh')
plt.set_xlabel('count')
labs = plt.set_yticklabels(index)

# <codecell>

## Possible intersections of interest

intersects = []
src_keys = []
dst_keys = []
intersect_df = pd.DataFrame(columns=['domain1', 'domain2', 'intersection'])
for c in itertools.combinations(keys, 2):
    src_keys.append(c[0])
    dst_keys.append(c[1])
    store_key = c[0]+':'+c[1]
    intersects.append(red.sinterstore(store_key, *c))

# <codecell>

intersect_df = pd.DataFrame({'domain1':src_keys, 'domain2':dst_keys, 'intersection':intersects}, columns=['domain1', 'domain2', 'intersection'])
intersect_df.shape

# <codecell>

intersect_df.intersection.hist(bins = 100)

# <codecell>

intersect_pivot = intersect_df.pivot('domain1', 'domain2', 'intersection')
intersect_pivot_df = intersect_pivot.fillna(value=0, inplace=False)
intersect_pivot_df

# <codecell>

intersect_norm_df = intersect_pivot_df.apply(np.log10)
df = intersect_norm_df.fillna(value = 0)

# <codecell>

df

# <codecell>

f = matplotlib.pyplot.figure()

p = plt.pcolor(intersect_pivot_df)
p.set_figure(f)
f.savefig('test.png')
# p.yticks(np.arange(0.5, len(intersect_pivot.index), 1), intersect_pivot.index)
# p.xticks(np.arange(0.5, len(intersect_pivot.columns), 1), intersect_pivot.columns)
# f.show()

# <markdowncell>

# ## Todo -- a heatmap of the intersections

# <codecell>

intersect_df

