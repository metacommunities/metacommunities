import datetime
import github
import requests
import textwrap
import time
import urllib
import user_prompt

def get_repo_names(self):
    if self.update_repo_names:
        question = textwrap.dedent("""
            Should I collect names of new repos? If this is
            the first time it will take at least 5 days.""")
        ans = user_prompt.query_yes_no(question)
        if ans == True:
            while True:
                try:
                    self.populate_repo()
                    break
                except urllib.error.URLError as e:
                    self.logger.error(e.reason)
                    self.logger.info("Sleep for 10 minutes.")
                    time.sleep(600) # 10 mins
                    self.logger.info("Trying again.")
                    pass

def populate_repo(self):
    """
    See if there are new repos to add to the database. Only basic details are
    added; id, owner, name, description, is it a fork.
    """
    
    self.logger.info("    Populating repo table...")
    
    # get connection
    self.open_con()
    self.logger.info("        Opened database connection.")
    
    # 'since' SQL
    select_sql = """
        SELECT max(id)
        FROM repo_list;
    """
    # start collecting repos
    while True:
        self.cur.execute(select_sql)
        since = self.cur.fetchone()[0]

        if since is None:
            since = github.GithubObject.NotSet
            msg = "        No records in repo table. Getting all..."
            self.logger.info(msg)
        else:
            msg = "        Collecting repos with ID greater than %i..."\
                  % (since)
            self.logger.info(msg)
        
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
        msg = "        Processed %i repos in %.2fs." % (self.N, time_taken)
        self.logger.info(msg)

        # if tried to get repos and N is still 0, then there were no repos to
        # get so break the while loop, otherwise we should "restart" the for
        # loop
        if self.N == 0:
            break
    
    # goodbye
    self.close_con()
    self.logger.info("        Closed database connection.")


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
        self.logger.warning("                Repo without an owner.")
        pass

    # stats last checked
    dat['last_updated'] = datetime.datetime.fromtimestamp(time.time()) # Now
    
    self.insert(dat, "repo_list")
