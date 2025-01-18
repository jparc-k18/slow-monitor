import epics
import os
from multiprocessing import Pool

import myenv

pv_list = [
  'HDRGPM:T1IN:MEAN_X',
  'HDRGPM:T1IN:MEAN_Y',
  'HDRGPM:T1IN:SIGMA_X',
  'HDRGPM:T1IN:SIGMA_Y',
  'HDPPS:K18:CNTR1_1S',
  'HDPPS:K18:CNTR1_INTG_HR',
  'HDPPS:K18BR:CNTR1_1S',
  'HDPPS:K18BR:CNTR1_INTG_HR',
  'RADHD:ORG0201G:VAL:LEVEL',
  'RADHD:ORG0201N:VAL:LEVEL',
  'RADHD:ORG0202G:VAL:LEVEL',
  'RADHD:ORG0202N:VAL:LEVEL',
]

#______________________________________________________________________________
def fetch_pv_value(pv_name):
  try:
    pv = epics.PV(pv_name)
    pv.wait_for_connection(timeout=0.2)
    value = pv.get()
    unit = pv.units
    return pv_name, value, unit
  except Exception as e:
    return None, e

#______________________________________________________________________________
def read():
  lines = []
  with Pool(processes=8) as pool:
    results = pool.map(fetch_pv_value, pv_list)
    # print(results)
  # tags = {}
  fields = {}
  for pv_name, value, unit in results:
    if value is not None:
      measurement = pv_name.lower().split(':')[0]
      # location = pv_name.lower().split(':')[1]
      field = pv_name.lower().split(':')[1:]
      # print(measurement, field)
      if measurement not in fields:
        # tags[measurement] = {}
        fields[measurement] = []
      # tags[measurement][field] = f'location={location}'
      fields[measurement].append(f'{"_".join(field)}={value}')
  # print(f'tags = {tags}')
  # print(f'fields = {fields}')
  for m, f in fields.items():
    lines.append(f'{m} {",".join(f)}')
  print('\n'.join(lines))

#______________________________________________________________________________
if __name__ == '__main__':
  read()
