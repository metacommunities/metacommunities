#!/usr/bin/env python

# source http://meta.stackoverflow.com/a/28231

import argparse
import logging
import os
import sqlite3
import sys
import xml.etree.cElementTree as etree

ANATOMY = {
 'Comments': {
  'Id':'INTEGER',
  'PostId':'INTEGER',
  'Score':'INTEGER',
  'Text':'TEXT',
  'CreationDate':'DATETIME',
  'UserDisplayName':'TEXT',
  'UserId':'INTEGER'
 },
 'Posts': {
  'Id':'INTEGER', 
  'PostTypeId':'INTEGER', # 1: Question, 2: Answer
  'ParentID':'INTEGER', # (only present if PostTypeId is 2)
  'AcceptedAnswerId':'INTEGER', # (only present if PostTypeId is 1)
  'CreationDate':'DATETIME',
  'Score':'INTEGER',
  'ViewCount':'INTEGER',
  'Body':'TEXT',
  'OwnerUserId':'INTEGER', # (present only if user has not been deleted) 
  'OwnerDisplayName':'TEXT', # (present only if user has been deleted) 
  'LastEditorUserId':'INTEGER',
  'LastEditorDisplayName':'TEXT', #="Rich B" 
  'LastEditDate':'DATETIME', #="2009-03-05T22:28:34.823" 
  'LastActivityDate':'DATETIME', #="2009-03-11T12:51:01.480" 
  'CommunityOwnedDate':'DATETIME', #(present only if post is community wikied)
  'Title':'TEXT',
  'Tags':'TEXT',
  'AnswerCount':'INTEGER',
  'CommentCount':'INTEGER',
  'FavoriteCount':'INTEGER',
  'ClosedDate':'DATETIME'
 },
 'Users': {
  'Id':'INTEGER',
  'Reputation':'INTEGER',
  'CreationDate':'DATETIME',
  'DisplayName':'TEXT',
  'LastAccessDate':'DATETIME',
  'WebsiteUrl':'TEXT',
  'Location':'TEXT',
  'Age':'INTEGER',
  'AboutMe':'TEXT',
  'Views':'INTEGER',
  'UpVotes':'INTEGER',
  'DownVotes':'INTEGER',
  'EmailHash':'TEXT'
  },
 'Votes': {
  'Id':'INTEGER',
  'PostId':'INTEGER',
  'UserId':'INTEGER',
  'VoteTypeId':'INTEGER',
           # -   1: AcceptedByOriginator
           # -   2: UpMod
           # -   3: DownMod
           # -   4: Offensive
           # -   5: Favorite
           # -   6: Close
           # -   7: Reopen
           # -   8: BountyStart
           # -   9: BountyClose
           # -  10: Deletion
           # -  11: Undeletion
           # -  12: Spam
           # -  13: InformModerator
  'CreationDate':'DATETIME',
  'BountyAmount':'INTEGER'
 },
 'Badges': {
  'Id':'INTEGER',
  'UserId':'INTEGER',
  'Name':'TEXT',
  'Date':'DATETIME'
 }
}

def dump_files(anatomy, input_path, 
    dump_database_name='stack-overflow-dump.sqlite3',
    create_query='CREATE TABLE IF NOT EXISTS [{table}]({fields})',
    insert_query='INSERT INTO {table} ({columns}) VALUES ({values})',
    log_filename='so-parser.log'):
  
  logging.basicConfig(filename=log_filename,level=logging.INFO)
  db = sqlite3.connect(dump_database_name)
  
  for filename in anatomy.keys():
    print "Opening %s.xml" % (filename)
    xml_file = os.path.join(input_path, filename + '.xml')
    tree = etree.iterparse(xml_file)
    table_name = filename
    
    sql_create = create_query.format(
      table=table_name, 
      fields=", ".join(['{0} {1}'.format(name, type) for name, type in anatomy[table_name].items()]))
    print "Creating table %s" % (table_name)
    
    try:
      logging.info(sql_create)
      db.execute(sql_create)
    except Exception, e:
      logging.warning(e)
    
    i = 0
    for events, row in tree:
      try:
        logging.debug(row.attrib.keys())
        
        db.execute(insert_query.format(
           table=table_name, 
           columns=', '.join(row.attrib.keys()), 
           values=('?, ' * len(row.attrib.keys()))[:-2]),
           row.attrib.values())
        sys.stdout.write("  %s records \r" % (str(i)))
        i += 1
      except Exception, e:
        logging.warning(e)
        print "x"
      finally:
        row.clear()
    
    print i + "\n"
    db.commit()
    del(tree)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input-dir', default='stackoverflow.com')
  args = parser.parse_args()
  dump_files(ANATOMY, args.input_dir)

