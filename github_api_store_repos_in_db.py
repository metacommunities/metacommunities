''' This is for making the 'repos' table for the data to go in
CREATE TABLE  `git`.`repos` (
`id` INT( 11 ) NOT NULL ,
 `name` TEXT COLLATE utf8_bin NOT NULL ,
 `full_name` TEXT COLLATE utf8_bin NOT NULL ,
 `private` TINYINT( 1 ) NOT NULL ,
 `description` TEXT COLLATE utf8_bin NOT NULL ,
 `fork` TINYINT( 1 ) NOT NULL ,
PRIMARY KEY (  `id` )
) ENGINE = INNODB DEFAULT CHARSET = utf8 COLLATE = utf8_bin
'''

import requests
import pandas as pn
import time
import MySQLdb
from pandas.io import sql
import github_api_data as gha

USER_FILE = open('github_api_user.txt')
USER = USER_FILE.readline().rstrip('\n')
PASSWORD = USER_FILE.readline().rstrip('\n')
USER_FILE.close()



def save_repos(limit=1000000):
    """ to get list of repos .... 
    the count is the number of requests to the API. Each request returns 100 repos
    to 'resume' this after already adding records to table, 
    add ?since=x where x is the last ID in your table.
    I'm only saving 6 variables right now because most of the variables returned 
    are URLs that follow a set structure and therefore could be easily built from the full_name'
    """

    con = MySQLdb.connect("localhost", USER, PASSWORD, "git", charset='utf8')
    df_temp = gha.get_repos(limit)
    sql.write_frame(
        df_temp[['id', 'name', 'private', 'full_name', 'description', 'fork']],  
        con=con,  name='repos',  
        if_exists='append',  flavor='mysql')
    return df_temp

def save_repos_commits( ):

    """gets all the commits for a given repository and saves to
    database"""
    return

       





