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


def generate_repo_data_from_local_archive(start = '2013-03-01', days = 1):
    """read created_at dates for repositories. These dates are only included in the archive date 
    as a field beginning at '2012-03-10-22' hrs. All repos before that, don't have it in the github data. 
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
            evs.update(read_one_github_hour(fpi))
        # increment date
        current_date +=  datetime.timedelta(1)
    # evs_df = pd.DataFrame.from_dict(evs, orient = 'index')
    # evs_df.columns = [ 'created_at']
    # return evs_df

def read_one_github_hour(filename, save_to_redis = True):
    """ Read all events in one hour of archive data. The field name 'repo' changes to 'repository'
    in March 2012. But the 'repo' field had no creation date. Is this part of the repackaging of the API 
    for purposes of publication?
    """
    if save_to_redis:
        pipe = red.pipeline()
    # the one hour of github archive
    f =  gzip.GzipFile(filename)
    # One event per line.
    try:
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

def get_creation_dates_from_API(query, number):
    repos = red.srandmember(query,number)

    for r in repos:
        try:
            res = git.get_repo(r)
            # print res.created_at
            #store datetime as milliseconds since epoch
            # to reverse: time.gmtime(t)
            repo_dates[r] = time.mktime(res.created_at.timetuple())
            red.zadd('repos:created_at', r, mktime(res.created_at.timetuple()))
        except Exception, e:
            print e
    return repo_dates

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Monitor GitHub activity.")
    parser.add_argument("--since", default=None, help="The starting date.")
    # parser.add_argument("--until", default=None, help="The end date.")
    parser.add_argument("--days", default=1, help="The number of days.")

    args = parser.parse_args()
    generate_repo_data_from_local_archive(start  = args.since, days = int(args.days))
