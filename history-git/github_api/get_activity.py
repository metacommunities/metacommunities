import datetime
import github
import time

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

def get(self, owner_repo):
  """
  Retrieve backlog for a specific 'owner/repo'. Backlog consists of 
  commits, issues, forks and pulls.
  """
  
  # premable
  self.owner_repo = owner_repo
  self.owner, self.repo = owner_repo.split('/')
  self.logger.info("Starting event collection for %s..." % (self.owner_repo))
  
  # get connection
  self.open_con()
  self.logger.info("  Opened database connection.")
  
  # go
  self.github_repo = self.gh.get_user(self.owner).get_repo(self.repo)
  
  self.get_commits()
  self.get_issues()
  self.get_forks()
  self.get_pulls()
  
  # goodbye
  self.close_con()
  self.logger.info("  Closed database connection.")


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
    self.logger.info("    No records in %s table. Getting all..." % (table))
    if until_type == "None":
      until = github.GithubObject.NotSet
    else:
      until = datetime.datetime.fromtimestamp(time.time()) # Now
  else:
    until -= datetime.timedelta(0,1)
    self.logger.info("    Collecting %ss before %s..." % (table, until))
  
  return until




def get_commits(self):
  self.logger.info("  Getting commits...")
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
  self.logger.info("    Processed %s commits in %.2fs." % (format(self.N, ",d"), time_taken))

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
  self.logger.info("  Getting forks...")
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
  self.logger.info("    Processed %i forks in %.2fs." % (self.N, time_taken))

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
  self.logger.info("  Getting issues...")
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
  self.logger.info("    Processed %i issues in %.2fs." % (self.N, time_taken))

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
  self.logger.info("  Getting pulls...")
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
  self.logger.info("    Processed %i pulls in %.2fs." % (self.N, time_taken))

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

