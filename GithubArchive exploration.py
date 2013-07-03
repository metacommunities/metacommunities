# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import google_bigquery_access as gbq
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# <markdowncell>

# # Repositories by event histories: top 100
# 
# A simple way to look at them is just be looking at sheer number of events. 

# <codecell>

query  = """SELECT repository_name, RepoEvents
FROM
(
    SELECT repository_name, COUNT(repository_name) AS RepoEvents
    FROM [githubarchive:github.timeline]
    GROUP BY repository_name
) MyTable
GROUP BY RepoEvents, repository_name
ORDER BY RepoEvents DESC
limit 100;"""

 
results_df = gbq.query_table(query, max_rows=5000)

# <codecell>

results_df

# <markdowncell>

# Some interesting entries in this list. Quite a few of the top repos are just test repos (try-git, test, Test). Some are major projects like the Eclipse software development environment, Mozilla, Moodle, linux, or rails, a Ruby web framework. Others are a bit more surprising, like the [Khan Academy](https://www.khanacademy.org/) Exercises or TrinityCore, a game server, or Euro2012. Or number 33: 'pulWifi shows the default password of some wireless networks'.  Can this repo really be more active than mozilla-central or do we need to distinguish what kinds of events are occurring in it? 
# 
# Running a similar query but now just looking at PushEvents. Maybe these give a different idea of repo activity?

# <codecell>

query = """
SELECT repository_name, RepoEvents
FROM
(
    SELECT repository_name, COUNT(repository_name) AS RepoEvents
    FROM [githubarchive:github.timeline]
    WHERE type = 'PushEvent'
    GROUP BY repository_name
) MyTable
GROUP BY RepoEvents, repository_name
ORDER BY RepoEvents DESC
limit 100;

"""
push_results_df = gbq.query_table(query, max_rows=5000)

# <codecell>

push_results_df

# <markdowncell>

# The ordering changes here, although many of the same repo names appear. But that's an important point. There is no single test repository, but quite a few repositories called 'test' or 'thesis' or 'scripts' or 'android'. Different repos can have the same name. 

