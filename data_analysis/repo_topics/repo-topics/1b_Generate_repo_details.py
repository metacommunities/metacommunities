# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import redis
import pandas as pd
import re

# <markdowncell>

# ## Generate details on repo topics and domains
# 
# Code to generate more detailed information on particular domains

# <codecell>

red = redis.Redis(db='1')

def device_specific_repos(query, use_description = False):
    """ For a given query, return all the repo names, full names and fork
    from the master list of reponames held on the githubarchive timeline.
    It uses regular expression to do this.
    
    @param: description - if True, will use the 'description' field too"""
    
    print('starting bigquery ... ')
    #to deal with the way people name repositories, try various separator characters
    query = re.subn('[-_\s+]', '.?', query)[0]
    query = re.subn('[,\(\):]', '', query)[0]
    print query
    if use_description:
        full_query = 'SELECT name, full_name, fork FROM [github_proper.repo_list] where regexp_match(lower(name),"' + query +'") or regexp_match(lower(description),"'+ query +'")'
                          
    else:
        full_query = 'SELECT name, full_name, fork FROM [github_proper.repo_list] where regexp_match(lower(name),"' + query +'")'
            
    full_df = pd.io.gbq.read_gbq(full_query)
    full_df['device'] = query
    print(full_df.shape)
    return full_df

# <codecell>

def aggregate_many_queries(df):
    queries = df['name'].str.strip().str.lower().tolist()
    result_df = pd.DataFrame()
    for q in queries:
        res = device_specific_repos(q, use_description=False)
        res['device'] = q
        result_df = result_df.append(res)
    return result_df
    

# <codecell>

df = pd.DataFrame({'name':['cloud', 'virtual']} )
a_df = aggregate_many_queries(df)
a_df.head()

# <codecell>

a_df['device'].value_counts()

# <codecell>

## Cloud query example

query = 'cloud'
cloud_df = device_specific_repos(query, use_description=True)

# <codecell>

cloud_df.head()

# <codecell>

query = 'corrugated-box-machine'
cartonmachine_df = device_specific_repos(query, use_description=False)

# <codecell>

cartonmachine_df.head()

# <codecell>

query = 'mirror'
mirror_df = device_specific_repos(query, use_description=True)

# <codecell>

mirror_df.head()

# <codecell>

socialmedia = pd.read_csv('topic_lists/social_media.csv', header=0)

# <codecell>

socialmedia_df = aggregate_many_queries(socialmedia[:4])

# <codecell>

socialmedia_df.shape
smdf = socialmedia_df.copy()

# <codecell>

wikipedia_df = device_specific_repos('wikipedia')

# <codecell>

socialmedia_df = pd.concat([socialmedia_df, wikipedia_df])
socialmedia_df.shape

# <codecell>

red.sadd('socialmedia', *socialmedia_df.full_name)

# <codecell>

df = device_specific_repos('api')

# <codecell>

df = device_specific_repos('api|sdk', description=False)

# <codecell>

df.head(20)

