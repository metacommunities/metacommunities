# Takes the list of urls returned by wayback machine
# and fetches the webpages from wayback machine
# then saves them as images in the images directory

import pandas as pd
import subprocess as sp
import sys

if sys.argv[1] != None:
    site = sys.argv[1]
else:
    site = 'github.com/about'

base = 'https://web.archive.org/web/'
csv_name = 'full_' + site.replace('/', '_') +'.csv'
df = pd.read_csv(csv_name, header=None)
df_c = df.iloc[:, [2,3,5,7]]
df_c.columns = ['date', 'url', 'code', 'size']
full_url = base+df_c.date.astype(str) + '/'+df_c.url
df_c['full_url'] = full_url
df_c.head()
# get_ipython().magic(u'matplotlib')
# df_c['size'].plot()

# get pages with size greater than blank
df_c = df_c.ix[df_c['size']>500,:]

for i in df_c.full_url.values:
    r = sp.Popen(['wkhtmltoimage', i, 'images/'+ i.replace('/', '')+'.png'], stdout=sp.PIPE, stderr=sp.PIPE)
    stout, sterr = r.communicate()



