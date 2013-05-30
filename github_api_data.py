"""
Functions that generate dataframes from  the github api.

Authentication with the github api increases the amount of 
data that can be retrieved. 
I've set up a github user id that we can use for api calls. 
In any case, user/pwd needs to be a 'github_api_user.txt' file. 
The user/pwd are read in when the module loads.

"""

import requests
import time
import pandas as pn

# read API user/password from your local file'
USER_FILE = open('github_api_user.txt')
USER = USER_FILE.readline().rstrip('\n')
PASSWORD = USER_FILE.readline()
USER_FILE.close()


def github_timeline():
    """Returns dictionary with recent events -- not sure how many"""
    req = requests.get('https://github.com/timeline.json')
    timeline = req.json
    return timeline

def get_repos(limit=500, sleep_time=1.0):

    """Returns a DataFrame of repositories; 
    The count is the number of requests to the API. 
    Each request returns 100 repos approximately."""

    url = 'https://api.github.com/repositories'
    repos_df = pn.DataFrame()
    url_next = ''
    current_count = 0
    while (url_next != url) and (current_count < limit):
        req = requests.get(url, auth=(USER, PASSWORD))
        url_next = req.links['next']['url']
        if(req.ok):
            repoItem = req.json
            repos_df = repos_df.append(pn.DataFrame.from_dict(repoItem))
            current_count = len(repos_df)
            print 'fetched ', current_count, 'rows'
        time.sleep(sleep_time)
        repos_df = repos_df.fillna('')
    return repos_df

def get_programming_languages(repos_df):

    """ Returns dataframe of the programming languages 
	used for repositories.

	url = 'https://github.com/search?l=Python&q=%40github&ref=searchresults&type=Repositories'

	But a more fine grained view comes from asking each repository
	what languages are being used there. 
		url = 'https://api.github.com/repos/vanpelt/jsawesome/languages'
		req = requests.get(url)
		lang = req.json
		print lang
    """

    df_lang = pn.DataFrame()

    for name, url in repos_df.languages_url.iteritems():
        print 'fetching repository %s from %s'% (name, url)
        req = requests.get(url, auth=(USER, PASSWORD))
        lang = req.json
        df_temp = pn.DataFrame.from_dict({name:lang}, 'index')
        df_lang = df_lang.append(df_temp)

    df_lang = df_lang.fillna(0)
    return df_lang

def get_repository_commits( 
    url = 'https://api.github.com/repos/torvalds/linux/commits',
    limit = 500, sleep_time=1.0):

    """Returns a dataframe of all the commit events in the repository"""

    # 'https://github.com/torvalds/linux' is the sample repos
    commit_df = pn.DataFrame()
    url_next = ''
    current_count = 0
    while (url_next != url) and (current_count < limit):
        req = requests.get(url, auth=(USER, PASSWORD))
        url_next = req.links['next']['url']
        if(req.ok):
            repoItem = req.json
            commits = [it['commit'] for it in repoItem]
            commit_df = commit_df.append(commits)
            current_count = len(commit_df)
            print 'fetched ', current_count, 'rows from ', url
        time.sleep(sleep_time)
    return commit_df    
