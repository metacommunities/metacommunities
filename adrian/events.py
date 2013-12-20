# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import seaborn
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import sys
sys.path.append('..')
import github_api_data as gad
import google_bigquery_access as gba

# <markdowncell>

# ## Get a list of repos and their urls to work with

# <codecell>

repos = gad.get_repos()

# <codecell>

# download event data for a sample of them
eve = gad.get_repository_event(url = repos.url.values[0])

# <codecell>

pickle.dump(eve, open('data/one_repos_events.pyd', 'wb'))

# <codecell>

eve = pickle.load(open('data/one_repos_events.pyd', 'rb'))

# <codecell>

eve[0]

# <codecell>

len(eve)

# <codecell>

created_at = [e['created_at'] for e in eve]

# <codecell>

event = [e['type'] for e in eve]

# <codecell>

ids = [e['actor']['id'] for e in eve]

# <codecell>

d = {'time':created_at, 'event':event, 'id':ids}

# <codecell>

df = pd.DataFrame(d)

# <codecell>

df.head()

# <codecell>

df.event.value_counts()

# <codecell>

df.time = pd.to_datetime(df.time)

# <codecell>

df.time.plot(kind='line')

