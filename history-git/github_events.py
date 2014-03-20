import ConfigParser
import datetime
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

logger = logging.getLogger('history_git')
logger.info("Module loaded")



class HistoryGitException(Exception):
    pass



def pretty(d, indent=0):
  """
  pretty print a json object -- used to print the data when HistoryGit errors
  """
  for key, value in d.iteritems():
    print '\t' * indent + str(key)
    if isinstance(value, dict):
       pretty(value, indent+1)
    else:
       print '\t' * (indent+1) + str(value)


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")


class HistoryGit():
  """
  History Git is this really grumpy guy who knows exactly how to get all the
  events for a given repo. Just pass him the 'owner/repo' string using .get()
  and he'll get to work, begrudingly.
  """
  
  def __init__(self, path, drop_db=False, commit_stats=False):
    self.commit_stats = commit_stats
    
    # load settings
    self.conf = ConfigParser.ConfigParser()
    self.conf.read(os.path.join(path, 'settings.conf'))
    
    # tables!
    self.create_db(drop_db)
    
    # github
    self.gh = github.Github(login_or_token = self.conf.get('github', 'usr'),
                            password = self.conf.get('github', 'pwd'))
  
  def open_con(self):
    """
    Open connection to mysql db.
    """
    
    self.con = MySQLdb.connect(host=self.conf.get('mysql', 'host'),
                               user=self.conf.get('mysql', 'usr'),
                               passwd=self.conf.get('mysql', 'pwd'),
                               db=self.conf.get('mysql', 'db'),
                               charset='utf8')
    self.cur = self.con.cursor()
  
  
  def close_con(self):
    """
    Commit inserts and close db connection.
    """
    
    self.cur.close()
    self.con.commit()
    self.con.close()
  
  
  def create_db(self, drop_db):
    """
    Maybe drop the database. Create database and tables in the db specific in
    the config, if any don't exists.
    """
    
    logger.info("Checking '%s' database..." % (self.conf.get('mysql', 'db')))
    
    con = MySQLdb.connect(host=self.conf.get('mysql', 'host'),
                          user=self.conf.get('mysql', 'usr'),
                          passwd=self.conf.get('mysql', 'pwd'))
    cur = con.cursor()
    
    # wipe those tables
    if drop_db:
      drop_sql = "DROP DATABASE IF EXISTS %s;" % (self.conf.get('mysql', 'db'))
      cur.execute(drop_sql)
      logger.info("Dropped database %s" % (self.conf.get('mysql', 'db')))
    
    # create db
    create_sql = "CREATE DATABASE IF NOT EXISTS %s;" % (self.conf.get('mysql', 'db'))
    cur.execute(create_sql)
    
    # use db
    use_sql = "USE %s;" % (self.conf.get('mysql', 'db'))
    cur.execute(use_sql)
    
    # create tables
    repo_sql = """
        CREATE TABLE IF NOT EXISTS repo (
          id                  INTEGER PRIMARY KEY,
          name                TINYTEXT,
          full_name           TINYTEXT,
          owner               TINYTEXT,
          created_at          DATETIME,
          description         TEXT,
          fork                TINYINT(1) NOT NULL DEFAULT 0,
          commits             MEDIUMINT NOT NULL DEFAULT 0,
          forks               MEDIUMINT NOT NULL DEFAULT 0,
          pull_requests       MEDIUMINT NOT NULL DEFAULT 0,
          last_commit         DATETIME NULL,
          last_fork           DATETIME NULL,
          last_pull_request   DATETIME NULL,
          collaborators       MEDIUMINT NOT NULL DEFAULT 0,
          contributors        MEDIUMINT NOT NULL DEFAULT 0,
          last_updated        DATETIME NOT NULL
        );
    """
    cur.execute(repo_sql)
    
    commit_sql = """
        CREATE TABLE IF NOT EXISTS commit (
          rid                 INTEGER,
          repo                TINYTEXT,
          owner               TINYTEXT,
          owner_repo          TINYTEXT,
          sha                 CHAR(40) NULL,
          author_login        TINYTEXT NULL,
          author_date         DATETIME NULL,
          committer_login     TINYTEXT NULL,
          committer_date      DATETIME NULL,
          files_n             SMALLINT NULL,
          stats_additions     INTEGER NULL,
          stats_deletions     INTEGER NULL,
          stats_total         INTEGER NULL
        );
    """
    cur.execute(commit_sql)

    fork_sql = """
        CREATE TABLE IF NOT EXISTS fork (
          parent_rid          INTEGER,
          parent_owner        TINYTEXT,
          parent_repo         TINYTEXT,
          parent_owner_repo   TINYTEXT,
          child_rid           INTEGER,
          child_owner         TINYTEXT,
          child_repo          TINYTEXT,
          child_owner_repo    TINYTEXT,
          id                  INTEGER NULL,
          created_at          DATETIME NULL,
          updated_at          DATETIME NULL,
          pushed_at           DATETIME NULL
        );
    """
    cur.execute(fork_sql)
    
    issue_sql = """
        CREATE TABLE IF NOT EXISTS issue (
          rid                 INTEGER,
          repo                TINYTEXT,
          owner               TINYTEXT,
          owner_repo          TINYTEXT,
          id                  INTEGER,
          number              INTEGER,
          user_login          TINYTEXT,
          state               TINYTEXT,
          assignee_login      TINYTEXT,
          created_at          DATETIME,
          updated_at          DATETIME,
          closed_at           DATETIME,
          title               TEXT,
          body                MEDIUMTEXT,
          pull_request        TINYINT(1),
          comments            SMALLINT
        );
    """
    cur.execute(issue_sql)
    
    pull_sql = """
        CREATE TABLE IF NOT EXISTS pull (
          id                    INTEGER,
          number                INTEGER,
          state                 TINYTEXT,
          title                 TEXT,
          user_login            TINYTEXT,
          body                  TEXT,
          created_at            DATETIME,
          updated_at            DATETIME,
          closed_at             DATETIME,
          merged_at             DATETIME,
          merge_commit_sha      CHAR(40),
          assignee_login        TINYTEXT,
          commits               TINYINT,
          comments              TINYINT,
          head_label            TINYTEXT,
          head_ref              TINYTEXT,
          head_sha              CHAR(40),
          head_owner            TINYTEXT,
          head_repo             TINYTEXT,
          head_owner_repo       TINYTEXT,
          head_fork             TINYINT(1),
          head_created_at       DATETIME,
          head_updated_at       DATETIME,
          head_pushed_at        DATETIME,
          base_label            TINYTEXT,
          base_ref              TINYTEXT,
          base_sha              CHAR(40),
          base_owner            TINYTEXT,
          base_repo             TINYTEXT,
          base_owner_repo       TINYTEXT
        );
    """
    cur.execute(pull_sql)
    
    language_sql = """
        CREATE TABLE IF NOT EXISTS language (
          rid           INTEGER NOT NULL,
          name          TINYTEXT NOT NULL,
          bytes         INTEGER NOT NULL,
          last_checked  DATETIME
        );
    """
    cur.execute(language_sql)
    
    cur.close()
    con.close()
    logger.info("Done.")
  
  
  def populate_repo(self):
    """
    See if there are new repos to add to the database. Only basic details are
    added; id, owner, name, description, is it a fork.
    """
    
    logger.info("  Populating repo table...")
    
    # get connection
    self.open_con()
    logger.info("    Opened database connection.")
    
    # 'since' SQL
    select_sql = """
      SELECT max(id)
      FROM repo;
    """
    # start collecting repos
    while True:
      self.cur.execute(select_sql)
      since = self.cur.fetchone()[0]

      if since is None:
        since = github.GithubObject.NotSet
        logger.info("    No records in repo table. Getting all...")
      else:
        logger.info("    Collecting repos with ID greater than %i..." % (since))
      
      start_time = time.time()
      self.n = 0
      self.N = 0

      for rp in self.gh.get_repos(since=since):
        # try to save
        try:
          self.save_repo(rp)
        except:
          print("\nError with repo: %s\n" % (rp._rawData['full_name']))
          raise
        
        # after 50k repos memory starts to get close to full, so break the
        # for loop
        if self.N == 50000:
          break
      
      self.con.commit()
      # results
      time_taken = time.time() - start_time
      logger.info("    Processed %i repos in %.2fs." % (self.N, time_taken))

      # if tried to get repos and N is still 0, then there were no repos to get
      # so break the while loop, otherwise we should "restart" the for loop
      if self.N == 0:
        break
    
    # goodbye
    self.close_con()
    logger.info("    Closed database connection.")
  
  
  def save_repo(self, rp):
    """
    Basic information for a repo is saved when scraped; id, name, full_name,
    description, fork, owner.
    """
    
    data = rp._rawData
    
    # repo level
    keys = ['id', 'name', 'full_name', 'description', 'fork']
    dat = { key: data[key] for key in keys }
    
    # owner level
    try:
      dat['owner'] = data['owner']['login']
    except TypeError:
      logger.warning("        Repo without an owner.")
      pass

    # stats last checked
    dat['last_updated'] = datetime.datetime.fromtimestamp(time.time()) # Now
    
    self.insert(dat, "repo")
  
  
  def get(self, owner_repo):
    """
    Retrieve backlog for a specific 'owner/repo'. Backlog consists of 
    commits, issues, forks and pulls.
    """
    
    # premable
    self.owner_repo = owner_repo
    self.owner, self.repo = owner_repo.split('/')
    logger.info("Starting event collection for %s..." % (self.owner_repo))
    
    # get connection
    self.open_con()
    logger.info("  Opened database connection.")
    
    # go
    self.github_repo = self.gh.get_user(self.owner).get_repo(self.repo)
    
    self.get_commits()
    self.get_issues()
    self.get_forks()
    self.get_pulls()
    
    # goodbye
    self.close_con()
    logger.info("  Closed database connection.")
  
  
  def set_until(self, table, dt, owner_repo="owner_repo", until_type="None"):
    """
    Determine the earliest date for a specific 'owner/repo' and hence retrieve
    events earlier than this.
    """
    
    # any existing events in the table for this repo?
    select_sql = """
      SELECT min(%s)
      FROM %s
      WHERE %s = '%s';
    """ % (dt, table, owner_repo, self.owner_repo)
    self.cur.execute(select_sql)
    until = self.cur.fetchone()[0]

    if until is None:
      logger.info("    No records in %s table. Getting all..." % (table))
      if until_type == "None":
        until = github.GithubObject.NotSet
      else:
        until = datetime.datetime.fromtimestamp(time.time()) # Now
    else:
      until -= datetime.timedelta(0,1)
      logger.info("    Collecting %ss before %s..." % (table, until))
    
    return until
  
  def insert(self, dat, table):
    """
    Generate an INSERT statement off of the keys of the dat dict. Determine
    if records are commited to the db.
    """
    
    fields = ', '.join(dat.viewkeys())
    values = ')s, %('.join(dat.viewkeys())
    insert_sql = "INSERT INTO " + table + " (" + fields + ") VALUES (%(" + values + ")s);"
    
    self.cur.execute(insert_sql, dat)
    
    # shall we commit to the db? -- Oh the irony...
    if self.n >= 1000:
      self.con.commit()
      #logger.info("        added %s records to '%s' table..." % (format(self.n, ",d"), table))
      self.n = 0
    self.n += 1
    self.N += 1
  
  
  def get_commits(self):
    logger.info("  Getting commits...")
    until = self.set_until("commit", "committer_date")
    self.n = 0
    self.N = 0
    
    # start processing the commits
    start_time = time.time()
    
    for cm in self.github_repo.get_commits(until=until):
      try:
        self.save_commit(cm)
      except:
        print("\nError with SHA: %s\n" % (cm._rawData['sha']))
        raise
    
    self.con.commit()
    # results
    time_taken = time.time() - start_time
    logger.info("    Processed %s commits in %.2fs." % (format(self.N, ",d"), time_taken))
  
  def save_commit(self, cm):
    data = cm._rawData
    dat = {
      'owner': self.owner,
      'repo': self.repo,
      'owner_repo': self.owner_repo
    }
    
    dat['sha'] = data['sha']
    
    try:
      dat['author_login'] = data['author']['login']
    except (TypeError, KeyError):
      dat['author_login'] = data['commit']['author']['name']
      
    dat['author_date'] = data['commit']['author']['date']

    if cm.committer is None:
      dat['committer_login'] = data['commit']['committer']['name']
    else:
      dat['committer_login'] = data['committer']['login']

    dat['committer_date']  = data['commit']['committer']['date']
    
    if self.commit_stats:
      dat['files_n']         = len(cm.files)  
      dat['stats_additions'] = cm.stats.additions
      dat['stats_deletions'] = cm.stats.deletions
      dat['stats_total']     = cm.stats.total
    
    self.insert(dat, "commit")
  
  
  def get_forks(self):
    logger.info("  Getting forks...")
    until = self.set_until("fork", "created_at", "parent_owner_repo",
      until_type="dt")
    self.n = 0
    self.N = 0
    
    # start processing the commits
    start_time = time.time()
    
    for frk in self.github_repo.get_forks():
      try:
        self.save_fork(frk, until)
      except:
        print("\nError with fork: %i\n" % (frk._rawData['id']))
        raise
    
    self.con.commit()
    
    # results
    time_taken = time.time() - start_time
    logger.info("    Processed %i forks in %.2fs." % (self.N, time_taken))
  
  def save_fork(self, fork, until):
    data = fork._rawData

    if fork.created_at < until:
      dat = {
        'parent_owner': self.owner,
        'parent_repo': self.repo,
        'parent_owner_repo': self.owner_repo,
        'child_owner': data['owner']['login'],
        'child_repo': data['name'],
        'child_owner_repo': data['full_name'],
        'id': data['id'],
        'created_at': data['created_at'],
        'updated_at': data['updated_at'],
        'pushed_at': data['pushed_at']
      }
      
      self.insert(dat, "fork")
  
  
  def get_issues(self):
    logger.info("  Getting issues...")
    until = self.set_until("issue", "created_at", until_type="ts")
    self.n = 0
    self.N = 0
    start_time = time.time()
    self.issues_enabled = True
    
    try:
      for issue in self.github_repo.get_issues(state="all"):
        self.save_issue(issue, until)
    except github.GithubException as e:
      if e.data['message'] == "Issues are disabled for this repo":
        self.issues_enabled = False
        pass
      else:
        raise
    
    self.con.commit()
    
    # results
    time_taken = time.time() - start_time
    logger.info("    Processed %i issues in %.2fs." % (self.N, time_taken))
  
  def save_issue(self, issue, until):
    data = issue._rawData
    
    if issue.created_at < until:
      dat = {
        'owner': self.owner,
        'repo': self.repo,
        'owner_repo': self.owner_repo,
      }
      
      # issue level
      keys = ['id', 'number', 'state', 'created_at', 'updated_at',
        'closed_at', 'title', 'comments']
      dat.update({ key: data[key]  for key in keys })
      
      # assignee level
      try:
        dat['assignee_login'] = data['assignee']['login']
      except TypeError:
        pass
      
      # user level
      dat['user_login'] = data['user']['login']
      
      try:
        dat['duration'] = (dat['closed_at'] - dat['created_at']).total_seconds
      except TypeError:
        pass
      
      if data['pull_request']['html_url'] is None:
        dat['pull_request'] = 0
      else:
        dat['pull_request'] = 1
      
      try:
        self.insert(dat, "issue")
      except:
        print(dat)
        raise
  
  def get_pulls(self):
    logger.info("  Getting pulls...")
    until = self.set_until("pull", "created_at", "base_owner_repo",
      until_type="ts")
    self.n = 0
    self.N = 0
    
    # start processing the commits
    start_time = time.time()
    
    for pull in self.github_repo.get_pulls(state="all"):
      try:
        self.save_pull(pull, until)
      except:
        print("\nError with Pull ID: %i\n" % (pull._rawData['id']))
        print("Here's the pull object:")
        pretty(pull._rawData)
        raise
    
    self.con.commit()
    
    # results
    time_taken = time.time() - start_time
    logger.info("    Processed %i pulls in %.2fs." % (self.N, time_taken))
  
  def save_pull(self, pull, until):
    data = pull._rawData
    
    if pull.created_at < until:
      dat = {}
      
      # pull level
      keys = ['id', 'number', 'state', 'title', 'body', 'created_at',
        'updated_at', 'closed_at', 'merged_at', 'merge_commit_sha']
      dat.update({ key: data[key]  for key in keys })
        
      # assignee level
      try:
        dat['assignee_login'] = data['assignee']['login']
      except TypeError:
        pass
            
      # generated stats
      dat['commits'] = pull.commits
      dat['comments'] = pull.comments
      
      # user level
      try:
        dat['user_login'] = data['user']['login']
      except TypeError:
        pass
            
      # head level
      keys = ['label', 'ref', 'sha']
      dat.update({ 'head_' + key: data['head'][key]  for key in keys })
      
      try:
        dat['head_owner'] = data['head']['user']['login']
      except TypeError:
        pass
      
      # head repo level
      try:
        keys = ['fork', 'created_at', 'updated_at', 'pushed_at']
        dat.update({ 'head_' + key: data['head']['repo'][key]  for key in keys })
        
        dat['head_repo'] = data['head']['repo']['name']
        dat['head_owner_repo'] = data['head']['repo']['full_name']
      except TypeError:
        pass
      
      # base level
      keys = ['label', 'ref', 'sha']
      dat.update({ 'base_' + key: data['base'][key]  for key in keys })
      dat['base_owner'] = data['base']['user']['login']
      dat['base_repo'] = data['base']['repo']['name']
      dat['base_owner_repo'] = data['base']['repo']['full_name']
      
      self.insert(dat, "pull")


