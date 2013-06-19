"""
Functions that generate dataframes from  the github api.

Authentication with the github api increases the amount of 
data that can be retrieved. 
I've set up a github user id that we can use for api calls. 
In any case, user/pwd needs to be in a  2-line 'github_api_user.txt' plain text file.
e.g:
    torvalds
    secretpassword 
The user/pwd are always read in when the module loads.

"""

import requests
import time
import pandas as pd
import json

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
    repos_df = pd.DataFrame()
    url_next = ''
    current_count = 0
    while current_count < limit:
        req = requests.get(url, auth=(USER, PASSWORD))
        if(req.ok):
            repoItem = req.json
            repos_df = repos_df.append(pd.DataFrame.from_dict(repoItem))
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

    df_lang = pd.DataFrame()

    for name, url in repos_df.languages_url.iteritems():
        print 'fetching repository %s from %s'% (name, url)
        req = requests.get(url, auth=(USER, PASSWORD))
        lang = req.json
        df_temp = pd.DataFrame.from_dict({name:lang}, 'index')
        df_lang = df_lang.append(df_temp)

    df_lang = df_lang.fillna(0)
    return df_lang

def get_repository_commits(repository, since = '2008-01-01', until = '',  limit = 500, sleep_time=1.0):

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

    commit_df = pd.DataFrame()
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
            commit_temp  = pd.DataFrame(data_dict, index = sha)
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

def get_repository_event(user, repo, limit=1000):
    """Returns a list of events as dictionaries
    from the API using url of the form
    https://api.github.com/repos/torvalds/linux/events
    Arguments
    ----------------------------------
    user: name of repo owner
    repo: name of repository
    limit: number of events to fetch
    """

    base_url = 'https://api.github.com/repos'
    suffix = 'events'
    url = '/'.join([base_url, user, repo, suffix])
    events = []
    try:
        url_next = ''
        current_count = 0
        while current_count < limit:
            events_req = requests.get(url, auth=(USER, PASSWORD))
            events = events + events_req.json
            if events_req.links.has_key('next'):
                url_next = events_req.links['next']['url']
                print url_next
            else:
                break
            if url == url_next:
                break
            else: appapp
                url = url_next + '&per_page=100'
            current_count = len(events)
            time.sleep(1.0)

    except Exception, e:
        print e
    return events

	
	
def get_repository_forkdata(repo):
#this function returns a data frame with data on a repo's forks - it currently breaks after around 500
	url = 'https://api.github.com/repos/'+repo+'/forks'
	repos_df = pn.DataFrame()
	req = requests.get(url, auth=(USER, PASSWORD))
	repoItem = req.json
	repos_df = repos_df.append(unpack_repoItem(repoItem, repos_df))
	while req.links.has_key('next'):
		url = req.links['next']['url']
		req = requests.get(url, auth=(USER, PASSWORD))
		repoItem = req.json
		repos_df = repos_df.append(unpack_repoItem(repoItem, repos_df))  
		time.sleep(1)
        return repos_df


def unpack_repoItem(repoItem, repos_df):
	'''This does the work of extracting relevant variables from the json item and returning a data frame
	repoItem is the json item to be unpacked
	repos_df is the data frame where data from the current item will be appended
	'''	
	id = [it['id'] for it in repoItem]
	full_name = [it['full_name'] for it in repoItem]
	description = [it['description'] for it in repoItem]
	language = [it['language'] for it in repoItem]
	fork = [it['fork'] for it in repoItem]
	forks = [it['forks'] for it in repoItem]
	size = [it['size'] for it in repoItem]
	watchers = [it['watchers'] for it in repoItem]
	open_issues = [it['open_issues'] for it in repoItem]
	created_at = [it['created_at'] for it in repoItem]
	pushed_at = [it['pushed_at'] for it in repoItem]
	updated_at = [it['updated_at'] for it in repoItem]
	has_downloads = [it['has_downloads'] for it in repoItem]
	has_issues = [it['has_issues'] for it in repoItem]
	has_wiki = [it['has_wiki'] for it in repoItem]
	master_branch = [it['master_branch'] for it in repoItem]
	parent_id = repo_id
	parent_name = repo

	data_dict = {
			'id': id,
			'full_name': full_name,
			'description': description,
			'language': language,
			'fork': fork,
			'forks': forks,
			'size': size,
			'watchers': watchers,
			'open_issues': open_issues,
			'created_at': created_at,
			'pushed_at': pushed_at,
			'updated_at': updated_at,
			'has_downloads': has_downloads,
			'has_issues': has_issues,
			'has_wiki': has_wiki,
			'master_branch': master_branch,
			'parent_id': parent_id,
			'parent_name': parent_name} 

	temp_df  = pn.DataFrame(data_dict, index = id)		
	repos_df = repos_df.append(temp_df)
	return repos_df

