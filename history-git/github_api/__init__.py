import ConfigParser
import github
import logging
import MySQLdb
import os
import warnings

# supress MySQL Warnings
warnings.filterwarnings('ignore', category=MySQLdb.Warning)

class HistoryGitException(Exception):
  """
  custom exception for History Git, so I can raise my own errors
  """
  pass


def create_logger(hg_path):
  """
  create logger which prints timestamp along with message out to log
  file and the screen.
  """
  log_file = os.path.join(hg_path, 'history_git.log')
  logger = logging.getLogger('history_git')
  logger.setLevel(logging.INFO)
  
  # create file handler which logs even debug messages
  fh = logging.FileHandler(log_file)
  fh.setLevel(logging.INFO)
  
  # create console handler with a higher log level
  ch = logging.StreamHandler()
  ch.setLevel(logging.INFO)
  
  # create formatter and add it to the handlers
  formatter = logging.Formatter('%(asctime)s  %(levelname)s  %(message)s',
                                '%Y-%m-%d %H:%M:%S')
  fh.setFormatter(formatter)
  ch.setFormatter(formatter)
  
  # add the handlers to the logger
  logger.addHandler(fh)
  logger.addHandler(ch)
  
  return logger


class HistoryGit():
  """
  History Git is this really grumpy guy who knows exactly how to get all the
  events for a given repo. Just pass him the 'owner/repo' string using .get()
  and he'll get to work, begrudingly.
  """
  from db import open_con, close_con, create_db, insert
  
  from get_repo_names import get_repo_names, populate_repo, save_repo
  
  from get_activity import get, set_until, get_commits, save_commit,\
                             get_forks, save_fork, get_issues, save_issue,\
                             get_pulls, save_pull
  
  from upload_activity import upload_wide_activity
  
  def __init__(self, path, drop_db=False):
    self.logger = logging.getLogger('history_git')
    
    # load settings
    self.conf = ConfigParser.ConfigParser()
    self.conf.read(os.path.join(path, 'settings.conf'))
    
    # history git settings
    self.commit_stats = self.conf.get('history_git', 'commit_stats')
    self.update_repo_names = self.conf.get('history_git', 'get_repo_names')
    
    # tables!
    self.create_db(drop_db)
    
    # github
    self.gh = github.Github(login_or_token = self.conf.get('github', 'user'),
                            password = self.conf.get('github', 'passwd'))

