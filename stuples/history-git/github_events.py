import ConfigParser
import github
import logging
import MySQLdb
import numpy as np
import os
import requests
import sys
import textwrap
import time
import warnings

# supress MySQL Warnings
warnings.filterwarnings('ignore', category=MySQLdb.Warning)

#class RequestLimiter():
#  """
#  This class keeps track of the request limits imposed by GitHub.
#  """
#  
#  def __init__(self, auth):
#    # track number of requests made
#    # quickly than calling across the API every time
#    self.n = 0 
#    
#    # details for acessing GH rate info
#    self.usr = auth['usr']
#    self.pwd = auth['pwd']
#    self.url = 'https://api.github.com/rate_limit'
#    
#    self.refresh()
#  
#  def refresh(self):
#    """
#    Refresh the limit, remaining and reset measures and reassess if we're
#    still OK to carry on.
#    """
#    
#    # initiate the measures
#    r = requests.get(self.url, auth=(self.usr, self.pwd),
#      headers={"Accept":"application/vnd.github.v3+json"})
#    
#    if r.status_code != requests.codes.ok:
#      logging.error('HTTP ERROR %s occured' % (r.status_code))
#    
#    r.raise_for_status()
#    
#    r = r.json()
#    self.limit      = r['resources']['core']['limit']
#    self.remaining  = r['resources']['core']['remaining']
#    self.reset      = r['resources']['core']['reset']
#    
#    if self.limit < 5000:
#      err_msg = textwrap.dedent("""\
#        Limit is too small (%i). Check username and password for GitHub
#        in 'settings.conf'.""" % (self.limit))
#      logging.error(err_msg)
#      raise StandardError(err_msg)
#    
#    # if the number of remaining requests are above 1% of the limit then
#    # we're good to keep going
#    self.ok = self.remaining > 50
#    
#    self.reset_time = datetime.datetime.fromtimestamp(self.reset).strftime('%H:%M')
#    msg = "Rate limit status: %i limit, %i remaining, reset at %s" % \
#      (self.limit, self.remaining, self.reset_time)
#    logging.info(msg)
#  
#  def update(self):
#    """
#    dont need to refresh() just to keep track of progress
#    refresh after 990 requests, this gives us 5 refreshes before entering into
#    the final 50 requests for the hour
#    """
#    self.n += 1
#    if self.n % 990 == 0:
#      self.refresh()
#      self.n = 0
  

class HistoryGit():
  """
  History Git is this really grumpy guy who knows exactly how to get all the
  events for a given repo. Just pass him the 'owner/repo' string using .get()
  and he'll get to work, begrudingly.
  """
  
  def __init__(self, path, drop_db=False):
    # load settings
    self.conf = ConfigParser.ConfigParser()
    self.conf.read(os.path.join(path, 'settings.conf'))
    
    # tables!
    self.create_db(drop_db)
    
    # github
    self.gh = github.Github(login_or_token = self.conf.get('github', 'usr'),
                            password = self.conf.get('github', 'pwd'))

  def open_con(self):
    self.con = MySQLdb.connect(host=self.conf.get('mysql', 'host'),
                               user=self.conf.get('mysql', 'usr'),
                               passwd=self.conf.get('mysql', 'pwd'),
                               db=self.conf.get('mysql', 'db'))
    self.cur = self.con.cursor()
  
  def close_con(self):
    self.cur.close()
    self.con.commit()
    self.con.close()

  def create_db(self, drop_db):
    con = MySQLdb.connect(host=self.conf.get('mysql', 'host'),
                          user=self.conf.get('mysql', 'usr'),
                          passwd=self.conf.get('mysql', 'pwd'))
    cur = con.cursor()
    
    # wipe those tables
    if drop_db:
      drop_sql = "DROP DATABASE IF EXISTS %s;" % (self.conf.get('mysql', 'db'))
      cur.execute(drop_sql)
      #logging.info("Dropped database %s" % (self.conf.get('mysql', 'db')))
    
    # create db
    create_sql = "CREATE DATABASE IF NOT EXISTS %s;" % (self.conf.get('mysql', 'db'))
    cur.execute(create_sql)
    
    # use db
    use_sql = "USE %s;" % (self.conf.get('mysql', 'db'))
    cur.execute(use_sql)
    
    # create tables
    commit_sql = """
        CREATE TABLE IF NOT EXISTS commit (
          repo                TINYTEXT NULL,
          owner               TINYTEXT NULL,
          owner_repo          TINYTEXT,
          sha                 CHAR(40),
          author_login        TINYTEXT,
          author_date         DATETIME,
          committer_login     TINYTEXT,
          committer_date      DATETIME,
          files_n             SMALLINT,
          stats_additions     INTEGER,
          stats_deletions     INTEGER,
          stats_total         INTEGER
        );
    """
    cur.execute(commit_sql)
    
    #logging.info("Created tables in db %s" % (self.conf.get('mysql', 'db')))
    
    cur.close()
    con.close()
  
  def get(self, owner_repo):
    """
    this starts the whole retrieval process
    """
    # premable
    self.owner_repo = owner_repo
    self.owner, self.repo = owner_repo.split('/')
    
    # get connection
    self.open_con()
    
    # go
    self.get_commits()
    
    # goodbye
    self.close_con()
  

  
  def get_commits(self):
    # any existing commits in the database?
    select_sql = """
      SELECT min(committer_date)
      FROM commit
      WHERE owner_repo = '%s';
    """ % (self.owner_repo)
    self.cur.execute(select_sql)
    until = self.cur.fetchone()[0]

    if until is None:
      until = github.GithubObject.NotSet
    else:
      until -= datetime.timedelta(0,1)
    
    # start
    logging.info("Getting commits for %s." % (self.owner_repo))
    repo = self.gh.get_user(self.owner).get_repo(self.repo)
    n = 0
    N = 0

    insert_sql = """
      INSERT INTO commit (owner, repo, owner_repo, sha, author_login,
        author_date, committer_login, committer_date, files_n, stats_additions,
        stats_deletions, stats_total)
      VALUES (%(owner)s, %(repo)s, %(owner_repo)s, %(sha)s, %(author_login)s,
        %(author_date)s, %(committer_login)s, %(committer_date)s, %(files_n)s,
        %(stats_additions)s, %(stats_deletions)s, %(stats_total)s);
    """
    
    # start processing the commits
    start_time = time.time()
    for cm in repo.get_commits(until=until):
      commit = {
        'owner': self.owner,
        'repo': self.repo,
        'owner_repo': self.owner_repo
      }
      
      commit['sha'] = cm.sha

      if cm.author is None:
        commit['author_login'] = cm.commit.author.name
      else:
        commit['author_login'] = cm.author.login

      commit['author_date'] = cm.commit.author.date

      if cm.committer is None:
        commit['committer_login'] = cm.commit.committer.name
      else:
        commit['committer_login'] = cm.committer.login

      commit['committer_date']  = cm.commit.committer.date
      commit['files_n']         = len(cm.files)  
      commit['stats_additions'] = cm.stats.additions
      commit['stats_deletions'] = cm.stats.deletions
      commit['stats_total']     = cm.stats.total
      
      #self.cur.execute(insert_sql, commit)

      # shall we commit? -- Oh the irony...
      if n >= 100:
        self.con.commit()
        n = 0
      n += 1
      N += 1
    
    # results
    time_taken = time.time() - start_time
    sys.stdout.write("\nProcessed %i commits in %.2fs.\n" % (N, time_taken))
  
  
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

