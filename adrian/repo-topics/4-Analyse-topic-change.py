# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ## Changing relations between domains over time
# 
# Do domain combine differently over time?

# <codecell>

import redis
import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import re
import itertools
import numpy as np
from github import Github

# <codecell>

g = Github('rian39', 'inc14ives')

# <codecell>

red  = redis.Redis(db='1')

# <codecell>

soc_sampe = red.srandmember('social_media', 100)
for r in soc_sampe:
    try:
        r = g.get_repo(r)
        print r.created_at
    except Exception, e:
        print e
    

