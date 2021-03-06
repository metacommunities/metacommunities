import github as gh
import redis
import time
import gzip
import json
import pandas as pd
import datetime
import dateutil
import os.path
import ConfigParser

path = '/home/mackenza/.history_git/'
conf = ConfigParser.ConfigParser()

data_path = '/git_data/githubarchive/'
conf.read(os.path.join(path, 'settings.conf'))
# github
git = gh.Github(login_or_token = conf.get('github', 'user'),
                        password = conf.get('github', 'password'))
red = redis.Redis(db ='2')


def retrieve_repos_by_date_created(start_date = '2008-01-01', end_date = '2009-01-01'):
    """ return repo names sorted by date as a Pandas timeseries
    arguments:
    start_date: in '2008-02-02' format
    start_date: in '2008-02-02' format"""
    st = time.mktime(time.strptime(start_date, '%Y-%m-%d'))
    fin = time.mktime(time.strptime(end_date, '%Y-%m-%d'))
    res= red.zrangebyscore('repos:created_at', st,fin, withscores = True)
    ts = pd.Series({time.ctime(r[1]):r[0] for r in res})
    ts.index = pd.to_datetime(ts.index)
    return ts

def get_repo_creation_date(repo):
    """ Look up repo creation date from redis store and if its 
    not there, get it from the Github API"""
    try:
        cdate = red.zscore('repos:created_at', repo)
        if cdate is None:
            load_repo_creation_dates_from_API([repo])
            cdate = red.zscore('repos:created_at', repo)
        return time.ctime(cdate)
    except Exception, e:
        print e


def retrieve_repos_by_date_order(start = 0, end = 100):
    """ return a dictionary of repo names keyed by date"""
    res = red.zrange('repos:created_at', start, end, withscores=True)
    return {time.ctime(r[1]):r[0] for r in res}

def generate_repo_data_from_local_archive(start = '2013-03-01', days = 1):
    """read created_at dates for repositories. These dates are only included in the archive date 
    as a field beginning at '2012-03-10-22' hrs. All repos before that, don't have it in the github data. 
    These need to be retrieved from the Github API
    """
    print start
    start_hour = 0
    evs = {}
    current_date =  datetime.datetime.strptime(start, '%Y-%m-%d')

    # process days
    for d in range(0, days):
        tt=current_date.timetuple()
        print tt
        start_day = tt.tm_mday
        start_month = tt.tm_mon
        start_year = tt.tm_year
        fp = os.path.join(data_path, '{year}-{month:02d}-{day:02d}-'.format(**{'year':start_year, 'month':start_month, 'day':start_day}))
        # read one day
        for i in range(start_hour,23):
            fpi = fp  + str(i) + '.json.gz'
            res = read_one_github_hour(fpi)
            if res is not None:
                evs.update(res)

        # increment date
        current_date +=  datetime.timedelta(1)
    # evs_df = pd.DataFrame.from_dict(evs, orient = 'index')
    # evs_df.columns = [ 'created_at']
    # return evs_df

def read_one_github_hour(filename, save_to_redis = True):
    """ Read all events in one hour of githubarchive data. The field name 'repo' changes to 'repository'
    in March 2012. But the 'repo' field had no creation date. Is this part of the repackaging of the API 
    for purposes of publication?
    """
    if save_to_redis:
        pipe = red.pipeline()
    #one hour of github archive
    if os.path.isfile(filename) is False:
	print 'Could not find file {}'.format(filename)	
	return
    try:
    	f =  gzip.GzipFile(filename)
    	# One event per line.
        events = [line.decode("utf-8", errors="ignore") for line in f]
    except Exception, e:
        # print(e)
        return 

    count = len(events)
    if count == 1:
        # probably an early formatted file -- not sure when these changed to \n separated
        events = events[0].replace('}{', '}\n{')
        events = [e for e in events.split('\n')]
        count = len(events)

    # One event per line.
    print ' processing  {} events '.format(count)
    evs = {}
    for n, line in enumerate(events):
        # Parse the JSON of this event.
        try:
            event = json.loads(line)
            #print event
            if event.has_key('repository'):
                repository = event['repository']
                date = repository['created_at']
                repo = '{}/{}'.format(repository['owner'], repository['name'])
                creation_date = dateutil.parser.parse(date)
	#	print creation_date
                evs[repo] = time.mktime(creation_date.timetuple())
                repo_attr = {}
                repo_attr['fork'] = repository['fork']
                if repository.has_key('description'):
                    repo_attr['description'] = repository['description']
                repo_attr['timezone'] = creation_date.tzinfo
                pipe.hmset('repo:'+repo, repo_attr)
        except Exception, ex:
            print( 'exception: {}'.format(ex))
    print 'Found {} repository creation dates'.format(len(evs))
    ## store in redis db
    #@TODO: change the db and key name -- this is for testing only
    # red.hmset('test:repos:created_at', evs)
    if save_to_redis and len(evs.items()) > 0:
        red.zadd('repos:created_at', **evs)
        pipe.execute()
    return evs

def load_repo_creation_dates_from_API(repos):
    """ looks up creation dates for repos in the list
    and stores them in Redis zset"""
    repo_dates = {}
    for r in repos:
        try:
            res = git.get_repo(r)
            #store datetime as milliseconds since epoch
            # to reverse: time.gmtime(t)
            repo_dates[r] = time.mktime(res.created_at.timetuple())
            print res.created_at
            red.zadd('repos:created_at', r, time.mktime(res.created_at.timetuple()))
        except Exception, e:
            print e
    return repo_dates

# if __name__ == "__main__":
#     import argparse
#     parser = argparse.ArgumentParser(description="Monitor GitHub activity.")
#     parser.add_argument("--since", default=None, help="The starting date.")
#     # parser.add_argument("--until", default=None, help="The end date.")
#     parser.add_argument("--days", default=1, help="The number of days.")

#     args = parser.parse_args()
#     generate_repo_data_from_local_archive(start  = args.since, days = int(args.days))
