import epics
import numpy
import os
import subprocess
from multiprocessing import Pool

import myenv

measurement = 'v895'

hosts = ['ctrl2', 'vme05'# , 'vme08'
         ]

#______________________________________________________________________________
def read_log(remote_host, last_log='CaenV895/last_param.log'):
  try:
    stdout = subprocess.check_output(
      ['ssh', remote_host, 'cat', last_log], text=True)
    return stdout
  except subprocess.CalledProcessError as e:
    print(e)

#______________________________________________________________________________
def read():
  for host in hosts:
    lines = read_log(host).splitlines()
    param_path = None
    param = {}
    for line in lines:
      if param_path is None:
        param_path = line
      columns = line.split()
      if len(columns) == 3 and columns[0] == '=====':
        addr = columns[1]
        param[columns[1]] = {}
      elif len(columns) == 3 and columns[0] == 'enable:':
        enable_bits = columns[1] + columns[2]
        enable = []
        for e in enable_bits:
          enable.append(e)
        param[addr]['enable'] = enable
      elif len(columns) == 9 and columns[0] == 'threshold:':
        threshold_bits = columns[1:]
        param[addr]['threshold'] = []
        for th in threshold_bits:
          param[addr]['threshold'].append(th)
      elif len(columns) == 8:
        threshold_bits = columns[0:]
        for th in threshold_bits:
          param[addr]['threshold'].append(th)
    # print(param_path)
    # print(param)
    for addr, p in param.items():
      for ch in range(16):
      # for key, l in p.items():
        # for ch, val in enumerate(l):
        print(f'{measurement},host={host},vme_address={addr},channel={ch:02d} enable={p["enable"][ch]},threshold={p["threshold"][ch]}')

#______________________________________________________________________________
if __name__ == '__main__':
  read()
