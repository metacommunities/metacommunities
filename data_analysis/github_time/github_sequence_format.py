import githubarchive_data as gha
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

#this is only a test dataset - a couple of hours on one day
df = gha.load_local_archive_dataframe()
df = df.dropna()
url = [r['url'] for r in df.repository.tolist()]
df['url'] = url
cols = ['id', 'time', 'event']
savedf = df[['url', 'created_at', 'type']]
savedf.colums = cols
savedf.to_csv('tse.csv')
# to get in TraMineR sts format

def create_SPS_record(repository_url):

	#aiming to get a repository in the State-Permanence-Sequence format (SPS)
	#(000,12)-(0W0,9)-(0WU,5)-(1WU,2)
	
	ex = savedf.get_group(repository_url)
	ex.created_at = pd.to_datetime(ex['created_at'])


	#the key function here is 'shift'
	ex['duration'] = (ex['created_at']-ex['created_at'].shift()).fillna(0)


	#convert to seconds
	ex['seconds'] = [d.item()/1000000000 for d in ex.duration]
	sps = ex[['type', 'seconds']]
	sps['seconds'] = sps.seconds.astype('str')
	return ','.join(['('+t+','+s+')' for t, s in zip(sps.type.tolist(), sps.seconds.tolist())])



f= open('sps.txt', 'w')
sps = [create_SPS(repo) for repo in savedf.groups.keys()]
[f.write(line+'\n') for line in sps]
f.close()


library('TraMineR')
tse=read.csv('tse.csv')

