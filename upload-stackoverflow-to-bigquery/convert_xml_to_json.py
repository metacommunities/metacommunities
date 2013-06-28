#!/usr/bin/env python

import argparse
import json
import locale
from lxml import etree
import os
import operator
import sys


def close_json(tmp_file, out_path, table_name, i):
  count = str(i).zfill(8)
  out_file = os.path.join(out_path, '%s_%d.json' % (table_name, i))
  os.rename(tmp_file, out_file)


def convert_xml(input_path, table_name, size):
  locale.setlocale(locale.LC_ALL, '')
  
  in_file  = os.path.join(input_path, table_name + '.xml')
  
  out_path = input_path + '_JSON'
  if not os.path.exists(out_path):
    os.makedirs(out_path)
  
  sys.stdout.write("converting %s to JSON:\n" % (table_name))
  
  # start iterating over the records
  i = 0
  new_file = True
  for action, element in etree.iterparse(in_file, tag='row'):
    if new_file:
      # create tmp file for wip
      tmp_file = os.path.join(out_path, 'tmp.json')
      with open(tmp_file, mode='wb') as f:
        f.write("")
    
    i += 1
    
    # all information for a record is stored as attributes inside the element
    row = dict(element.attrib)
    
    with open(tmp_file, mode='ab') as f:
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
      current_size = os.path.getsize(tmp_file) / 1048576  # MB
      if current_size > size:
        close_json(tmp_file, out_path, table_name, i)
        new_file = True
  
  # final close
  if (size is not None and current_size < size) or size is None:
    close_json(tmp_file, out_path, table_name, i)
  
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
  convert_xml(args.input_dir, args.table, args.size)

