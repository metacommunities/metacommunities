import pandas as pd
site = 'github.com/about'
df = pd.read_csv('http://web.archive.org/cdx/search/cdx?url='+site, sep=' ')
df = df.icol([1,2])
base = 'https://web.archive.org/web/'
df.columns = ['date', 'url']
df['date_formatted'] = pd.to_datetime(df.date, format='%Y%m%d%H%M%S')
full_url = base+df.date.astype(str) + '/'+df.url
full_url.to_csv(site.replace('/', '_') + '.txt',index=False)
