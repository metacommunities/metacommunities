# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import sys
sys.path.append('..')
import github_api_data as gad
import google_bigquery_access as gba
import google_bigquery_access as gbq
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# <markdowncell>

# # Demo: retrieving 50,000 rows from githubarchive on programming languages in 2012
# 
# The code assumes that you have already authenticated an application with Googel oauth2, and that you have client_secrets.json file in the same directory as the this notebook. 

# <codecell>

programming_languages_2012 = """select actor, repository_language, 
                            count(repository_language) 
                            as pushes
                            from [githubarchive:github.timeline]
                            where type='PushEvent'
                            and repository_language != ''
                            and PARSE_UTC_USEC(created_at) >= PARSE_UTC_USEC('2012-01-01 00:00:00')
                            and PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2013-01-01 00:00:00')
                            group by actor, repository_language;"""

# <codecell>

results_df = gbq.query_table(programming_languages_2012, max_rows=100000)

# <codecell>

results_df = results_df.fillna('')
results_df.head()

# <codecell>

languages=results_df['repository_language'].value_counts()
plt.figure(figsize=(10,12))
plt.barh(range(0,languages.index.shape[0]), languages, alpha=0.7)
plt.yticks(range(0,languages.index.shape[0]),languages.index)

plt.title('programming languages on github 2012')

plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='on',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='on')
plt.tick_params(
    axis='y',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    left='on',      # ticks along the bottom edge are off
    right='off')
plt.box(on=False)

#.plot(kind='bar', title='programming languages on github 2012', box='off')

# <markdowncell>

# ## What about in 2011? Did things look the same then?

# <codecell>

programming_languages_2011 = """select actor, repository_language, 
                            count(repository_language) 
                            as pushes
                            from [githubarchive:github.timeline]
                            where type='PushEvent'
                            and repository_language != ''
                            and PARSE_UTC_USEC(created_at) >= PARSE_UTC_USEC('2011-01-01 00:00:00')
                            and PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2012-01-01 00:00:00')
                            group by actor, repository_language;"""


# <codecell>

results_2011_df = gbq.query_table(programming_languages_2011, max_rows=100000)

# <codecell>

results_2011_df.head()

# <markdowncell>

# # The growth of repositories

# <codecell>

query = """
select repository_name, DATE(TIMESTAMP(repository_created_at)) as date, count(repository_name) 
FROM
  (SELECT repository_name, repository_created_at, type FROM [githubarchive:github.timeline]
   WHERE (HASH(repository_created_at)%10 == 0))
 GROUP BY  repository_name, date
 order by date;"""

# <codecell>

resdf = gbq.query_table(query, max_rows=100000, timeout=3.0)

# <codecell>

resdf.head()

# <codecell>

resdf.to_csv('data/repos_created_100k.csv')

# <codecell>

#only if loading locally
resdf = pd.DataFrame.from_csv('data/repos_created_100k.csv')

# <codecell>

series = pd.TimeSeries(data = resdf['repository_name'])
dti = pd.DatetimeIndex(resdf['date'])

# <codecell>

series.index = dti
series.head()

# <codecell>

ms=series.to_period(freq='M')

# <codecell>

ds = series.to_period(freq='D')
ds.shape

# <codecell>

ds.head()
ds[ds == 'jquery']

# <codecell>

by_months = ds.resample('m', how='count')
by_months.plot(kind='bar', label='repositories created by months', figsize=(10,5))

# <markdowncell>

# # Events per repo over time

# <codecell>

query = """SELECT
  DAYOFYEAR(TIMESTAMP(repository_created_at)) as day,
  YEAR(TIMESTAMP(repository_created_at)) as year,
  repository_name,
  type,
  COUNT(*) AS daily_event_count
FROM
  /* Consider only approximately 1/10th of the creation dates in the entire table */
  (SELECT repository_name, repository_created_at, type FROM [githubarchive:github.timeline]
   WHERE (HASH(repository_created_at)%10 == 0))
GROUP BY
  year, day,type, repository_name
HAVING
  daily_event_count > 2
ORDER BY
  year ASC, day ASC, daily_event_count DESC; """

# <codecell>

events_df = gbq.query_table(query, max_rows = 100000)
events_df.head()

# <codecell>

events_df.to_csv('data/events_per_repo.csv')

# <codecell>

events_df = pd.DataFrame.from_csv('data/events_per_repo.csv')

# <codecell>


plt.figure()

# <codecell>

events_df['daily_event_count'] = events_df['daily_event_count'].astype('int32')
events_df['day'] = events_df['day'].astype('int32')
events_df['year'] = events_df['year'].astype('int32')

# <codecell>


events_df['day'].hist(bins=50, color='k', alpha=0.3, normed=True, by=events_df['year'])


# <codecell>


