from pathlib import Path
from pprint import pprint

dump_data = Path('./seed.txt')

dump_list = []
with dump_data.open() as f:
  dump_strs = f.read().split()
  _xyz = []
  for _ in dump_strs:
    _xyz.append(float(_))
    if len(_xyz) == 3:
      dump_list.append(_xyz)
      _xyz = []


    

for i in dump_list:
  print('---')
  print(i)

print(len(dump_list))
