"""
Functions to test ease and speed of search, retrieval
from githubarchive on Google BigQuery.

to get datasets we have access to
https://www.googleapis.com/bigquery/v2/projects/metacommunities/datasets
the root url is:    https://www.googleapis.com/bigquery/v2

NB: got these examples from https://developers.google.com/bigquery/docs/hello_bigquery_api

Sample query:
SELECT repository_name,
    /* Extracts the relevant emoticon from the GitHub commit message    */
    REGEXP_EXTRACT(payload_commit_msg, r'([\;:]-[\)\(])') AS emoticon,
    COUNT(*) AS emoticon_count
FROM [publicdata:samples.github_timeline]
    /* Matches the following emoticons :-),;-),:-(,;-(    */
    WHERE REGEXP_MATCH(payload_commit_msg, r'[\;:]-[\)\(]')
    /* Group by repository name and emoticon */
GROUP BY
    repository_name, emoticon
ORDER BY
    emoticon_count DESC
LIMIT 5;

Another sample query
---------------------------------
select actor, repository_language, count(repository_language) as pushes
from [githubarchive:github.timeline]
where type='PushEvent'
        and repository_language != ''
        and PARSE_UTC_USEC(created_at) >= PARSE_UTC_USEC('2012-01-01 00:00:00')
        and PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2013-01-01 00:00:00')
group by actor, repository_language;

Another one
--------------------------------
        query_data = {'query':
                'SELECT TOP( title, 10) as title, 
                COUNT(*) as revision_count FROM [publicdata:samples.wikipedia] 
                WHERE wp_namespace = 0;'}

"""


import httplib2
import pprint
import time
import pandas as pn
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

PROJECT_NUMBER = '237471208995'
PROJECT_ID = 'metacommunities'
SERVICE_ACCOUNT_EMAIL = 'rian39@gmail.com'

#not actually using these, but keeping them in case
api_key_file = file('google_api_key.txt')
api_key = api_key_file.read()
api_key_file.close()

#authorization is handled by this; you need one of these to get script to work
FLOW = flow_from_clientsecrets('client_secrets.json',
                 scope='https://www.googleapis.com/auth/bigquery')

#a sample query to use for testing
QUERY_DATA = {'query': """select actor, repository_language, 
                            count(repository_language) 
                            as pushes
                            from [githubarchive:github.timeline]
                            where type='PushEvent'
                            and repository_language != ''
                            and PARSE_UTC_USEC(created_at) >= PARSE_UTC_USEC('2012-01-01 00:00:00')
                            and PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2013-01-01 00:00:00')
                            group by actor, repository_language;"""}


def setup_bigquery():

    """
    Does the authorization and returns a service object;
    Assumes that you have sorted out the oauth2 stuff and 
    stored the keys in local file 'client_secrets.json'
    """

    storage = Storage('bigquery_credentials.dat')
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run(FLOW, storage)

    http = httplib2.Http()
    http = credentials.authorize(http)

    bigquery_service = build('bigquery', 'v2', http=http)
    return bigquery_service

def query_table(query, timeout=1.0):

    """ Returns the results of query on the githubarchive
    args:
    ----------------
    query: a BigQuery SQL query

    returns:
    ---------------------------
    results_df: a pandas.DataFrame of the results
    """
    
    try:
        bigquery_service = setup_bigquery()
        job_collection = bigquery_service.jobs()
        query_reply = job_collection.query(projectId=PROJECT_NUMBER,
                                     body=query).execute()

        # query_reply = query_request.query(projectId=PROJECT_NUMBER,
                                             # body=query).execute()
        jobReference = query_reply['jobReference']

        while (not query_reply['jobComplete']):
            print 'Job not yet complete...'
            query_reply = job_collection.getQueryResults(
                              projectId=jobReference['projectId'],
                              jobId=jobReference['jobId'],
                              timeoutMs=timeout).execute()
    
        results_df = pn.DataFrame()

        if('rows' in query_reply):
            print 'has a rows attribute'
            # printTableData(query_reply, 0)
            currentrow = len(query_reply['rows'])
            first_page_df = convert_results_to_dataframe(query_reply)
            results_df = pn.concat([results_df, first_page_df])
            print currentrow, 'of  ', query_reply['totalRows'], results_df.shape


        # Loop through each page of data
        while('rows' in query_reply and currentrow < query_reply['totalRows']):
            query_reply = job_collection.getQueryResults(
                             projectId=jobReference['projectId'],
                             jobId=jobReference['jobId'],
                             startIndex=currentrow).execute()
            if('rows' in query_reply):
                next_page_df = convert_results_to_dataframe(query_reply)
                results_df = pn.concat([results_df, next_page_df])            
                currentrow += len(query_reply['rows'])
                print 'getting more  data ', currentrow, results_df.shape


        return results_df
    except HttpError as err:
        print 'Error:', pprint.pprint(err.content)
    except AccessTokenRefreshError:
        print ("Credentials have been revoked or expired,"
            "please re-run the application to re-authorize")   

def convert_results_to_dataframe(query_response):

    """ Returns pn.DataFrame from query results 
    -----
    query_response: the object returned by bigquery_service
    """

    rows = [r['f'] for r in query_response['rows']]
    frames = []
    for arow in rows:
        frames.append([field['v'] for field in arow])
    results_df = pn.DataFrame(data=frames, 
        columns = ['actor', 'language', 'count'])
    return results_df

    