"""
TODO:
 - payload extraction for all event types
"""

import datetime as dt
import logging
import MySQLdb
import pandas as pd
import requests
import textwrap


def create_db(config):
  con = MySQLdb.connect(host=config['host'], user=config['usr'],
    passwd=config['pwd'])
  cur = con.cursor()

  # create db
  sql = "CREATE DATABASE IF NOT EXISTS %s;" % (config['db'])
  cur.execute(sql)

  # use db
  sql = "USE %s;" % (config['db'])
  cur.execute(sql)

  # create tables
  sql = """
      CREATE TABLE IF NOT EXISTS event (
        id            BIGINT NOT NULL PRIMARY KEY,
        repo          TINYTEXT,
        owner         TINYTEXT,
        owner_repo    TINYTEXT,
        type          TINYTEXT,
        created_at    DATETIME,
        actor         TINYTEXT,
        push_id       INT NULL,
        size          INT NULL,
        distinct_size INT NULL
      );
  """
  cur.execute(sql)

  sql = """
      CREATE TABLE IF NOT EXISTS commit (
        eid         BIGINT,
        sha         TINYTEXT,
        author      TINYTEXT,
        message     TEXT NULL,
        is_distinct TINYINT
      );
  """
  cur.execute(sql)

  cur.close()
  con.close()

def extract_event_info(event):
  eve = {}
  commits = []
  
  # all event types have the following info
  eve['id']         = event['id']
  eve['type']       = event['type']
  eve['created_at'] = event['created_at']
  eve['actor']      = event['actor']['login']
  
  # process payload based on type
  if event['type'] == 'PushEvent':
    payload = { 'payload_' + keep_key: event['payload'][keep_key] for keep_key in
      ('push_id', 'size', 'distinct_size') }
    
    for commit in event['payload']['commits']:
      cmmt = {}
      cmmt['sha'] = commit['sha']
      cmmt['author'] = commit['author']['name']
      cmmt['message'] = commit['message']
      cmmt['distinct'] = commit['distinct']
      commits.append(cmmt)
  
  # TODO payloads for the following
  
  # ForkEvent
  
  # WatchEvent
  
  # PullRequestEvent
  
  eve.update(payload)
  
  return {'event': eve, 'commits':commits}





class RequestLimiter():
  """
  This class keeps track of the request limits imposed by GitHub.
  """
  
  def __init__(self, auth):
    # track number of requests made
    # quickly than calling across the API every time
    self.n = 0 
    
    # details for acessing GH rate info
    self.usr = auth['usr']
    self.pwd = auth['pwd']
    self.url = 'https://api.github.com/rate_limit'
    
    self.refresh()
  
  def refresh(self):
    """
    Refresh the limit, remaining and reset measures and reassess if we're
    still OK to carry on.
    """
    
    # initiate the measures
    r = requests.get(self.url, auth=(self.usr, self.pwd))
    
    if r.status_code != requests.codes.ok:
      logging.error('HTTP ERROR %s occured' % (r.status_code))
    
    r.raise_for_status()
    
    r = r.json()
    self.limit      = r['resources']['core']['limit']
    self.remaining  = r['resources']['core']['remaining']
    self.reset      = r['resources']['core']['reset']
    
    if self.limit < 5000:
      err_msg = textwrap.dedent("""\
        Limit is too small (%i). Check username and password for GitHub
        in 'settings.conf'.""" % (self.limit))
      logging.error(err_msg)
      raise StandardError(err_msg)
    
    # if the number of remaining requests are above 1% of the limit then
    # we're good to keep going
    self.ok = self.remaining > 50
    
    self.reset_time = dt.datetime.fromtimestamp(self.reset).strftime('%H:%M')
    msg = "Rate limit status: %i limit, %i remaining, reset at %s" % \
      (self.limit, self.remaining, self.reset_time)
    logging.info(msg)
  
  def update(self):
    """
    dont need to refresh() just to keep track of progress
    refresh after 990 requests, this gives us 5 refreshes before entering into
    the final 50 requests for the hour
    """
    self.n += 1
    if self.n % 990 == 0:
      self.refresh()
      self.n = 0
  

#class RepoEventPage:
#  """
#  This class requests a page of event history for a given repo over the GitHub
#  API and formats it so it can be stored.
#  """
#  def __init__(self):
#    
#  
#  def get(self, user, repo):
#    
#  


#def get_repository_event(user, repo):
#    """
#    Returns a list of events as dictionaries
#    from the API using url of the form
#    https://api.github.com/repos/torvalds/linux/events
#    Arguments
#    ----------------------------------
#    user: name of repo owner
#    repo: name of repository
#    url: full api url of repo
#    limit: number of events to fetch
#    """

#    suffix = 'events'
#    if url is not  None:
#        url = '/'.join([url, suffix])
#    else:
#        base_url = 'https://api.github.com/repos'
#        url = '/'.join([base_url, user, repo, suffix])
#    events = []
#    try:
#        url_next = ''
#        current_count = 0
#        while current_count < limit:
#            events_req = requests.get(url, auth=(USER, PASSWORD))
#            events = events + events_req.json()
#            if events_req.links.has_key('next'):
#                url_next = events_req.links['next']['url']
#                print url_next
#            else:
#                break
#            if url == url_next:
#                break
#            else:
#                url = url_next + '&per_page=100'
#            current_count = len(events)
#            time.sleep(0.72)

#    except Exception, e:
#        print e
#    return events

#    
#def unpack_repoItem(repoItem, repos_df, parent):
#    '''
#    This does the work of extracting relevant variables from the json item
#    and returning a data frame

#    Parameters
#    -------------------------------------
#    repoItem is the json item to be unpacked
#    repos_df is the data frame where data from the current item will be appended
#    '''

#    id = [it['id'] for it in repoItem]
#    full_name = [it['full_name'] for it in repoItem]
#    description = [it['description'] for it in repoItem]
#    language = [it['language'] for it in repoItem]
#    fork = [it['fork'] for it in repoItem]
#    forks = [it['forks'] for it in repoItem]
#    size = [it['size'] for it in repoItem]
#    watchers = [it['watchers'] for it in repoItem]
#    open_issues = [it['open_issues'] for it in repoItem]
#    created_at = [it['created_at'] for it in repoItem]
#    pushed_at = [it['pushed_at'] for it in repoItem]
#    updated_at = [it['updated_at'] for it in repoItem]
#    has_downloads = [it['has_downloads'] for it in repoItem]
#    has_issues = [it['has_issues'] for it in repoItem]
#    has_wiki = [it['has_wiki'] for it in repoItem]
#    parent_id = 1
#    parent_name = parent

#    data_dict = {
#            'id': id,
#            'full_name': full_name,
#            'description': description,
#            'language': language,
#            'fork': fork,
#            'forks': forks,
#            'size': size,
#            'watchers': watchers,
#            'open_issues': open_issues,
#            'created_at': created_at,
#            'pushed_at': pushed_at,
#            'updated_at': updated_at,
#            'has_downloads': has_downloads,
#            'has_issues': has_issues,
#            'has_wiki': has_wiki,
#            'parent_id': parent_id,
#            'parent_name': parent_name} 

#    temp_df  = pd.DataFrame(data_dict, index = id)      
#    repos_df = repos_df.append(temp_df)
#    return repos_df



#    
#def unpack_repoItem_pulls(repoItem, repos_df, parent):
#    '''
#    This does the work of extracting relevant variables from the json item
#    and returning a data frame
#    Parameters
#    ------------------------------
#    repoItem:the json item to be unpacked
#    repos_df: the data frame where data from the current item will be appended
#    '''
#    id = [it['id'] for it in repoItem]
#    state = [it['state'] for it in repoItem]
#    title = [it['title'] for it in repoItem]
#    body = [it['body'] for it in repoItem]
#    number = [it['number'] for it in repoItem]
#    merged_at = [it['merged_at'] for it in repoItem]
#    closed_at = [it['closed_at'] for it in repoItem]
#    created_at = [it['created_at'] for it in repoItem]
#    head_created_at = [it['head']['repo']['created_at'] for it in repoItem]
#    head_full_name = [it['head']['repo']['full_name'] for it in repoItem]
#    head_fork = [it['head']['repo']['fork'] for it in repoItem]
#    head_forks = [it['head']['repo']['forks'] for it in repoItem]
#    base_full_name = [it['base']['repo']['full_name'] for it in repoItem]
#    pull_user = [it['user']['login'] for it in repoItem]
#    data_dict = {
#            'id': id,
#            'state': state,
#            'title': title,
#            'body': body,
#            'number': number,
#            'merged_at': merged_at,
#            'closed_at': closed_at,
#            'created_at': created_at,
#            'head_created_at': head_created_at,
#            'head_full_name': head_full_name,
#            'head_fork': head_fork,
#            'head_forks': head_forks,
#            'base_full_name': base_full_name,
#            'pull_user': pull_user} 

#    temp_df  = pd.DataFrame(data_dict, index = id)      
#    repos_df = repos_df.append(temp_df)
#    return repos_df

