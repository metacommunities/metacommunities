# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Classifying Organizations

# <codecell>

%load_ext autoreload
%autoreload 2

# <codecell>

import sys
sys.path.append('..')
import github_api_data as gad
import google_bigquery_access as gba
import bq

import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn

# <markdowncell>

# We are attempting to build a classifier for Github organisations. We want to see if organisations organise github (or not). Is the 'organisation' construct something that deeply shapes what happens on the platform? If so, in what ways?

# <markdowncell>

# ## Data sources
# 
# A. The table of ~500 organisations that Richard and Adrian coded by hand as types 0-4. This table is our training and test data. It took a long time to construct because we had to look at the repos and look at websites. We also tagged the organisation with domains like 'design', 'software' etc
# 
# This is the classification:
# 
# 0. junk or nothing -- equivalent to a spam organisation?
# 1. totally internal to github, almost fictional organisation that individual or group make for some benighted reason (e.g ours -- we have a research project) 
# 2. internal but substantial organisations that make something that goes out into the world -- e.g. a software project/product. Github is the main place they exist. Some of the repos should be forked by others 
# 3. external organisation who move into github as a way of revamping/expanding etc what they do. e.g. BBC. Github is not the main place they exist
# 4. Other – impossible to classify
# 
# B. The table of ~ 80k organisations with as many features as we could find -- how many repos, do they fork, do they receive pull requests, do they have an external website, etc

# <codecell>

## the training/test data
org_training = pd.io.excel.read_excel('../data/orgs_manual_coding_sample_reconciled.xlsx', sheetname= 'Sheet1', header=6, skiprows=6)

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

# ## Construct the full training/testing data set using the organization ultimate table on bigquery

# <codecell>

# I tried to use pandas to do this directly, but got UnicodeEncodeErrors
# query = 'SELECT * FROM [metacommunities:github_proper.org_ultimate]'
# orgs_full = pd.io.gbq.read_gbq(query)

# <codecell>

# using the bq module directly is easy ... 
client = bq.Client.Get()

query = "select * from metacommunities:github_proper.org_ultimate"

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

# if already saved, load local copy
org_full_training_df = pd.read_csv('../data/organisation_classification_data.csv')
print org_full_training_df.shape

# <codecell>

# otherwise, add the 'type' column, set the index to organization, and save local copy
org_full_training_df.set_index(keys = 'repository_organization', inplace=True)
org_training.set_index(keys = 'repository_organization', inplace=True)

org_full_training_df['type'] = org_training.type
org_full_training_df.to_csv('../data/organisation_classification_data.csv')
org_full_training_df.shape

# <codecell>

# making a local copy for ease of playing around
org_full_training_df.to_csv('../data/organisation_classification_data.csv')

# <codecell>

org_full_training_df.columns

# <codecell>

org_full_training_df.type
org_full_training_df.type.hist(figsize=(4,4), bins=4)

# <markdowncell>

# ## Feature selection

