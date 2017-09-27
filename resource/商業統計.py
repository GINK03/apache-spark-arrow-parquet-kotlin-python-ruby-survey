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
  for k in list(obj.keys()):
    if re.search('\d{4}',k):
      obj[k] = obj[k].replace(',', '')
      try:
        obj[k] = float( obj[k] )
      except:
        obj[k] = None
    if k == '市区町村名':
      obj['contry'] = obj[k]
      del obj[k]
    if k == '市区町村コード':
      obj['city'] = obj[k]
      del obj[k]
    if '年' in k:
      obj[ k.replace('年', '') ] = obj[k]
      del obj[k]
  print('a', obj )
  w.write( json.dumps(obj, ensure_ascii=False) + '\n' )
