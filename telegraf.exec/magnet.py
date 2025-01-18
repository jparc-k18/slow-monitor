import epics
import os
from multiprocessing import Pool

import myenv

magnet_list = [
  'BSM1',
  'AK18D1',
  'AK11D1',
  'AH18',
  'K18Q1',
  'K18Q2',
  'K18D2',
  'K18Q3',
  'K18O1',
  'K18Q4',
  'K18S1',
  'K18CM1',
  'K18CM2',
  'K18S2',
  'K18Q5',
  'K18Q6',
  'K18D3',
  'K18Q7',
  'K18O2',
  'K18S3',
  'K18CM3',
  'K18CM4',
  'K18S4',
  'K18Q8',
  'K18O3',
  'K18Q9',
  'K18Q10',
  'K18Q11',
  'K18D4',
  'K18D4S',
  'K18Q12',
  'K18Q13',
  'S2SQ1',
  'S2SQ2',
  'S2SD1',
]

pv_tail_list = [
  'CMON',
  'CSET',
  'POL',
]

#______________________________________________________________________________
def fetch_pv_value(pv_name):
  try:
    pv = epics.PV(pv_name)
    pv.wait_for_connection(timeout=0.2)
    value = pv.get(as_string=('POL' in pv_name))
    if isinstance(value, str):
      if value == 'POS':
        value = 1
      elif value == 'NEG':
        value = -1
      else:
        value = 'NaN'
    unit = pv.units
    magnet = pv_name.split(':')[1].lower()
    return magnet, pv_name, value, unit
  except Exception as e:
    return None, e

#______________________________________________________________________________
def read():
  lines = []
  pv_list = []
  for i, magnet in enumerate(magnet_list):
    for pv_tail in pv_tail_list:
      pv_name = 'HDPS:' + magnet + ':' + pv_tail
      pv_list.append(pv_name)
  with Pool(processes=8) as pool:
    results = pool.map(fetch_pv_value, pv_list)
    # print(results)
  fields = {}
  for magnet, pv_name, value, unit in results:
    if value is not None:
      field = pv_name.split(':')[2].lower()
      if magnet not in fields:
        fields[magnet] = []
      fields[magnet].append(f'{field}={value}')
  for m, f in fields.items():
    lines.append(f'hdps,magnet={m},order={magnet_list.index(m.upper()):02d} {",".join(f)}')
  print('\n'.join(lines))

#______________________________________________________________________________
if __name__ == '__main__':
  read()
