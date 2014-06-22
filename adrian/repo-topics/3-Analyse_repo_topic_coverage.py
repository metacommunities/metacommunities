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
import time
# import mpld3
# mpld3.enable_notebook()

# <codecell>

REDIS_HOST = '127.0.0.1'

# <codecell>

red = redis.Redis(db='1', host=REDIS_HOST)

# <codecell>

#get all keys
keys_all = set(red.keys('*'))
#get the intersection keys
keys_int = set(red.keys('*:*'))
#isolate the topic keys
keys = keys_all.difference(keys_int)
keys = list(keys)

# <codecell>

sort(keys)

# <codecell>

#only run if there is fresh data in the redis db
un =red.sunionstore('repos:union', *keys)

# <codecell>

red.set('repos:union-count', un)
print 'Account for {}% repositories of the total'.format(100*float(red.get('repos:union-count'))/float(red.get('repos:count_timeline')))

# <codecell>

key_sizes = {k:red.scard(k) for k in keys}
index = key_sizes.keys()
my_colors = 'rgbkymc'
repos_df  = pd.DataFrame(key_sizes.values(), index = index, columns=['repo_count'])
topic_plt = repos_df.repo_count.plot(kind='barh', color = my_colors)
topic_plt.set_xlabel('Number of repositories')
topic_plt.set_ylabel('Domains')
labs = topic_plt.set_yticklabels(index)
topic_plt.set_title('Repository topics on Github')

# <codecell>

ts = time.time()
topic_plt.figure.savefig('figures/{}repotopics.svg'.format(ts))

# <markdowncell>

# ## Intersections between topics
# 
# This was the whole of the topic analysis. Not so much to find the topics on Github, but to explore how they are connected.

# <codecell>

## Possible intersections of interest
intersects = []
src_keys = []
dst_keys = []

for c in itertools.combinations(keys, 2):
    src_keys.append(c[0])
    dst_keys.append(c[1])
    store_key = c[0]+':'+c[1]
    intersects.append(red.sinterstore(store_key, *c))
    fresh_intersects = True

# <codecell>


if fresh_intersects:
    intersect_df = pd.DataFrame({'domain1':src_keys, 'domain2':dst_keys, 'intersection':intersects}, columns=['domain1', 'domain2', 'intersection'])
    intersect_df.shape
    #save as csv to avoid having to run the intersections again
    intersect_df.to_csv('data/intersect_df.csv',index=False)
    fresh_intersects = False
else:     
    #load from csv
    intersect_df = pd.read_csv('data/intersect_df.csv', header=0)

intersect_df = intersect_df.sort(['domain1', 'domain2'])

# <codecell>

intersect_pivot = intersect_df.pivot('domain1', 'domain2', 'intersection')
intersect_pivot_df = intersect_pivot.fillna(value=0, inplace=False)

## another way to do the same thing
# df = intersect_df.set_index(['domain1', 'domain2'])
# df.unstack()

# <codecell>

intersect_norm_df = intersect_pivot_df.apply(np.log1p)
intersect_norm_df.to_csv('intersects.csv')

print intersect_norm_df.shape
print len(intersect_norm_df.index)
print len(intersect_norm_df.columns)

# <codecell>


f = plt.figure(figsize = (10,10))
sp = f.add_subplot(111)
ax = plt.gca()
from mpl_toolkits.axes_grid1 import make_axes_locatable

data = intersect_norm_df.transpose().as_matrix()
mat = sp.matshow(data, cmap=cm.coolwarm)
sp.set_title('Intensity of intersections between domains (normalized)', y= 1.2)
sp.set_xticks(range(0, intersect_norm_df.shape[0]))
sp.set_yticks(range(0, intersect_norm_df.shape[0]))
sp.set_yticklabels(intersect_norm_df.columns)
sp.set_xticklabels(intersect_norm_df.index, rotation=90)
sp.grid(b=False)

divider = make_axes_locatable(ax)

cax = divider.append_axes("right", size="5%", pad=0.1)

cbar = f.colorbar(mat, ticks=[0, 6, 12], cax=cax)
cbar.ax.set_yticklabels(['< 0', '6', '>12'])


f.show()

f.savefig('figures/intersections_normed.svg')

# <markdowncell>

# ## Anomalies in the intersections
# 
# Why are there so few intersections around social media? And especially between social media and web frameworks?

# <codecell>

intersect_df = intersect_df.set_index('domain1')

# <codecell>

intersect_df.ix['social_media']

# <codecell>


for i in range(1,100):
    print socmedia.pop()

# <codecell>

%load_ext rmagic

# <codecell>

int_m  = intersect_pivot_df.as_matrix()
print(type(int_m))
%Rpush int_m

# <codecell>

%%R
xr=chisq.test(int_m)
print(summary(xr$p.value))


# <codecell>


