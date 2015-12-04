# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Github re-naming, takeover or merger?
# 
# We have a table of 200k repos that are forks and have at least 4 Push events. 
# 
# This is basically going through the takeover/renaming/merger analysis that Richard did in early Sept 2013.

# <codecell>

import pandas as pd
import matplotlib.pylab as mpl
import MySQLdb

# <codecell>

#text file with MySQL user on 1st line and password on the 2nd needed!
mysql_details = open('mysql_user_login.txt', 'r')
credentials = mysql_details.readlines()
user = credentials[0].strip()
password = credentials[1].strip()

# mysql database name where the table lives -- could put this into mysql_details.txt?
gh_db = 'github_analysis'

db_conn=MySQLdb.connect(db=gh_db, user=user, passwd = password)

#the table that Richard made from BQ
query = 'select * from bq_forks_aug'

# <codecell>

repos_df = pd.io.sql.read_sql(query, db_conn)

# <codecell>

print(repos_df.columns)
print('table shape: '+str(repos_df.shape))

# <codecell>

repos_df.repository_url.value_counts().head(20)

# <markdowncell>

# Not sure why this table has duplicate repo names. Richard? I can understand the parent_repos being duplicated, but not the fork repos names ... 
# Richard: Didn't expect this. There are ForkEvents tying them to more than one parent, possibly where a user created a fork of a repo, deleted it, and then forked another version of that same repo.
# I wouldn't have expected that table of repository_url to have duplicates and I never checked to see if it did. I've had a look and its because some of the fork repos have ForkEvents tying them to more than one parent (ForkEvents are how I tied the forks to their parents, I assumed one event per fork). There are two possibilities: 1) a user creates a fork of a repo, deletes it and subsequently forks another version of the repo (which is actually a distinct repo but gets the same name as the earlier deleted fork because its being created by the same user). 2) I don't know but it may be possible to fork a branch of a repository and fold it into one's own repository as a distinct branch, and the method I used of tying forks to their parent may have picked up on these events as well. In any case, there are 5,230 forks in the bq_forks_aug table which have 'more than one parent'. I will have a look and see if I can find out if the above explanations fit (it should be possible to rule out the 2nd).

# <codecell>

print(repos_df.parent_repo.value_counts().head(30))

# <markdowncell>

# ## Overview of the count fields in the table
# 
# All plots below just to have a quick look at the kinds of numbers in the table

# <codecell>

plt = repos_df.iloc[:,[2,3,4,5,6,7,8,9, 15,16,17,18,19,20, 21, 22, 23, 26, 27, 28, 29, 30, 31]].hist(bins=100, figsize=(18,14))

# <markdowncell>

# ## Where the fork is more than the parent
# 
# Various criteria to look at here:
# 
# 1. Fork has the same or more pushes than parent
# 2. Fork has the same or more pushers than parent
# 2. Fork has the same or more watchers than parent
# 3. Fork forks the same or more than parent
# 4. Fork receives the same or more pull requests than parent
# 
# Here I'm not taking into account the commonpushers. So this filtering will allow 'renaming' takeovers through. That's ok. 

# <codecell>

#more pushes than parent
more_pushes = repos_df[repos_df.PushEvents >= repos_df.Parent_PushEvents]
print('%d where fork has more pushes than the parent'% more_pushes.shape[0])
#more pushers than parent
more_pushers = repos_df[repos_df.Pushers >= repos_df.Parent_Pushers]
print('%d where fork has more pushers than the parent'% more_pushers.shape[0])
#more watchers than parent
more_watchers = repos_df[repos_df.maxWatchers >= repos_df.Parent_maxWatchers]
print('%d where fork has more watchers than the parent'% (more_watchers.shape[0]))

#more forks than parent
more_forks = repos_df[repos_df.maxForks >= repos_df.Parent_maxForks]
print('%d where fork has more forks than the parent'% (more_forks.shape[0]))
more_pullrequest_heads = repos_df[repos_df['PR_fork_base_distinctrepos']> repos_df['PR_parent_base_distinctrepos']]
print('%d where fork has received pull requests from a greater number of distinct head repos than the parent'% (more_pullrequest_heads.shape[0]))

more_pullrequest = repos_df[repos_df['PR_fork_base']> repos_df['PR_parent_base']]
print('%d where fork has received more pull request events than the parent'% (more_pullrequest_heads.shape[0]))


# <codecell>

## to look at intersection of these
push_set = set(more_pushes.index)
forks_greater_than_parents =push_set.intersection(more_pushers.index, more_watchers.index, more_forks.index, more_pullrequest.index)
forks_greater_than_parents_union =push_set.union(more_pushers.index, more_watchers.index, more_forks.index, more_pullrequest.index)
print('%d forks are greater than their parents on every front'%len(forks_greater_than_parents))
print('%d forks are greater than their parents on at least one front'%len(forks_greater_than_parents_union))

# <codecell>

repos_df.ix[forks_greater_than_parents, ['repository_url','parent_repo', 'PushEvents', 'Pushers', 'CommonPushers']].sort('PushEvents', ascending=False).head(20)

# <markdowncell>

# This table of 140 repositories should be the most comprehensive takeovers/renamings/mergers on the Github timeline. I guess it doesn't give us too many to analyse.
# 
# Richard: how did you get 5662 here?  I either get 34k or 140 (for the full intersection on all fronts). 
# 
# Richard's response: I get the same figures for the first 2 rows. Where fork has more watchers than parent you are looking at the largest observed figure for parent and fork - I was looking at the growth of this figure over the observation period (difference between min and maxWatchers for fork/parent). Same thing applies for number of forks. Your row about pull requests is actually comparing the number of distinct head repos which made pull requests on the fork/parent, whereas I was looking at number of distinct pull requests.

