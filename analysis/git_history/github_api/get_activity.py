import datetime
import github
import time
from pprint import pprint

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
    self.logger.info("    Opened database connection.")
    
    # go
    self.github_repo = self.gh.get_user(self.owner).get_repo(self.repo)
    self.setup_repo_summary()
    self.get_commits()
    self.get_issues()
    self.update_open_issues()
    self.get_forks()
    self.get_pulls()
    self.update_open_pulls()
    self.update_repo_summary()
    
    # goodbye
    self.close_con()
    self.logger.info("    Closed database connection.")


def setup_repo_summary(self):
    """
    Set up empty repo summary, if one doesn't already exist for 'owner/repo'
    """
    
    select_sql = """
        SELECT backlog_complete
        FROM repo_summary
        WHERE full_name = '%s'
    """ % (self.owner_repo)
    self.cur.execute(select_sql)
    backlog = self.cur.fetchone()[0]
    
    if backlog == None:
        now = datetime.datetime.fromtimestamp(time.time())
        insert_sql = """
            INSERT INTO repo_summary
                (name, full_name, owner, last_summary_updated)
            VALUES
                ('%s', '%s', '%s', '%s')
        """ % (self.repo, self.owner_repo, self.owner, now)
        self.cur.execute(insert_sql)
        self.backlog = 0
    else:
        self.backlog = backlog


def update_repo_summary(self):
    """
    After scraping all the interesting event types, update summary of the repo.
    """
    
    self.logger.info("    Updating summary.")
    
    data = {
        'now':       datetime.datetime.fromtimestamp(time.time()),
        'full_name': self.owner_repo,
        'pushed_at': self.github_repo.pushed_at,
        'language':  self.github_repo.language
    }
    
    # when was repo created?
    if self.backlog == 0:
        update_repo = """
        UPDATE repo_summary
        SET
            created_at       = %(created_at)s,
            description      = %(description)s,
            is_fork          = %(fork)s,
            backlog_complete = 1
        WHERE
            full_name        = %(full_name)s
        """
        self.cur.execute(update_repo, self.github_repo._rawData)
    
    # start of the update query
    update_start = """
        UPDATE repo_summary
        SET
            commits = (
                SELECT count(*)
                FROM commit
                WHERE owner_repo = %(full_name)s
            ),
            forks = (
                SELECT count(*)
                FROM fork
                WHERE parent_owner_repo = %(full_name)s
            ),
            pull_requests = (
                SELECT count(*)
                FROM pull
                WHERE base_owner_repo = %(full_name)s
            ),
            issues = (
                SELECT count(*)
                FROM issue
                WHERE owner_repo = %(full_name)s
            ),
            pushed_at = %(pushed_at)s,
            language = %(language)s,
            last_commit = (
                SELECT MAX(created_at)
                FROM commit
                WHERE owner_repo = %(full_name)s
            ),
            last_fork = (
                SELECT MAX(created_at)
                FROM fork
                WHERE parent_owner_repo = %(full_name)s
            ),
            last_pull_request = (
                SELECT MAX(created_at)
                FROM pull
                WHERE base_owner_repo = %(full_name)s                
            ),
            last_summary_updated = %(now)s"""
    
    # count collaborators and contributors
    if self.conf.get('history_git', 'count_devs') == "True":
        self.logger.info("        Counting collaborators...")
        data['collaborators'] = 0
        for coll in self.github_repo.get_collaborators():
            data['collaborators'] += 1
        
        self.logger.info("        Counting contributors...")
        data['contributors'] = 0
        for contrib in self.github_repo.get_contributors():
            data['contributors'] += 1
        
        update_middle = """,
            collaborators = %(collaborators)s,
            contributors = %(contributors)s
        """
    else:
        update_middle = ""
    
    
    # save all this stuff
    update_end = """
        WHERE
            full_name = %(full_name)s
    """
    
    update = update_start + update_middle + update_end
    self.cur.execute(update, data)


def set_until(self, table, dt, owner_repo="owner_repo", until_type="NotSet"):
    """
    Determine the earliest date for a specific 'owner/repo' and hence retrieve
    events earlier than this.
    """
    
    # any existing events in the table for this repo?
    select_sql = """
        SELECT MIN(%s)
        FROM %s
        WHERE %s = '%s';
    """ % (dt, table, owner_repo, self.owner_repo)
    self.cur.execute(select_sql)
    event_until = self.cur.fetchone()[0]

    if event_until is None:
        msg = "        No records in %s table. Getting all..." % (table)
        self.logger.info(msg)
        if until_type == "NotSet":
            event_until = github.GithubObject.NotSet
        else:
            event_until = datetime.datetime.fromtimestamp(time.time()) # Now
    else:
        event_until -= datetime.timedelta(0,1)
        msg = "        Collecting %ss before %s..." % (table, event_until)
        self.logger.info(msg)
    
    return event_until


def set_since(self, table, dt, owner_repo="owner_repo", since_type="NotSet"):
    """
    Like set_until, but determines the latest data for 'owner_repo' for
    event type 'table'.
    """
    
    # any existing events in the table for this repo?
    select_sql = """
        SELECT MAX(%s)
        FROM %s
        WHERE %s = '%s';
    """ % (dt, table, owner_repo, self.owner_repo)
    self.cur.execute(select_sql)
    event_since = self.cur.fetchone()[0]

    if event_since is None:
        msg = "        No records in %s table. Getting all..." % (table)
        self.logger.info(msg)
        if since_type == "NotSet":
            event_since = github.GithubObject.NotSet
        else:
            event_since = self.github_repo.created_at
    else:
        event_since += datetime.timedelta(0,1)
        msg = "        Collecting %ss since %s..." % (table, event_since)
        self.logger.info(msg)
    
    return event_since


def get_commits(self):
    self.logger.info("    Getting commits...")
    
    if self.backlog == 1:
        since = self.set_since("commit", "committer_date")
        until = github.GithubObject.NotSet
    else:
        since = github.GithubObject.NotSet
        until = self.set_until("commit", "committer_date")
    
    self.n = 0
    self.N = 0
    
    # start processing the commits
    start_time = time.time()
    
    for cm in self.github_repo.get_commits(since=since, until=until):
        try:
            self.save_commit(cm)
        except:
            print("\nError with SHA: %s\n" % (cm._rawData['sha']))
            raise
    
    self.con.commit()
    # results
    time_taken = time.time() - start_time
    msg = "        Processed %s commits in %.2fs."\
          % (format(self.N, ",d"), time_taken)
    self.logger.info(msg)


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

    dat['committer_date']    = data['commit']['committer']['date']
    
    if self.commit_stats:
        dat['files_n']         = len(cm.files)    
        dat['stats_additions'] = cm.stats.additions
        dat['stats_deletions'] = cm.stats.deletions
        dat['stats_total']     = cm.stats.total
    
    self.insert(dat, "commit")


def get_forks(self):
    self.logger.info("    Getting forks...")
    
    if self.backlog == 1:
        since = self.set_since("fork", "created_at", "parent_owner_repo",
                               since_type="dt")
        until = None
    else:
        since = None
        until = self.set_until("fork", "created_at", "parent_owner_repo",
                               until_type="dt")
    
    self.n = 0
    self.N = 0
    
    # start processing the commits
    start_time = time.time()
    
    for fork in self.github_repo.get_forks():
        try:
            if (
                isinstance(until, datetime.datetime) and
                fork.created_at < until
               ) or (
                isinstance(since, datetime.datetime) and
                fork.created_at > since
               ):
                self.save_fork(fork)
            elif (
                  isinstance(since, datetime.datetime) and
                  fork.created_at < since
                 ):
                break
        except:
            print("\nError with fork: %i\n" % (fork._rawData['id']))
            pprint(fork._rawData)
            raise
    
    self.con.commit()
    
    # results
    time_taken = time.time() - start_time
    msg = "        Processed %i forks in %.2fs." % (self.N, time_taken)
    self.logger.info(msg)


def save_fork(self, fork):
    data = fork._rawData
    dat = {
        'parent_owner':      self.owner,
        'parent_repo':       self.repo,
        'parent_owner_repo': self.owner_repo,
        'child_owner':       data['owner']['login'],
        'child_repo':        data['name'],
        'child_owner_repo':  data['full_name'],
        'id':                data['id'],
        'created_at':        data['created_at'],
        'updated_at':        data['updated_at'],
        'pushed_at':         data['pushed_at']
    }   
    self.insert(dat, 'fork')


def get_issues(self):
    self.logger.info("    Getting issues...")
    
    if self.backlog == 1:
        since = self.set_since("issue", "created_at", since_type="ts")
        until = None
    else:
        since = None
        until = self.set_until("issue", "created_at", until_type="ts")
    
    self.n = 0
    self.N = 0
    start_time = time.time()
    self.issues_enabled = True
    
    try:
        for issue in self.github_repo.get_issues(state="all"):
            if (
                    isinstance(until, datetime.datetime) and
                    issue.created_at < until
               ) or ( 
                    isinstance(since, datetime.datetime) and
                    issue.created_at > since
               ):
                self.save_issue(issue)
    
    except github.GithubException as e:
        if e.data['message'] == "Issues are disabled for this repo":
            self.issues_enabled = False
        else:
            raise
    
    self.con.commit()
    
    # results
    time_taken = time.time() - start_time
    msg = "        Processed %i issues in %.2fs." % (self.N, time_taken)
    self.logger.info(msg)


def save_issue(self, issue):
    data = issue._rawData
    
    dat = {
        'owner': self.owner,
        'repo': self.repo,
        'owner_repo': self.owner_repo,
    }
    
    # issue level
    keys = ['id', 'number', 'state', 'created_at', 'updated_at',
            'closed_at', 'title', 'comments']
    dat.update({ k: data[k]    for k in keys })
    
    # assignee level
    try:
        dat['assignee_login'] = data['assignee']['login']
    except TypeError:
        pass
    
    # user level
    dat['user_login'] = data['user']['login']
    
    # duration of the issue
    try:
        dat['duration'] = (dat['closed_at'] - dat['created_at']).total_seconds
    except TypeError:
        pass
    
    # is the issue associated with a pull request
    if 'pull_request' in data:
        dat['pull_request'] = 0
    else:
        dat['pull_request'] = 1
    
    # try to insert this issue in to the database
    try:
        self.insert(dat, "issue")
    except:
        print(dat)
        raise

def update_open_issues(self):
    n = 0
    start_time = time.time()
    self.logger.info("    Updating open issues...")
    
    select = """
        SELECT number
        FROM issue
        WHERE owner_repo = '%s' AND state = 'open'
    """ % (self.owner_repo)
    self.cur.execute(select)
    
    update = """
        UPDATE issue
        SET
            state      = %(state)s,
            updated_at = %(updated_at)s,
            closed_at  = %(closed_at)s,
            comments   = %(comments)s
        WHERE
            owner_repo = %(owner_repo)s AND
            number     = %(number)s
    """
    
    for number in self.cur:
        n += 1
        issue = self.github_repo.get_issue(number[0])
        issue = issue._rawData
        issue['owner_repo'] = self.owner_repo
        self.cur.execute(update, issue)
   
    # results
    time_taken = time.time() - start_time
    self.logger.info("        Updated %i issues in %.2fs." % (n, time_taken))


def update_closed_issues(self):
    self.open_con()
    start_time = time.time()
    self.logger.info("Updating closed issues...")
    
    # how many closed issues need updating?
    count = """
        SELECT count(*)
        FROM issue
        WHERE state = 'closed' AND duration_s IS NULL
    """
    self.cur.execute(count)
    n = self.cur.fetchone()[0]
    
    # update the duration field
    update_duration = """
        UPDATE issue
        SET duration_s = TIMESTAMPDIFF(SECOND, created_at, closed_at)
        WHERE state = 'closed' AND duration_s IS NULL
    """
    self.cur.execute(update_duration)
    
    # results
    time_taken = time.time() - start_time
    self.logger.info("    Updated %i issues in %.2fs." % (n, time_taken))
    self.close_con()


def get_pulls(self):
    self.logger.info("    Getting pulls...")
    
    if self.backlog == 1:
        since = self.set_since("pull", "created_at", "base_owner_repo",
                               since_type="ts")
        until = None
    else:
        since = None
        until = self.set_until("pull", "created_at", "base_owner_repo",
                               until_type="ts")
    
    self.n = 0
    self.N = 0
    
    # start processing the commits
    start_time = time.time()
    
    for pull in self.github_repo.get_pulls(state="all"):
        try:
            if (
                    isinstance(until, datetime.datetime) and
                    pull.created_at < until
               ) or ( 
                    isinstance(since, datetime.datetime) and
                    pull.created_at > since
               ):
                self.save_pull(pull)
        except:
            print("\nError with Pull ID: %i\n" % (pull._rawData['id']))
            print("Here's the pull object:")
            pretty(pull._rawData)
            raise
    
    self.con.commit()
    
    # results
    time_taken = time.time() - start_time
    msg = "        Processed %i pulls in %.2fs." % (self.N, time_taken)
    self.logger.info(msg)


def save_pull(self, pull):
    data = pull._rawData
    dat = {}
    
    # pull level
    keys = ['id', 'number', 'state', 'title', 'body', 'created_at',
            'updated_at', 'closed_at', 'merged_at', 'merge_commit_sha']
    dat.update({ k: data[k] for k in keys })
        
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
    dat.update({ 'head_' + k: data['head'][k] for k in keys })
    
    try:
        dat['head_owner'] = data['head']['user']['login']
    except TypeError:
        pass
    
    # head repo level
    try:
        keys = ['fork', 'created_at', 'updated_at', 'pushed_at']
        dat.update({ 'head_' + k: data['head']['repo'][k] for k in keys })
        
        dat['head_repo'] = data['head']['repo']['name']
        dat['head_owner_repo'] = data['head']['repo']['full_name']
    except TypeError:
        pass
    
    # base level
    keys = ['label', 'ref', 'sha']
    dat.update({ 'base_' + k: data['base'][k] for k in keys })
    dat['base_owner'] = data['base']['user']['login']
    dat['base_repo'] = data['base']['repo']['name']
    dat['base_owner_repo'] = data['base']['repo']['full_name']
    
    self.insert(dat, "pull")


def update_open_pulls(self):
    n = 0
    start_time = time.time()
    self.logger.info("    Updating open pulls...")
    
    update = """
        UPDATE pull
        SET
            state      = %(state)s,
            updated_at = %(updated_at)s,
            closed_at  = %(closed_at)s,
            merged_at  = %(merged_at)s,
            comments   = %(comments)s
        WHERE
            base_owner_repo = %(base_owner_repo)s
            AND
            number     = %(number)s
    """
    
    select = """
        SELECT number
        FROM pull
        WHERE base_owner_repo = '%s' AND state = 'open'
    """ % (self.owner_repo)
    self.cur.execute(select)
    
    for number in self.cur:
        n += 1
        pull = self.github_repo.get_pull(number[0])
        pull = pull._rawData
        pull['base_owner_repo'] = self.owner_repo
        self.cur.execute(update, pull)
    
    # results
    time_taken = time.time() - start_time
    self.logger.info("        Updated %i pulls in %.2fs." % (n, time_taken))


def update_closed_pulls(self):
    self.open_con()
    start_time = time.time()
    self.logger.info("Updating closed pulls...")
    
    # how many closed pulls need updating?
    count = """
        SELECT count(*)
        FROM pull
        WHERE state = 'closed' AND duration_s IS NULL
    """
    self.cur.execute(count)
    n = self.cur.fetchone()[0]
    
    # update the duration field
    update_duration = """
        UPDATE pull
        SET duration_s = TIMESTAMPDIFF(SECOND, created_at, closed_at)
        WHERE state = 'closed' AND duration_s IS NULL
    """
    self.cur.execute(update_duration)
    
    # results
    time_taken = time.time() - start_time
    self.logger.info("    Updated %i pulls in %.2fs." % (n, time_taken))
    self.close_con()
