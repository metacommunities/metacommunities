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
4)     take the tags from post (or the parent question if the post is an answer)
5)     pair off the tags with the repo name
7) go to (2) and see if there is another URL in the body
"""

import argparse
import MySQLdb
import re
import sys

def process(pid, post):
    # find github URL(s)
    # \w        word character: [A-Za-z0-9_]
    # \d        digit: [0-9]
    pattern = r'http[s]?://(www\.)?github.com/([\w\d-]*/[\w\d-]*)'
    regex = re.compile(pattern, re.IGNORECASE)
    
    # make sure URLs are unique
    # group=0, all of the URL i.e. "http://..."
    # group=2, second brackets i.e. "owner/repo"
    if post is not None:
        urls = [ match.group(2) for match in regex.finditer(post) ]
        urls = list(set(urls))
        
        # for each github url in the post, do the following:
        for url in urls:
                tags = get_tags(pid)
                save_url_with_tags(pid, url, tags)
                con_tag.commit()

def get_tags(pid):
    """
    Get tags for the post (or for the parent Question post if post is an answer)
    """
    
    # determine if post is a question or an answer by grabbing the ParentID for
    # the post. NULL if post is THE parent.
    
    cur_tag.execute("SELECT parentid FROM posts WHERE id = %s;", pid)
    
    parent = cur_tag.fetchone()[0]
    
    if parent:
        pid = parent
    
    # get tags
    tag_sql = """
        SELECT tags.tag
        FROM posttags, tags
        WHERE posttags.pid = %s AND tags.id = posttags.tid;
    """
    cur_tag.execute(tag_sql, (pid))
    tags = cur_tag.fetchall()
    
    return tags


def save_url_with_tags(pid, url, tags):
    # pair-off the tags with the url
    
    pair_sql = """
        INSERT INTO url_tag (pid, url, tag)
        VALUES (%s, %s, %s);
    """
    
    for tag in tags:
        cur_tag.execute(pair_sql, (pid, url, tag[0]))
    
    # one dot is one post that contained at least one github URL
    sys.stdout.write('.')
    sys.stdout.flush()


def main(user, passwd, host, db, charset):
    # connections
    global con_tag
    global cur_tag
    con_tag = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db,
                              charset=charset)
    cur_tag = con_tag.cursor()

    con_post = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db,
                               charset=charset)
    cur_post = con_post.cursor(MySQLdb.cursors.SSCursor) # NOT fetch all

    # create the table for the URL-tag pairs 
    url_tag_sql = """
        CREATE TABLE IF NOT EXISTS url_tag (
            pid    INTEGER,
            url    TINYTEXT,
            tag    TINYTEXT
        );
    """

    cur_post.execute(url_tag_sql)

    # start fetching the body text
    cur_post.execute("SELECT id, body FROM posts;")

    for pid, body in cur_post:
        process(pid, body)

    sys.stdout.write('\n')
    sys.stdout.flush()

    # goodby mysql
    cur_post.close()
    con_post.close()

    cur_tag.close()
    con_tag.close()

if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--user')
        parser.add_argument('-p', '--passwd')
        parser.add_argument('-l', '--host', default='localhost')
        parser.add_argument('-d', '--db', default='so')
        parser.add_argument('-c', '--charset', default='utf8')
        args = parser.parse_args()
        main(args.user, args.passwd, args.host, args.db, args.charset)

