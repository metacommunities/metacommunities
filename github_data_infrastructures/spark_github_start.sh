IPYTHON=1 ./bin/pyspark --driver-memory 1500M --executor-memory 1500M

import json
import redis
ghd = sc.textFile('/media/mackenza/overflow/data/2013-0*').map(lambda x:x.encode('utf-8', errors='ignore')).map(lambda x: json.loads(x.replace('\r\n', '\\r\\n')))


ghd = sc.textFile('/git_data/githubarchive/2013-0*').map(lambda x:x.encode('utf-8', errors='ignore')).map(lambda x: json.loads(x.replace('\r\n', '\\r\\n')))
#sort repos by how often they are forked
forks = ghd.filter(lambda x: 'ForkEvent' in x['type'] and  x.has_key('repository')).map(lambda x:  (x['repository']['name'],1)).reduceByKey(lambda x, y: x+y).map(lambda x:(x[1], x[0])).sortByKey(ascending=False)

