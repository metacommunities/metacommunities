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
import base64

# read API user/password from your local file'
USER_FILE = open('github_api_key.txt')
USER = USER_FILE.readline().rstrip('\n')
PASSWORD = USER_FILE.readline().rstrip('\n')
USER_FILE.close()

def get_repository_event(user = '', repo = '', url = '', limit=1000):
    
    """Returns a list of events as dictionaries
    from the API using url of the form
    https://api.github.com/repos/torvalds/linux/events
    Arguments
    ----------------------------------
    user: name of repo owner
    repo: name of repository
    url: full api url of repo
    limit: number of events to fetch
    """

    suffix = 'events'
    if url is not  None:
        url = '/'.join([url, suffix])
    else:
        base_url = 'https://api.github.com/repos'
        url = '/'.join([base_url, user, repo, suffix])
    events = []
    try:
        url_next = ''
        current_count = 0
        while current_count < limit:
            events_req = requests.get(url, auth=(USER, PASSWORD))
            events = events + events_req.json()
            if events_req.links.has_key('next'):
                url_next = events_req.links['next']['url']
                print url_next
            else:
                break
            if url == url_next:
                break
            else:
                url = url_next + '&per_page=100'
            current_count = len(events)
            time.sleep(0.72)

    except Exception, e:
        print e
    return events

    
def unpack_repoItem(repoItem, repos_df, parent):
    '''
    This does the work of extracting relevant variables from the json item
    and returning a data frame

    Parameters
    -------------------------------------
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
    parent_id = 1
    parent_name = parent

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
            'parent_id': parent_id,
            'parent_name': parent_name} 

    temp_df  = pd.DataFrame(data_dict, index = id)      
    repos_df = repos_df.append(temp_df)
    return repos_df



    
def unpack_repoItem_pulls(repoItem, repos_df, parent):
    '''
    This does the work of extracting relevant variables from the json item
    and returning a data frame
    Parameters
    ------------------------------
    repoItem:the json item to be unpacked
    repos_df: the data frame where data from the current item will be appended
    '''
    id = [it['id'] for it in repoItem]
    state = [it['state'] for it in repoItem]
    title = [it['title'] for it in repoItem]
    body = [it['body'] for it in repoItem]
    number = [it['number'] for it in repoItem]
    merged_at = [it['merged_at'] for it in repoItem]
    closed_at = [it['closed_at'] for it in repoItem]
    created_at = [it['created_at'] for it in repoItem]
    head_created_at = [it['head']['repo']['created_at'] for it in repoItem]
    head_full_name = [it['head']['repo']['full_name'] for it in repoItem]
    head_fork = [it['head']['repo']['fork'] for it in repoItem]
    head_forks = [it['head']['repo']['forks'] for it in repoItem]
    base_full_name = [it['base']['repo']['full_name'] for it in repoItem]
    pull_user = [it['user']['login'] for it in repoItem]
    data_dict = {
            'id': id,
            'state': state,
            'title': title,
            'body': body,
            'number': number,
            'merged_at': merged_at,
            'closed_at': closed_at,
            'created_at': created_at,
            'head_created_at': head_created_at,
            'head_full_name': head_full_name,
            'head_fork': head_fork,
            'head_forks': head_forks,
            'base_full_name': base_full_name,
            'pull_user': pull_user} 

    temp_df  = pd.DataFrame(data_dict, index = id)      
    repos_df = repos_df.append(temp_df)
    return repos_df

