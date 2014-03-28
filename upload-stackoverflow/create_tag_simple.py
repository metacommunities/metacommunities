#!/usr/bin/python

# this differs from the other tag scripts by creating a simple 'tag' table
# in which it saves the results from splitting out the tag field for a post

import argparse
import csv
import MySQLdb
import os
import re
import sys

def extract_tags(mysql_user, mysql_password, mysql_host):
    # always flush messages
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

    # connect to mysql 
    con = MySQLdb.connect(
        host=mysql_host,
        user=mysql_user,
        passwd=mysql_password,
        db="so"
    )
    cur = con.cursor()

    # create space for post tags
    sys.stdout.write(" Dropping/creating 'posttags' table.\n")
    cur.execute('DROP TABLE IF EXISTS posttags;')
    create_posttag = """
        CREATE TABLE posttags (
            pid                 INTEGER,
            tag                 TINYTEXT,
            tid                 INTEGER,
            post_creation_date  DATETIME
        )
        CHARACTER SET utf8
        COLLATE utf8_general_ci
        ENGINE = InnoDB;
    """
    cur.execute(create_posttag)

    insert = """INSERT INTO posttags (pid, tag) VALUES (%s, %s);"""

    sys.stdout.write(" Prepping")
    # get n so we can monitor progress
    cur.execute('SELECT count(*) FROM posts WHERE postTypeId = 1;')
    n = cur.fetchone()
    n = n[0]
    sys.stdout.write(" .")

    # grab post id and tag field from the Posts table
    cur.execute('SELECT id, tags FROM posts WHERE postTypeId = 1;')
    sys.stdout.write(" .\n")

    sys.stdout.write(" There are %i posts to process.\n" % (n))

    # begin processing the tags
    posttags = []
    i = 1

    for pid, ptag in cur.fetchall():
        if ptag:
            # seperate the tags out
            ptag = re.split('[<>]', ptag)
            ptag = filter(None, ptag)
            ptag = list(set(ptag))
            
            for pt in ptag:
                cur.execute(insert, (pid, pt))
            
            # print progress
            msg = i / float(n) * 100
            msg = "{:5.1f}".format(msg)
            msg = " Processing tags: " + msg + "%"
            sys.stdout.write(msg + "\r")
            i += 1

    sys.stdout.write(msg + "\n")
    con.commit()

    sys.stdout.write("Building indexes on 'posttags' table.")
    cur.execute("ALTER TABLE posttags ADD INDEX (pid);")

    sys.stdout.write("Creating 'tags' summary table.")

    cur.execute("DROP TABLE IF EXISTS tags;")
    create_tag = """
        CREATE TABLE tags (
            SELECT tag, count(*) as count
            FROM posttags
            GROUP BY tag
            ORDER BY tag ASC
        );
    """
    cur.execute(create_tag)

    # add tag id
    sys.stdout.write("Adding tag id to 'tags' table.\n")
    tag_id = """
        ALTER TABLE tags
        ADD COLUMN id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
    """
    cur.execute(tag_id)

    sys.stdout.write("Building indexes on 'tags' table.\n")
    cur.execute("ALTER TABLE tags ADD UNIQUE INDEX (id), ADD INDEX (tag(10));")
        
    # add tag id to 'posttags'
    sys.stdout.write("Adding tag id to 'posttags' table.\n")
    posttag_tid = """
        UPDATE posttags, tags
        SET posttags.tid = tags.id
        WHERE posttags.tag = tags.tag;
    """
    cur.execute(posttag_tid)

    # add creation timestamp of post to 'posttags'
    # select every 500,000th post id
    sys.stdout.write("Adding post creation timestamp to 'posttags', this is slow.")
    cur.execute(
        """
        SELECT *
        FROM ( 
            SELECT 
                @row := @row +1 AS rownum, id
            FROM ( 
                SELECT @row :=0
            ) r, posts
        ) ranked 
        WHERE rownum % 500000 = 0
        """
    )
    post_ids = cur.fetchall()
    post_ids = [ x[1] for x in post_ids ]
    sys.stdout.write(".")

    cur.execute("SELECT max(id) FROM posts;")
    max_id = cur.fetchone()[0]
    max_id += 1
    post_ids.append(max_id)
    sys.stdout.write(".")

    update_posttags_date = """
        UPDATE posttags
        INNER JOIN posts ON posttags.pid = posts.id
        SET posttags.post_creation_date = posts.creationdate
        WHERE posttags.post_creation_date IS NULL AND posttags.pid < %s;
    """

    for pid in post_ids:
        cur.execute(update_posttags_date, (pid))
        con.commit()
        sys.stdout.write(".")
    
    sys.stdout.write("\n")
    
    # add first used timestamp and post id to 'tags'
    sys.stdout.write("Adding when the tag was first used to 'tags' table.\n")
    cur.execute("""
        ALTER TABLE tags
        ADD COLUMN first_question INTEGER,
        ADD COLUMN first_question_date DATETIME;
    """)
    
    tag_question = """
        UPDATE
            tags
        JOIN
            (
                SELECT
                    tid,
                    MIN(pid) AS first_question,
                    MIN(post_creation_date) AS first_question_date
                FROM
                    posttags
                GROUP BY
                    tid
            ) pt
        ON
            pt.tid = tags.id
        SET
            tags.first_question = pt.first_question,
            tags.first_question_date = pt.first_question_date;
            
    """
    cur.execute(tag_question)
    
    # goodbye
    con.commit()
    cur.close()
    con.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--passwd')
    parser.add_argument('-l', '--host')
    args = parser.parse_args()
    extract_tags(args.user, args.passwd, args.host)
