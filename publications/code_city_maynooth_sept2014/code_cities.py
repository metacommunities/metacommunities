# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ## Code in cities
# 
# I wanted to get some sense of the geography of github. It only needs to be approximate, so I'm using actor_location to do this

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


# <codecell>

client = bq.Client.Get()

query = "select * from metacommunities:github.actor_location"

# <codecell>

fields, data = client.ReadSchemaAndRows(client.Query(query)['configuration']['query']['destinationTable'], max_rows = 100000)
colnames = [f['name'] for f in fields]

# <codecell>

locations_df = pd.DataFrame(data, columns = colnames)
locations_df.shape

# <codecell>

locations_df['location_count'] = locations_df.location_count.astype('int')
locations_df.sort('location_count', ascending=False)

# <codecell>

# clean up location names
locations_df['locations_full'] = locations_df.location.str.lower().str.strip().str.replace('$ ', 'na').str.encode('utf8').str.replace('[<>=().;/"]', '').str.split(', ')

# drop empty values
locs = locations_df.dropna()
locs.shape

# <codecell>

# create master list of places that mixes countries, cities, states, etc
place_list = [i for l in locs.locations_full.tolist() for i in l]

# <codecell>

place_set = list(set(sort(place_list)))

# <codecell>

locs.ix[locs['locations_full'].map(lambda x: 'hong kong' in x)]

