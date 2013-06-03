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

CREATE TABLE  `git`.`commits` (
`date` TEXT NOT NULL ,
`repository` TEXT COLLATE utf8_bin NOT NULL,
 `name` TEXT COLLATE utf8_bin NOT NULL ,
 `message` TEXT COLLATE utf8_bin NOT NULL ,
 `sha`  TEXT COLLATE utf8_bin NOT NULL );
'''

import MySQLdb
from pandas.io import sql
import github_api_data as gad

USER_FILE = open('github_api_user.txt')
USER = USER_FILE.readline().rstrip('\n')
PASSWORD = USER_FILE.readline().rstrip('\n')
USER_FILE.close()
DB = 'git_test'

def save_repos(limit = 1000):
    
    """ fetches up to the limit repos using the github api 
    and stores all returned fields
    in the database (currently mysql)

    Parameters
    ------------------------------
    limit: how many repositories to fetch and save
    """

    repos_df = gad.get_repos(limit)
    try: 
        con = MySQLdb.connect("localhost", 
            USER, PASSWORD, DB, charset='utf8')
        sql.write_frame(
            repos_df[['id', 'name', 'private', 'full_name', 'description', 'fork']],  
            con=con,  name='repos',  
            if_exists='append',  flavor='mysql')
    except MySQLdb.MySQLError, sql_ex:
        print sql_ex
    finally:
        con.close()
    return repos_df

def read_repositories():

    """ Returns DataFrame of all repositories
    """

    try:
        con = MySQLdb.connect("localhost", 
            USER, PASSWORD, DB, charset='utf8')
        query = "select * from repos"
        repos_df = sql.read_frame(query, con)
    except MySQLdb.MySQLError, sql_ex:
        print sql_ex
    finally:
        con.close()
    return repos_df


def save_repo_commits(repository, limit  = 1000):

    """Gets all the commits for a given repository and saves to
    database. 

    Parameters
    --------------------------------------
    repository:  should be in the form: torvalds/linux
    limit: how many commits to fetch and save
    """

    df_temp = gad.get_repository_commits(repository, limit)
    try:
        con = MySQLdb.connect("localhost", 
            USER, PASSWORD, DB, charset='utf8')
        sql.write_frame(
                df_temp,  
                con=con,  name='commits',  
                if_exists='append',  flavor='mysql')   
    except MySQLdb.MySQLError, sql_ex:
        print sql_ex
    finally:
        con.close()


       
def read_repo_commits(repository):

    """ Returns DataFrame of all commits in the database
    for that repository
    """

    try:
        con = MySQLdb.connect("localhost", 
            USER, PASSWORD, DB, charset='utf8')
        query = "select * from commits where repository='%s'" % repository
        commits_df = sql.read_frame(query, con).unique()
    except MySQLdb.MySQLError, sql_ex:
        print sql_ex
    finally:
        con.close()
    return commits_df




