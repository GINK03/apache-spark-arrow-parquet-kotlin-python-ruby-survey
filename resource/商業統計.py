import os
import re
import json

f = open('商業統計.txt')
keys = re.split(r'\s{1,}', next(f).strip())
print(keys)
w = open('商業統計.json', 'w')
for vals in f:
  vals = re.split(r'\s{1,}', vals.strip())
  obj = dict( zip(keys, vals) )
  print( obj ) 
  for k in obj.keys():
    if re.search('\d{4}',k):
      obj[k] = obj[k].replace(',', '')
      try:
        obj[k] = float( obj[k] )
      except:
        obj[k] = None
  print('a', obj )
  w.write( json.dumps(obj, ensure_ascii=False) + '\n' )
