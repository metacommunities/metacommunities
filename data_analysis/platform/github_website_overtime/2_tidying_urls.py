# coding: utf-8
import pandas as pd
import subprocess as sp
get_ipython().magic(u'pinfo sp.Popen')
urls = pd.read_csv('github.com_about.txt', header=None)
get_ipython().magic(u'load 1_clean_archived_gh_websites.py')
site = 'github.com/about'
base = 'https://web.archive.org/web/'
df['date_formatted'] = pd.to_datetime(df.date, format='%Y%m%d%H%M%S')
full_url = base+df.date.astype(str) + '/'+df.url
full_url.to_csv(site.replace('/', '_') + '.txt',index=False)
df = pd.read_csv('full_github.com_about.csv')
df.head()
df = pd.read_csv('full_github.com_about.csv', header=None)
df.head()
df_c = df.iloc[:, [2,3,5,7]]
df_c.columns = ['date', 'url', 'code', 'size']
get_ipython().magic(u'matplotlib')
df_c['size'].plot()
df_c = df_c.ix[df_c['size']>500,['date', 'url']]
