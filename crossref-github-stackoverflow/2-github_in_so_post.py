"""
Extract Github URLs from the bodies of a stackoverflow (SO) post (question or
answer) and record the associated question tags

This is one way of bridging the gap between GH and SO.

We're going text mining!

find all URLs in a body of text:
http://stackoverflow.com/a/6513840/1004740


logic:
1) take text from a post
2) search for a URL to a github repo in the body text
3) if we get a hit then
4)   take the tags from post (or the parent question if the post is an answer)
5)   pair off the tags with the repo name
7) go to (2) and see if there is another URL in the body
"""

import MySQLdb
import re
import sys

hst = 'localhost'
usr = 'so_import'
pwd = 'fancyTea'
db  = 'so'
chrst = 'utf8'



# functions

def process(pid, post):
  # find github URL(s)
  pattern = r'http[s]?://(www\.)?github.com/([\S]*/[\S]*)'
  regex = re.compile(pattern, re.IGNORECASE)
  for match in regex.finditer(body):
      repo_url = match.group(2) # group=2, second brackets i.e. "owner/repo"
      save_url_with_tags(pid, repo_url)

def save_url_with_tags(pid, url):
  # 2nd connection to MySQL
  con_tag = MySQLdb.connect(host=hst, user=usr, passwd=pwd, db=db, charset=chrst)
  cur_tag = con_tag.cursor()
  
  # get tags
  tag_sql = """
    SELECT tag.tag
    FROM posttag, tag
    WHERE posttag.pid = %s AND tag.id = posttag.tid;
  """
  cur_tag.execute(tag_sql, (pid))
  tags = cur_tag.fetchall()
  
  # pair-off the tags with the url
  pair_sql = """
    INSERT INTO url_tag (pid, url, tag)
    VALUES (%s, %s, %s);
  """
  
  for tag in tags:
    cur_tag.execute(pair_sql, (pid, url, tag[0]))
  
  sys.stdout.write('.')
  sys.stdout.flush()
  # goodbye mysql
  cur_tag.close()
  con_tag.commit()
  con_tag.close()



## main

# connection for aquiring post body
con_post = MySQLdb.connect(host=hst, user=usr, passwd=pwd, db=db, charset=chrst)
cur_post = con_post.cursor(MySQLdb.cursors.SSCursor) # NOT fetch all

# create the table for the URL-tag pairs 
url_tag_sql = """
  CREATE TABLE IF NOT EXISTS url_tag (
    pid  INTEGER,
    url  TINYTEXT,
    tag  TINYTEXT
  );
"""

cur_post.execute(url_tag_sql)

# start fetching the body text
cur_post.execute("SELECT id, body FROM post;")

for pid, body in cur_post:
  process(pid, body)

sys.stdout.write('\n')
sys.stdout.flush()

