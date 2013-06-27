#!/usr/bin/env python

import argparse
import json
import locale
from lxml import etree
import os
import operator
import sys

def convert_xml(input_path, table_name):
  locale.setlocale(locale.LC_ALL, '')
  
  in_file  = os.path.join(input_path, table_name + '.xml')
  
  out_path = input_path + '_JSON'
  if not os.path.exists(out_path):
    os.makedirs(out_path)
  out_file = os.path.join(out_path, table_name + '.json')
  
  sys.stdout.write("converting %s to JSON:\n" % (table_name))

  # create empty file
  with open(out_file, mode='wb') as f:
    f.write("")
  
  # start iterating over the records
  i = 0
  for action, element in etree.iterparse(in_file, tag='row'):
    i += 1
    row = dict(element.attrib)
    
    with open(out_file, mode='ab') as f:
      if i > 1:
        f.write("\n")
        
      json.dump(row, f, default=operator.attrgetter('__dict__'), sort_keys=True)
    
    element.clear()
    
    # display progress
    if i % 1000 == 0:
      fi = locale.format("%d", i, grouping=True)
      sys.stdout.write("\r  %s records processed " % (fi))
      sys.stdout.flush()
  
  # final print of progress
  fi = locale.format("%d", i, grouping=True)
  sys.stdout.write("  %s records processed\n\n" % (fi))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input-dir', default='stackoverflow.com')
  parser.add_argument('-t', '--table')
  args = parser.parse_args()
  convert_xml(args.input_dir, args.table)

