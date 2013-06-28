#!/usr/bin/env python

import argparse
import json
import locale
from lxml import etree
import os
import operator
import sys

def new_tmp_json(filename):
  with open(filename, mode='wb') as f:
    f.write("")

def close_json(tmp_file, out_path, table_name, i):
  out_file = os.path.join(out_path, '%s_%d.json' % (table_name, i))
  os.rename(tmp_file, out_file)
  os.remove(tmp_file)

def convert_xml(input_path, table_name, nrows):
  locale.setlocale(locale.LC_ALL, '')
  
  in_file  = os.path.join(input_path, table_name + '.xml')
  
  out_path = input_path + '_JSON'
  if not os.path.exists(out_path):
    os.makedirs(out_path)
  out_file = os.path.join(out_path, table_name + '.json')
  
  sys.stdout.write("converting %s to JSON:\n" % (table_name))

  # create tmp file for wip
  tmp_file = os.path.join(out_path, 'tmp.json')
  new_tmp_json(tmp_file)
  
  # start iterating over the records
  i = 0
  for action, element in etree.iterparse(in_file, tag='row'):
    i += 1
    row = dict(element.attrib)
    
    with open(tmp_file, mode='ab') as f:
      if i > 1:
        f.write("\n")
        
      json.dump(row, f, default=operator.attrgetter('__dict__'), sort_keys=True)
    
    element.clear()
    
    # display progress
    if i % 1000 is 0:
      fi = locale.format("%d", i, grouping=True)
      sys.stdout.write("\r  %s records processed " % (fi))
      sys.stdout.flush()
    
    # is it time to start a new file?
    if nrows is not None and i % nrows is 0:
      close_json(tmp_file, out_path, table_name, i)
      new_tmp_json(tmp_file)
  
  # final close
  if (nrows is not None and i % nrows is not 0) or nrows is None:
    close_json(tmp_file, out_path, table_name, i)
  
  # final print of progress
  fi = locale.format("%d", i, grouping=True)
  sys.stdout.write("\r  %s records processed\n\n" % (fi))
  sys.stdout.flush()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input-dir', default='stackoverflow.com')
  parser.add_argument('-t', '--table')
  parser.add_argument('-n', '--nrows', default=None)
  args = parser.parse_args()
  convert_xml(args.input_dir, args.table, args.nrows)

