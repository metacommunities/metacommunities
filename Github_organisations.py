# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # How organisations fork repositories and how their forking relates them to the github commons

# <codecell>

%load_ext autoreload
%autoreload 2

# <codecell>

import matplotlib.pyplot as plt
import google_bigquery_access as gba
import pandas as pd
import graph_tool.all as gt
import numpy as np
import re
import IPython.display
import pickle
import github_api_data as gad

# <markdowncell>

# ## Setup code to get data from our bigquery tables
# 
# Only run this section code if there is no local copy of the organisation data. See next section to load the local copy of the data.

# <codecell>

# get list of tables in our dataset
bq = gba.setup_bigquery()
tables = bq.tables()
gh_tables = tables.list(projectId=gba.PROJECT_ID,  datasetId='github_explore').execute()

# <codecell>

# these are all the tables we have made using queries, as well as the github timeline itself
[t['id'] for t in gh_tables['tables']]

# <codecell>

#for organisations and their forks, this is the main table to work
table_name = 'forks_made_by_orgs'
tdata = bq.tabledata()

# <codecell>

# get data from the table on bigquery
td = tdata.list(projectId = gba.PROJECT_ID, datasetId = gba.DATASET_ID, tableId=table_name, maxResults=200000)
org_f = td.execute()

# <codecell>

print(org_f.keys())
print('Total rows in table %s: %s' % (table_name, org_f['totalRows']))
orgs = org_f['rows']

vals =[i.values() for f in orgs for i in f['f']]
# better way to do this in pandas?
vala =np.array(vals).reshape([len(orgs), 4])
org_fork_df = pd.DataFrame(vala, columns = ['fork_url', 'parent_url', 'creation_data', 'organisation']).drop_duplicates()
print('Retrieved %d unique rows from table' % org_fork_df.shape[0])

# <markdowncell>

# The table in BigQuery doesn't seem to have enough rows -- that is, only ~14k organisations appear there. Can that be right? In that case, most organisations are forking other repos.
# Also, the api only returns 58k unique rows, but the total rows in the table is 133k. But looking at the table, it seems there are quite a few duplicates. e.g. Rows 1-4 ... 

# <codecell>

# construct a new column for parent/target repo names (the ones that are forked)
org_fork_df['parent_repo'] = org_fork_df.parent_url.map(lambda x: '_'.join(re.split('\/', x)[-2:]))

# <codecell>

print('There are %s unique organisations and they fork %s unique repositories' 
      % (len(org_fork_df.organisation.unique()), len(org_fork_df.parent_url.unique())))
org_fork_df.head()

# <codecell>

#save/load local copy
org_fork_df.to_csv('data/org_forks.csv')

# <markdowncell>

# ## Load local copy of the data if available

# <codecell>

#load local copy
org_fork_df = pd.DataFrame.from_csv('data/org_forks.csv')

# <markdowncell>

# ## The graph of organisations who fork repos

# <codecell>

## graph
g = gt.Graph()
verts = g.add_vertex(n= len(org_fork_df.organisation.unique()) + len(org_fork_df.parent_repo.unique()))
v_org = g.new_vertex_property('string')
v_parent = g.new_vertex_property('boolean')
#the complete list of nodes includes organisations and parent repos for the moment
nodes = pd.concat([org_fork_df.organisation,  org_fork_df.parent_repo]).unique().tolist()
#add nodes as vertices
for v,o in zip(verts, nodes):
    v_org[v] = o
    if o in org_fork_df.parent_repo:
        v_parent[v] = True
g.vertex_properties['org_repo_name'] = v_org
g.vertex_properties['is_parent'] = v_parent

# <codecell>

#add edges
for s,t in zip(org_fork_df.organisation, org_fork_df.parent_repo):
    g.add_edge(nodes.index(s),nodes.index(t)) 

# <codecell>

#this takes ages!
pos = gt.sfdp_layout(g)
gt.graph_draw(g, pos = pos)
#to save
gt.graph_draw(g, pos=pos, output='figures/organisation_parent.png')

# <codecell>

IPython.display.Image('figures/organisation_parent.png')

# <markdowncell>

# This kind of supernova suggests there are some highly reactive/attractive repositories that attract organisations in github. What are they?

# <markdowncell>

# ## The repos that are forked and who forks them
# 
# ### Repos that are forked
# 
# CyanogenMod is very big here (Android open source). Has it appeared before on our lists? Interesting also see  AOKP - Android Open Kang Project. Is Android software actually really important in github?
# 
# And then the social media platforms -- twitter, github, rails, django, facebook-ios, restkit.
# 
# So maybe we want to do some platform-type classification here -- android repos, vs social media repos vs others .... 

# <codecell>

print('\tThe repos that organisations are forking')
print('______________________________________________________')
org_fork_df.parent_repo.value_counts().head(50)

# <codecell>

# to try and get a better look at the parent repos
pos, sel = gt.graph_draw(g, vertex_shape=v_parent)

# <codecell>

# community structure is Mark Newman's
community = gt.community_structure(g, 1000, 5)
gt.graph_draw(g, pos=pos, vertex_fill_color=community,  output='figures/organisation_parent_community.png')

# <codecell>

IPython.display.Image('figures/organisation_parent_community.png')

# <markdowncell>

# ## The organisations are forking
# 
# The problem of formal vs informal organisations -- what is a proper organization? Presumably it needs more than one member ...
# Which organisations are doing the most forking?

# <codecell>

org_fork_df.organisation.value_counts()

# <codecell>

org_fork_df.organisation.value_counts().hist(bins=200)

# <markdowncell>

# The histogram shows that most organisations only fork one or two repositories, but some fork many more. It's possible that the many-fork organisations are not very substantial organisations, but just github-organisations. Compare the organization 'mozilla' with 'ChameleonOS'

# <codecell>

mozilla_members = gad.get_organisation_members('mozilla')

# <codecell>

print('Mozilla organisation has %d members' % mozilla_members.shape[0])
mozilla_members[['id', 'login']].head(30)

# <codecell>

chameleon_members = gad.get_organisation_members('ChameleonOS')

# <codecell>

print('ChameleonOS organisation has %d members' % chameleon_members.shape[0])
chameleon_members[['id', 'login']].head()

# <markdowncell>

# To check whether these heavy-forking organisations are substantial organisations, we need the membership numbers for them

# <codecell>

top_forking_orgs = org_fork_df.organisation.value_counts()
top_fork_names  = top_forking_orgs.index[0:50]
org_member_df = pd.DataFrame()
for o in top_fork_names:
    
    o_memb = gad.get_organisation_members(o)
    o_memb['organisation'] = o
    print ('%s:\t\t%d'%(o, o_memb.shape[0]))
    if o_memb.shape[0] >0:
        org_member_df = org_member_df.append(o_memb)


# <markdowncell>

# The higher numbers are good indicators. The organisation called 'collective' is a good example, as is 'CyanogenMod.'  I'd call them 'organisations.' Then the question is why they are forking so much. 
# 
# Others are doing something very different. There are loads of Android related organisation who fork a lot. Is this something specific to Android software or modding? A mushrooming of high-forking organisations?
# 
# Some of these results are strange. The last one -- WindowsAzure-Preview is a Microsoft organisation and repos. Microsoft is an organisation it seems, but it has no members. 

# <codecell>

org_member_df.head()

