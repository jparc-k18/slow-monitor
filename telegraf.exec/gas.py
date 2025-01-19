import epics
import numpy
import os
from multiprocessing import Pool

import myenv

measurement = 'gas'

pv_list = [
  'GAS:SDC3:DIFP',
  'GAS:SDC4:DIFP',
  'GAS:SDC5:DIFP',
]

#______________________________________________________________________________
def fetch_pv_value(pv_name):
  try:
    pv = epics.PV(pv_name)
    pv.wait_for_connection(timeout=0.2)
    value = pv.get()
    unit = pv.units
    if isinstance(value, numpy.ndarray):
      value = value[0]
    location = pv_name.lower().split(':')[1]
    field = pv_name.lower().split(':')[2]
    return measurement, location, field, value, unit
  except Exception as e:
    return None, e, None

#______________________________________________________________________________
def read():
  lines = []
  with Pool(processes=8) as pool:
    results = pool.map(fetch_pv_value, pv_list)
    # print(results)
  tags = {}
  fields = {}
  for measurement, location, field, value, unit in results:
    if value is not None:
      # print(measurement, location, field, value)
      if location not in fields:
        tags[location] = {}
        fields[location] = []
      tags[location][field] = f'location={location}'
      fields[location].append(f'{field}={value}')
  # print(f'tags = {tags}')
  # print(f'fields = {fields}')
  for l, f in fields.items():
    lines.append(f'{measurement},location={l} {",".join(f)}')
  print('\n'.join(lines))

#______________________________________________________________________________
if __name__ == '__main__':
  read()
