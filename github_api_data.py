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
PASSWORD = USER_FILE.readline().rstrip('\n')
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
    while current_count < limit:
        req = requests.get(url, auth=(USER, PASSWORD))
        if(req.ok):
            repoItem = req.json
            repos_df = repos_df.append(pn.DataFrame.from_dict(repoItem))
            current_count = len(repos_df)
            print 'fetched ', current_count, 'rows'
        time.sleep(sleep_time)
        repos_df = repos_df.fillna('')

        # check if any more commits to fetch
        if req.links.has_key('next'):
            url_next = req.links['next']['url']
        else:
            break
            
        if url == url_next:
            break
        else:
            url = url_next

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

def get_repository_commits(repository, since = '2008-01-01', 
    until = '',  limit = 500, sleep_time=1.0):

    """Returns a dataframe of all the commit events in the repository.
    We assume that github starts 1 Jan 2008, and that there is no 
    data before then. 

    Parameters
    -----------------------------------------
    repository: should be in the form 'torvalds/linux'
    since: the starting date for commits
    until: the end date for commits
    limit: max number of commits to fetch
    """

    base_url = 'https://api.github.com/repos/'
    suffix = '/commits'
    url = base_url + repository + suffix + '?&since=' + since

    # add time range 
    if until != '':
        url = url + '&until=' + until

    commit_df = pn.DataFrame()
    url_next = ''
    current_count = 0
    while current_count < limit:
        req = requests.get(url, auth=(USER, PASSWORD))
        if(req.ok):
            repoItem = req.json
            #may need to get more fields from json object
            commits = [it['commit'] for it in repoItem]
            date = [it['author']['date'] for it in commits]
            name = [it['author']['name'] for it in commits]
            message = [it['message'] for it in commits]
            sha = [it['sha'] for it in repoItem]
            data_dict = {
                    'repository': repository,
                    'date': date,
                    'name': name,
                    'message': message,
                    'sha': sha} 
            commit_temp  = pn.DataFrame(data_dict, index = sha)
            commit_df = commit_df.append(commit_temp)
            current_count = len(commit_df)
            print 'fetched ', current_count, 'rows from ', url
        time.sleep(sleep_time)
        
        # check if any more commits to fetch
        if req.links.has_key('next'):
            url_next = req.links['next']['url']
        else:
            break
        if url == url_next:
            break
        else:
            url = url_next
    return commit_df    


