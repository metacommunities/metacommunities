# this script takes a url and fetches all the urls
# of versions stored at InternetArchive. It saves the full
# urls as a csv file in the local directory

import pandas as pd
import sys

if sys.argv[1] !=None:
    site = sys.argv[1]
else:
    site = 'github.com/about'

print('getting versions for %s'%site)
df = pd.read_csv('http://web.archive.org/cdx/search/cdx?url='+site, sep=' ')
df.ix[1]
df.to_csv('full_'+site.replace('/', '_')+ '.csv', sep=',')
df2 = df.iloc[:, [1,2] ]
base = 'https://web.archive.org/web/'
df2.columns = ['date', 'url']
df2['date_formatted'] = pd.to_datetime(df2.date, format='%Y%m%d%H%M%S')
full_url = base+df2.date.astype(str) + '/'+df2.url
full_url.to_csv(site.replace('/', '_') + '.csv',index=False)
