import datetime as dt
import logging
import MySQLdb
import pandas as pd
import requests
import textwrap
import time

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
    r = requests.get(self.url, auth=(self.usr, self.pwd),
      headers={"Accept":"application/vnd.github.v3+json"})
    
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
  

class HistoryGit():
  """
  History Git is this really grumpy guy who knows exactly how to get all the
  events for a given repo. Just pass him the 'owner/repo' string using .get()
  and he'll get to work, begrudingly.
  """
  
  def __init__(self, config, drop_db=False):
    self.github = dict(config.items('github'))
    self.mysql  = dict(config.items('mysql'))
    
    self.limiter = RequestLimiter(auth=self.github)
    
    self.create_db(drop_db)
  
  def create_db(self, drop_db):
    con = MySQLdb.connect(host=self.mysql['host'], user=self.mysql['usr'],
      passwd=self.mysql['pwd'])
    cur = con.cursor()
    
    # wipe those tables
    if drop_db:
      drop_sql = "DROP DATABASE %s;" % (self.mysql['db'])
      cur.execute(drop_sql)
    
    # create db
    create_sql = "CREATE DATABASE IF NOT EXISTS %s;" % (self.mysql['db'])
    cur.execute(create_sql)

    # use db
    use_sql = "USE %s;" % (self.mysql['db'])
    cur.execute(use_sql)

    # create tables
    event_sql = """
        CREATE TABLE IF NOT EXISTS event (
          id                  BIGINT NOT NULL PRIMARY KEY,
          repo                TINYTEXT NULL,
          owner               TINYTEXT NULL,
          owner_repo          TINYTEXT,
          type                TINYTEXT,
          created_at          DATETIME,
          actor               TINYTEXT,
          api_page            INT,
          push_push_id        INT NULL,
          push_size           INT NULL,
          push_distinct_size  INT NULL,
          fork_forkee_full_name TINYTEXT NULL,
          watch_action          TINYTEXT NULL
        );
    """
    cur.execute(event_sql)

    commit_sql = """
        CREATE TABLE IF NOT EXISTS commit (
          eid         BIGINT,
          sha         TINYTEXT,
          author      TINYTEXT,
          message     TEXT NULL,
          is_distinct TINYINT
        );
    """
    cur.execute(commit_sql)

    cur.close()
    con.close()
  
  
  def get(self, owner_repo):
    """
    this starts the whole retrieval process
    """
    self.owner_repo = owner_repo
    
    # premable
    self.con = MySQLdb.connect(host=self.mysql['host'], user=self.mysql['usr'],
      passwd=self.mysql['pwd'], db=self.mysql['db'])
    self.cur = self.con.cursor()
    
    url_base = 'https://api.github.com/repos/%s/events?page=%i'
    cutoff_ts = self.get_cutoff_timestamp()
    
    self.limiter.refresh()
    
    page_history = []
    page = 0
    power = 0
    n = 0
    
    # start getting pages
    while True:
      page += 1
      page_history.append(page)
      url = url_base % (owner_repo, page)
      pg = requests.get(url, auth=(self.github['usr'], self.github['pwd']),
        headers={"Accept":"application/vnd.github.v3+json"})
      
      # is page good?
      pg.raise_for_status()
      pg = pg.json()
      
      # is the page empty? we should never run out of requests because of the limiter
      # so an empty page is because we've reached the end of the history
      if pg:
        # any events with a date before start_ts?
        event_ts = [ time.mktime(time.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ'))
          for event in pg ]
        keepers = [ i for i, ets in enumerate(event_ts) if ets < cutoff_ts]
        
        if keepers:
          print("process page %i" % (page_history[-1]))
          for k in keepers:
            n += 1
            #self.save_event(pg[k])
        
        # we've successfully made and, potentially, processed a single whole
        # request, so we can now sleep if we have to
        self.limiter.update()
      else:
        break
        #print("break")
    
    # the end
    self.cur.close()
    self.con.close()
    logging.info("Added %i events from %i pages for repo: %s" % (n, page, owner_repo))
  
  
  def save_event(self, event):
    """
    extracts the 'useful' event info which depends on the event type and then
    uploads this info to the mysql database
    """
    eve = {}
    commits = []
    
    # all event types have the following info
    eve['id']         = event['id']
    eve['type']       = event['type']
    eve['created_at'] = event['created_at']
    eve['actor']      = event['actor']['login']
    
    # process payload based on type:
    if event['type'] == 'PushEvent':
      # PushEvent payload:
      #   push_id
      #   size
      #   distinct_size
      payload = { 'push_' + keep_key: event['payload'][keep_key] for keep_key in
        ('push_id', 'size', 'distinct_size') }
      
      for commit in event['payload']['commits']:
        cmmt = {}
        cmmt['sha']      = commit['sha']
        cmmt['author']   = commit['author']['name']
        cmmt['message']  = commit['message']
        cmmt['distinct'] = commit['distinct']
        commits.append(cmmt)
    
    elif event['type'] == 'ForkEvent':
      # ForkEvent payload:
      #   forkee:
      #     full_name
      payload['fork_'] = event['payload']['forkee']['full_name']
    
    elif event['type'] == 'WatchEvent':
      # WatchEvent payload:
      #   action
      payload['watch_action'] = event['payload']['action']
    
    #elif event['type'] == 'PullRequestEvent':
    #  # PullRequestEvent payload:
    #  #   
    #  payload = { 'pullrequest_' + keep_key: event['payload'][keep_key] for keep_key in
    #    ('push_id', 'size', 'distinct_size') }
    #
    #    elif event['type'] == 'IssueEvent':
    #      # IssueEvent payload:
    #      #   action
    #      #   issue:
    #      #     
    #      
    #      
    #      
    #    
    #    elif event['type'] == 'IssueCommentEvent':
    #      # IssueCommentEvent payload:
    #      #   action
    #      #   issue:
    #      #     
    #      #   comment
    
    # add payload to event object    
    eve.update(payload)
    
    # if event was a push event then we need to also save the commits
    if not info['commits']:
      self.upload_commit(info['commits'])
  
  
  def upload_event(self, event):
    """
    construct an INSERT statement based on the event dictionary
    """
    event_sql = "INSERT INTO event (a,b,c) VALUES (%(qwe)s, %(asd)s, %(zxc)s);"
    self.cur.execute(event_sql, info['event'])
  
  
  def upload_commit(self, commit):
    """
    construct an INSERT statement based on the commit dictionary
    """
    commmits_sql = "INSERT INTO commit (a,b,c) VALUES (%(qwe)s, %(asd)s, %(zxc)s);"
    self.cur.execute(commits_sql, info['commits'])  
  
  
  def get_cutoff_timestamp(self):
    """
    if we've collected data before on this repo then it'll be in the database,
    if so then we use the earliest timestamp as our starting point, else
    we just use current time
    """
    sql_prev_hist = """
      SELECT min(created_at)
      FROM event 
      WHERE owner_repo = '%s'
    """ % (self.owner_repo)
    
    self.cur.execute(sql_prev_hist)
    
    cutoff_ts = self.cur.fetchone()[0]
    
    if not cutoff_ts:
      cutoff_ts = time.time()
    
    return cutoff_ts

