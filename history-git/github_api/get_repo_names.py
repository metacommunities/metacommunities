import datetime
import github
import requests
import sys
import textwrap
import time
import urllib

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
        sys.stdout.write("\n")
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

def get_repo_names(self):
  if self.update_repo_names:
    question = textwrap.dedent("""
      Should I collect names of new repos? If this is
      the first time it will take at least 5 days.""")
    ans = query_yes_no(question)
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
  
  self.logger.info("  Populating repo table...")
  
  # get connection
  self.open_con()
  self.logger.info("    Opened database connection.")
  
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
      self.logger.info("    No records in repo table. Getting all...")
    else:
      self.logger.info("    Collecting repos with ID greater than %i..." % (since))
    
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
    self.logger.info("    Processed %i repos in %.2fs." % (self.N, time_taken))

    # if tried to get repos and N is still 0, then there were no repos to get
    # so break the while loop, otherwise we should "restart" the for loop
    if self.N == 0:
      break
  
  # goodbye
  self.close_con()
  self.logger.info("    Closed database connection.")


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
    self.logger.warning("        Repo without an owner.")
    pass

  # stats last checked
  dat['last_updated'] = datetime.datetime.fromtimestamp(time.time()) # Now
  
  self.insert(dat, "repo_list")
