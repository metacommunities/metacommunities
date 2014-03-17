# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Classifying Organizations
# 
# We are attempting to build a classifier for Github organisations. We want to see if organisations organise github. That is, are they a major metacommunity process? Do they significantly affect resource use in the code commons? Is the 'organisation' construct something that deeply shapes what happens on the platform? If so, in what ways?
# 
# Our original motivation for this was a kind of despair in looking at repositories. Although we could characterise them in terms of the categories of sociability (fork-pull requests, pushes, releases, etc), we found it difficult to say anything about why they all existed, what they were doing. Many of them seem to be doing more or less the same thing, but how would we know that? Many of them seemed to be doing nothing. So everything seems too homogeneous. 
# 
# Organisations offer a bit more hope. Some of them exist outside Github and prior to github. Identifying them might give a handle on what is happening  to repos. Conversely, organisations that start on Github and then start to extend beyond it might also be important. Identifying them might tell us about how Github is 
# 
# The first major question here is whether organisations generate any signal on github. That's what the classifier modelling tries to explore.

# <codecell>

%load_ext autoreload
%autoreload 2
import sys
sys.path.append('..')

# <codecell>

import github_api_data as gad
import google_bigquery_access as gba
import bq

import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn
from ggplot import *

from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier

# <markdowncell>

# ## Data sources
# 
# A. The table of ~500 organisations that Richard and Adrian coded by hand as types 0-4. This table is our training and test data. It took a long time to construct because we had to look at the repos and look at websites. We also tagged the organisation with domains like 'design', 'software' etc
# 
# This is the classification:
# 
# - Type 0. junk or nothing -- equivalent to a spam organisation?
# - Type 1. totally internal to github, almost fictional organisation that individual or group make for some benighted reason (e.g ours -- we have a research project) 
# - Type 2. internal but substantial organisations that make something that goes out into the world -- e.g. a software project/product. Github is the main place they exist. Some of the repos should be forked by others 
# - Type 3. external organisation who move into github as a way of revamping/expanding etc what they do. e.g. BBC. Github is not the main place they exist
# - Type 4. Other – impossible to classify
# 
# B. The table of ~ 80k organisations with as many features as we could find -- how many repos, do they fork, do they receive pull requests, do they have an external website, etc

# <markdowncell>

# ### Cleaning up the training data

# <codecell>

## the training/test data
org_training = pd.read_excel('../data/orgs_manual_coding_sample_reconciled.xlsx', sheetname= 'Sheet1', header=6, skiprows=6)

# <codecell>

org_training.shape

# <codecell>

# construct a new column with Adrian and Richard reconciled values
org_training['type'] = org_training['adrian type'].where(
    cond=org_training['adrian type'] == org_training['Richard type'],other=org_training.reconciled )

# <codecell>

print(org_training['type'].value_counts())
org_training['type'].hist(bins=4,figsize=(4,4))

# <markdowncell>

# This data is quite unbalanced. We could probably drop type '0' -- the junk organisations. But type 3 -- the external organisations latching onto github -- do outnumber the type 2 -- our favourite _sui generis_ organisations by a factor of 4 to 1.

# <markdowncell>

# ### Construct the full training/testing data set using the organization ultimate table on bigquery
# 
# Begin to generate the full training data by getting most of what we know about organizations

# <codecell>

# I tried to use pandas to do this directly, but got UnicodeEncodeErrors
# query = 'SELECT * FROM [metacommunities:github_proper.org_ultimate]'
# orgs_full = pd.io.gbq.read_gbq(query)

# <codecell>

# using the bq module directly is easy ... 
client = bq.Client.Get()

query = "select * from metacommunities:github_proper.org_ultimate_1"

# <codecell>

fields, data = client.ReadSchemaAndRows(client.Query(query)['configuration']['query']['destinationTable'], max_rows = 100000)
colnames = [f['name'] for f in fields]

# <codecell>

org_full = pd.DataFrame(data, columns = colnames)
org_full = org_full.drop_duplicates()
org_full_df = org_full.set_index(org_full['repository_organization'])
org_full.shape

# <codecell>

# to construct the full training set

# choose the matching organisation
org_full_training_df = org_full_df.ix[org_training['repository_organization']]

# <codecell>

# add the 'type' column, set the index to organization, and save local copy
org_full_training_df.set_index(keys = 'repository_organization', inplace=True)
org_training.set_index(keys = 'repository_organization', inplace=True)

org_full_training_df['type'] = org_training.type
org_full_training_df.to_csv('../data/organisation_classification_data.csv')
org_full_training_df.shape

# <markdowncell>

# ### Load local cache of dataset (if saved previously)

# <codecell>

# if already saved, load local copy
org_full_training_df = pd.read_csv('../data/organisation_classification_data.csv')


print org_full_training_df.shape

# <codecell>

org_full_training_df['org_type'] = pd.cut(org_full_training_df.type,bins=4, labels=['junk', 'internal_only', 'internal_ext', 'external'])

# <codecell>

# but the categorical variable has a different shape - not sure why that is.
print org_full_training_df.org_type.value_counts()
org_full_training_df.org_type.value_counts().plot(kind='bar',color='green')

# <markdowncell>

# ## Feature selection
# 
# Which variables/features are likely to be directly useful in classifying organisations?

# <codecell>

print '[%s]' % '\n '.join(map(str, org_full_training_df.columns.tolist()))

# <markdowncell>

# ## Other possible features to include in the model
# 
# 1. Has a blog -- binary
# 2. Blog is .com, .gov, .edu, etc -- categorical
# 3. Org_created -- bin this into periods -- early, middle, recent?
# 
# ## Variables I don't fully understand
# 
# 1. Event20Time -- is this when an organisation first reaches 20 events? But there is already MinsTO20Events
# 2. repository_homepages -- are these offsite homepages for repos

# <codecell>

# there are few outliers that wreck this graph if they are plotted, so keeping Repo count < 100. 

p1 = ggplot(org_full_training_df.ix[org_full_training_df.Repos<100], aes(y='repository_homepages', x= 'Repos', color='type')) + geom_jitter()
print(p1)

# <markdowncell>

# ## Data to drop
# 
# If 'type' is what we want to predict I'm thinking Type 0 -- the junk organisations -- are not worth using. 

# <codecell>

# drop the 'junk' organisations?
# org_full_training_df = org_full_training_df.ix[org_full_training_df['type'] > 0 ]
org_full_training_df = org_full_training_df.ix[org_full_training_df['type'] > 0]

# <codecell>


# data exploration
res=org_full_training_df.icol([1,2,3,4,5, 6,7,8,9,10,11,12,13, 14, 15, 16, 18, 19, 20,
                               21, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]).hist(bins=50, figsize=(16,14))

# <codecell>

org_plot = org_full_training_df.ix[org_full_training_df.org_type.dropna()]
print org_plot.org_type
# p = ggplot(data = org_full_training_df.ix[org_full_training_df.org_type.dropna()],
#                                           aesthetics=aes(x='Pushers', y='PushEvents', size='ForkEvents', color='org_type'))
# print(p+geom_point() + labs('Pushers', 'PushEvents', 'Organization Pushing'))

# <codecell>

from ggplot import *
p = ggplot(data = org_full_training_df, aesthetics=aes(x='PushDurationDays', y='Pushers', color='type', size='PushEvents'))
print(p+geom_jitter() + ggtitle('Organisations and their pushes'))

# <markdowncell>

# ## Classifier for organisations types

# <codecell>


clf = RandomForestClassifier(random_state=0)
scores = cross_val_score(clf, org_full_training_df.icol([1,2,3,4,7,8, 9,10, 11, 12, 
                                                16, 18, 19, 20,
                                                21, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]), 
                org_full_training_df.type, cv=50)
scores.mean()

# <markdowncell>

# That is hardly better than dice rolling.
# 
# ## A simpler organisation typology: indigenous and immigrant
# 
# Our typology of organisations is maybe too blurry. What if we say there are some organisations that originate on github and others that come to github from somewhere else?
# 
# - Type 1: originate in Github
# - Type 2: migrate to Github
# 
# (This is somewhat consistent with the metacommunities idea.) That means combining the existing Type 1 and Type 2, and leaving Type 3 as it is.  We are left with a binary response

# <codecell>

# add a new binary response variable that reflects just two types of organisation: indigenous or not
internal = org_full_training_df.type.copy()

internal[internal < 3] = 1
internal[internal > 2] = 0

internal = internal.astype(np.bool)
org_full_training_df['internal_type'] = internal

# <codecell>

org_full_training_df.shape
org_full_training_df['internal_type'].value_counts()

# <codecell>


# set up the algorithm -- n_jobs uses more cores if available
clf = RandomForestClassifier(n_estimators=500, n_jobs = 4)

# <codecell>

scores = cross_val_score(clf, org_full_training_df.icol([1,2,3,4,7,8, 9,10, 11, 12, 
                                                16, 18, 19, 20,
                                                21, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]), 
                org_full_training_df['internal_type'], cv=100)
scores.mean()

# <codecell>

clf.fit(X=org_full_training_df.icol([1,2,3,4,7,8, 9,10, 11, 12, 
                                                16, 18, 19, 20,
                                                21, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]),
        y=org_full_training_df['internal_type'])

# <codecell>

clf.feature_importances_

# <codecell>

feature_names = org_full_training_df.columns.tolist()
feature_names = [feature_names[i] for i in [1, 2,3,4,7,8, 9,10, 11, 12, 16, 18, 19, 20, 21, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]]                                         

d = {'feature': feature_names, 'importance': clf.feature_importances_}
features = pd.DataFrame(d['importance'], index = d['feature'])
features.plot(kind='barh')
# clf.estimators_

# <markdowncell>

# This suggests that PushDurationDays, PushEvents, number of repos, the number of forked repos, number of Pushers, watchevents, etc are the best predictors to work with. The problem is that the score is still quite low (61%) -- that's still not much better than dice rolling. 

# <codecell>

p = ggplot(data = org_full_training_df, aesthetics=aes(x='PushDurationDays',
                                                       y='Pushers', size='PushEvents'))
p = p+geom_jitter() + ggtitle('Organisations and their pushes') + facet_grid('internal_type')
print(p)
ggsave('organisations.png', p)

