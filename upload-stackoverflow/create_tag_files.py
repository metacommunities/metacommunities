#!/usr/bin/python

import argparse
import csv
import MySQLdb
import os
import pandas as pd
import re
import sys

def concatenate_tags(mysql_user, mysql_password, mysql_host):

  # always flush messages
  sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

  # create two CSV files; 'tag.csv' and 'posttag.csv' from the data in the Tags
  # field in the 'post' table 
  tag_file     = 'stackoverflow.com/tag.csv'
  posttag_file = 'stackoverflow.com/posttag.csv'

  con = MySQLdb.connect(host=mysql_host,
    user=mysql_user, passwd=mysql_password, db="so")

  cur = con.cursor()

  sys.stdout.write(" Prepping")
  # get n so we can monitor progress
  cur.execute('SELECT count(*) FROM post WHERE postTypeId = 1;')
  n = cur.fetchone()
  n = n[0]
  sys.stdout.write(" .")
  # iterate over the Tags from the Posts table
  cur.execute('SELECT id, tags FROM post WHERE postTypeId = 1;')
  sys.stdout.write(" .\n")

  # process the tags
  tag = pd.DataFrame(columns=['tag'])
  posttag = pd.DataFrame(columns=['pid', 'tid'])
  i = 1

  for pid, ptag in cur.fetchall():
    if ptag:
      # seperate the tags out
      ptag = re.split('[<>]', ptag)
      ptag = filter(None, ptag)
      ptag = pd.DataFrame(ptag, columns=['tag'])
      
      # identify any new tags that we dont already know about
      new_tag = ptag[~ptag.tag.isin(tag.tag)]
      
      if not new_tag.empty:
        # grow the list of unique tags
        tag = tag.append(new_tag, ignore_index=True)
      
      # append new pid-tid pairs
      ptag['pid'] = pid
      ptag['tid'] = tag.index[tag.tag.isin(ptag.tag)]
      
      posttag = posttag.append(ptag[['pid', 'tid']], ignore_index=True)

      # print progress
      msg = i / float(n) * 100
      msg = "{:5.1f}".format(msg)
      msg = " Processing tags: " + msg + "%"
      sys.stdout.write(msg + "\r")
      i += 1

  sys.stdout.write(msg + "\n")

  # update tag index, so we dont want a "zero" id
  tag.index += 1
  posttag.tid += 1

  # export to CSV files
  sys.stdout.write(" Exporting to CSVs")
  tag.to_csv(tag_file, header=True, index_label='id',
    quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8')
  sys.stdout.write(" .")
  posttag.to_csv(posttag_file, header=True, index=False, encoding='utf-8')
  sys.stdout.write(" .\n")

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-u', '--user')
  parser.add_argument('-p', '--password')
  parser.add_argument('-h', '--host')
  args = parser.parse_args()
  concatenate_tags(args.user, ars.password, args.host)
