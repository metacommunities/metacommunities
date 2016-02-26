import pandas as pd
site = 'github.com/about'
df = pd.read_csv('http://web.archive.org/cdx/search/cdx?url='+site, sep=' ')
df.ix[1]
df.to_csv('full_'+site.replace('/', '_')+ '.csv', sep=',')
df2 = df.iloc[:, [1,2] ]
base = 'https://web.archive.org/web/'
df2.columns = ['date', 'url']
df2['date_formatted'] = pd.to_datetime(df2.date, format='%Y%m%d%H%M%S')
full_url = base+df2.date.astype(str) + '/'+df2.url
full_url.to_csv(site.replace('/', '_') + '.txt',index=False)
