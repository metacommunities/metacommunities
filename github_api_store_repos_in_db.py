
""" Store and retrieve functions for github data.
Configuration data, such as user and password  for
databases needs to be in a local text file.

Configuration
----------------------------------
The name of the database to use is held in the 
global variabel DB_NAME
 """

import MySQLdb
from pandas.io import sql
import github_api_data as gad


USER_FILE = open('github_api_user.txt')
USER = USER_FILE.readline().rstrip('\n')
PASSWORD = USER_FILE.readline().rstrip('\n')
USER_FILE.close()
DB_NAME = 'git_test'


SQL_TABLES = {
'repos':
"""CREATE TABLE  IF NOT EXISTS `repos` (
`id` INT( 11 ) NOT NULL ,
 `name` TEXT COLLATE utf8_bin NOT NULL ,
 `full_name` TEXT COLLATE utf8_bin NOT NULL ,
 `private` TINYINT( 1 ) NOT NULL ,
 `description` TEXT COLLATE utf8_bin NOT NULL ,
 `fork` TINYINT( 1 ) NOT NULL ,
PRIMARY KEY (  `id` )
) ENGINE = INNODB DEFAULT CHARSET = utf8 COLLATE = utf8_bin;""",

'commits': 
"""CREATE TABLE  IF NOT EXISTS  `commits` (
`date` TEXT NOT NULL ,
`repository` TEXT COLLATE utf8_bin NOT NULL,
 `name` TEXT COLLATE utf8_bin NOT NULL ,
 `message` TEXT COLLATE utf8_bin NOT NULL ,
 `sha`  TEXT COLLATE utf8_bin NOT NULL );
"""}



def db_setup(db_name = DB_NAME):

    """ checks if database exists, creates it if not;
    Also constructs tables because pandas.sql 
    seems bad at doing this

    Parameters
    -----------------------------
    db_name: name of database to check and setup 
    """

    try:
        
        #connect to DB_NAME if it exists
        query = 'CREATE DATABASE IF NOT EXISTS %s;' % db_name
        con =  MySQLdb.connect("localhost", 
            USER, PASSWORD, db_name, charset='utf8')
        cursor = con.cursor()
        cursor.execute(query)

        #check if tables exist
        for table in SQL_TABLES:
            
            # if table doesn't exist, creat it
            print 'creating table %s'  % table 
            query = SQL_TABLES[table]
            cursor.execute(query)
        con.close()
    except MySQLdb.MySQLError, sql_ex:
        print sql_ex
        return False
    finally:
        print 'database set up complete'
    return True

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
            USER, PASSWORD, DB_NAME, charset='utf8')
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
            USER, PASSWORD, DB_NAME, charset='utf8')
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
            USER, PASSWORD, DB_NAME, charset='utf8')
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
            USER, PASSWORD, DB_NAME, charset='utf8')
        query = "select * from commits where repository='%s'" % repository
        commits_df = sql.read_frame(query, con)
    except MySQLdb.MySQLError, sql_ex:
        print sql_ex
    finally:
        con.close()
    return commits_df




