# coding: utf-8
import pandas as pd
import subprocess as sp
site = 'github.com/about'
base = 'https://web.archive.org/web/'
df = pd.read_csv('full_github.com_about.csv', header=None)
df_c = df.iloc[:, [2,3,5,7]]
df_c.columns = ['date', 'url', 'code', 'size']
full_url = base+df_c.date.astype(str) + '/'+df_c.url
df_c['full_url'] = full_url
df_c.head()
get_ipython().magic(u'matplotlib')
df_c['size'].plot()
# get pages with size greater than blank
df_c = df_c.ix[df_c['size']>500,:]

for i in df_c['full_url'].values:
    r = sp.Popen(['wkhtmltoimage', i, i.replace('/', '_')+'.png'])



