# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Topics on stackoverflow
# 
# Trying out some of the ideas from Allamanis (Allamanis, 2013) to see whether they help us. 

# <codecell>

import sys
sys.path.append('..')

import google_bigquery_access as gbq
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import gensim as gs

# <markdowncell>

# ## Questions about git and github
# 
# We could use stackoverflow to see how people talk about git or github. What kind of issues or problems do they ask about?

# <codecell>

query1 = """select title, body, tags, viewcount from [stack_overflow.Posts]
where tags contains 'git'
limit 1000;"""
git_df = gbq.query_table(query1, 1000)

# <markdowncell>

# To get some idea of the most popular questions about git, just look at those that are viewed more than 2000 times

# <codecell>

git_df['viewcount'] = git_df['viewcount'].astype('int')
git_df[git_df['viewcount']>2000].title

# <markdowncell>

# The most heavily viewed question on Stackoverflow about git is:

# <codecell>

git_df[git_df.viewcount == git_df.viewcount.max()][['title', 'tags']]

# <markdowncell>

# This suggests that differences and merging is a key issue. 

# <markdowncell>

# ## Particular platforms and their importance: the example of Node.js
# 
# If we think that particular platforms or libraries are especially worth investigating, how would we go about that?
# Take for instance the Node.js platform: how is that present on Stackoverflow?

# <codecell>

query2 = """ select title, body, tags, answercount, creationdate from [stack_overflow.Posts]
where tags contains 'node.js'
limit 100"""
node_df = gbq.query_table(query2, 1000)

# <codecell>

node_df.ix[0:10][['creationdate', 'title']]

# <markdowncell>

# A very small sample here, but the rate at which these questions were being created suggests high levels of interest in node.js

