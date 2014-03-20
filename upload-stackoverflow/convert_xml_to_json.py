#!/usr/bin/env python

import csv
import argparse
import json
import locale
from lxml import etree
import os
import operator
import re
import sys


def close_file(tmp_file, out_path, table_name, i):
  ext = re.search('tmp\.(sql|json)', tmp_file).group(1)
  count = str(i).zfill(8)
  out_file = os.path.join(out_path, '%s_%d.%s' % (table_name, i, ext))
  os.rename(tmp_file, out_file)


def convert_xml(input_path, table_name, size, user, passwd, host):
  locale.setlocale(locale.LC_ALL, '')
  
  in_file  = os.path.join(input_path, 'stackoverflow.com-' + table_name)
  
  header = get_header(user, passwd, host, table_name)
  
  # export paths
  out_json = input_path + '_JSON'
  
  if not os.path.exists(out_json):
    os.makedirs(out_json)

  sys.stdout.write("converting %s to JSON and SQL:\n" % (table_name))
  
  # start iterating over the records
  i = 0
  new_file = True
  for action, element in etree.iterparse(in_file, tag='row'):
    if new_file:
      # create tmp file for wip
      tmp_json = os.path.join(out_json, 'tmp.json')
      
      with open(tmp_json, mode='wb') as f:
        f.write("")
    
    i += 1
    
    # all information for a record is stored as attributes inside the element
    row = dict(element.attrib)
    
    # append to json
    with open(tmp_json, mode='ab') as f:
      # bigquery wants the json to be "newline delimited"
      if new_file:
        new_file = False
      else:
        f.write("\n")
      
      json.dump(row, f, default=operator.attrgetter('__dict__'), sort_keys=True)
    
    element.clear()

    # display progress
    if i % 10000 is 0:
      fi = locale.format("%d", i, grouping=True)
      sys.stdout.write("\r  %s records processed " % (fi))
      sys.stdout.flush()
    
    # is it time to start a new file?
    if size is not None:
      current_size = os.path.getsize(tmp_json) / 1048576  # MB
      if current_size > size:
        close_file(tmp_json, out_json, table_name, i)
        new_file = True
  
  # final close
  if (size is not None and current_size < size) or size is None:
    close_file(tmp_json, out_json, table_name, i)
    
  
  # final print of progress
  fi = locale.format("%d", i, grouping=True)
  sys.stdout.write("\r  %s records processed\n\n" % (fi))
  sys.stdout.flush()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input-dir')
  parser.add_argument('-t', '--table')
  parser.add_argument('-s', '--size', type=int, default=None)
  args = parser.parse_args()
  convert_xml(args.input_dir, args.table, args.size, args.user, args.passwd,
    args.host)

