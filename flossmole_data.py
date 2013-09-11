# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Repository datasets archived at [flossmole](http://code.google.com/p/flossmole/downloads/list) and also SourceForge
# 
# Flossmole could be a way to help fill out data before February 2011 for github (the github data seems to only go back to 2010). And flossmole has data on many other sites, such as sourceforge, google code, and launchpad. Both the data and the scripts they used could be helpful for us. The url for the download page is http://code.google.com/p/flossmole/downloads/list

# <codecell>

import pandas as pd
import bz2
import requests
import StringIO as io
import json
import time
import datetime

def get_flossmole(url, header=34):

    """ Returns a dataframe for the data at the given flossmole url
    Arguments:
    --------------------------
    url: flossmole url
    header: the line number of the header line
    """

    bz_file = requests.get(url)
    flossmole_data =io.StringIO(bz2.decompress(bz_file.content))
    floss_mole_df = pd.read_table(flossmole_data, sep='\t',  lineterminator='\n',  header = header)
    return floss_mole_df

def get_sourceforge_repo(name):
    
    """ Returns a json dict for the named sourceforge projects

    Arguments:
    --------------------------
    name: the name of the sourceforge project
    """

    sf_api_url_prefix = 'http://sourceforge.net/api/project/name/'
    sf_api_url_suffix = '/json'
    repo_url= sf_api_url_prefix + name + sf_api_url_suffix
    print 'getting %s from %s' % (name, repo_url)
    repo_req = requests.get(repo_url)
    repo_json = json.load(io.StringIO(repo_req.content))
    return repo_json

# <codecell>


url = 'http://flossmole.googlecode.com/files/ghProjectInfo2010-May.txt.bz2'


gh_2010_df = get_flossmole(url, header=34)

# <codecell>

gh_2010_df.head()

# <markdowncell>

# The fields here are not exactly the same as at githubarchive, but having the project names, and url is probably enough to help us see what was there in May 2012.

# <markdowncell>

# ## some data on other repositories: e.g SourceForge

# <codecell>

url_sf = 'http://flossmole.googlecode.com/files/sfRawUserIntData2008-Feb.txt.bz2'
url_sf_topics = 'http://flossmole.googlecode.com/files/sfRawTopicData2008-Feb.txt.bz2'

# <codecell>

sf_df = get_flossmole(url_sf, 30)
sf_df.head()

# <codecell>

sf_topics_df = get_flossmole(url_sf_topics, header=30)
sf_topics_df.head()
sf_df.ix[sf_df['proj_unixname'] == 'filezilla']

# <markdowncell>

# # Could we combine these project names with the SourceForge api to get more data? 
# 
# The sourceforge api is fairly basic but easy to use: http://sourceforge.net/apps/trac/sourceforge/wiki/API. Many queries return json. 
# It can be date delimited, but then you get RSS, which needs further processing
# e.g. http://sourceforge.net/api/project/index/new_since/1272409091

# <codecell>

sf_api_url='http://sourceforge.net/api/project/name/tangoiconsprite/json'
req = requests.get(sf_api_url)
sf_example =json.load(io.StringIO(req.content))

# <codecell>

sf_example_df = pd.DataFrame.from_dict(sf_example, orient='index')
sf_example_df

# <codecell>

## using flossmole list of projects ...

sf_repos_df = pd.DataFrame()
for name in sf_df['proj_unixname'][100:105]:
    repo_json = get_sourceforge_repo(name)
    sf_repos_df = sf_repos_df.append(pd.DataFrame.from_dict(repo_json,orient='index'))

# <codecell>

sf_repos_df.columns

# <codecell>

sf_repos_df.created

# <markdowncell>

# ## To get time delimited SourceForge data
# 
# URL has the form: http://sourceforge.net/api/project/index/new_since/timestamp
# 
# I think the results are paged, so more work to get them. But to show possibilities ... 

# <codecell>



start_date = datetime.datetime(2010, 12, 31)
timestamp = int(time.mktime(start_date.timetuple()))
date_url = "http://sourceforge.net/api/project/index/new_since/" + str(timestamp)
date_req = requests.get(date_url)

# <codecell>

# make this into a list of elements, dropping all the name.u entries (I think)
projects = date_req.content
projects_clean = projects.replace('<br/>', '').replace('Group: ', '')
projects_clean = projects_clean.splitlines()

projects_alone = []
for project in projects_clean:
    if project.find('.u') <0:
        projects_alone.append(project)

# <codecell>

projects_alone

# <markdowncell>

# We can use then use those project lists to get repository data for each project in the list, and then also to access the repository directly

# <codecell>

get_sourceforge_repo(projects_alone[1])

# <codecell>

source_forge_project_df = pd.DataFrame()
for project in projects_alone[-20:-1]:
    project_json = get_sourceforge_repo(project)
    project_data = pd.DataFrame.from_dict(project_json, orient='index')
    source_forge_project_df = source_forge_project_df.append(project_data)
    

# <codecell>

source_forge_project_df.head()

# <codecell>


