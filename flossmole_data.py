# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Many repository datasets archived at [flossmole](http://code.google.com/p/flossmole/downloads/list)
# 
# It could be a way to help fill out data before February 2011, when githubarchive goes back to. And it has many other sites, such as sourceforge, google code, and launchpad.
# Although they say they have been collecting repository data since 2004, the github data seems to only go back to 2010.

# <codecell>

import pandas as pd
import bz2
import requests
import StringIO as io

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

df = get_flossmole(url_sf, 30)
df.head()

# <codecell>

sf_2008_df.tail()

# <codecell>

df = get_flossmole(url_sf_topics, header=30)
df.head()

# <codecell>


