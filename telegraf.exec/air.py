import epics
import numpy
import os
from multiprocessing import Pool

import myenv

pv_list = [
  'AIR:BFT_TENT:TEMP',
  'AIR:BFT_TENT:HUMI',
  'AIR:TRG_RACK:TEMP',
  'AIR:TRG_RACK:HUMI',
  'AIR:WCU:TEMP',
  'AIR:WCU:HUMI',
  'AIR:WCD:TEMP',
  'AIR:WCD:HUMI',
  'AIR:BH2_RACK:TEMP',
  'AIR:BH2_RACK:HUMI',
  # 'AIR:HBX:TEMP',
  # 'AIR:HBX:HUMI',
  'AFT:X_U1:TEMP',
  'AFT:X_U2:TEMP',
  'AFT:Y_U:TEMP',
  'AFT:Y_D:TEMP',
  'AFT:X_D1:TEMP',
  'AFT:X_D2:TEMP',
  'AFT:AIR:TEMP',
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
    if 'AFT' in pv_name:
      location = '_'.join(pv_name.lower().split(':')[0:2])
    else:
      location = pv_name.lower().split(':')[1]
    measurement = 'air'
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
    lines.append(f'air,location={l} {",".join(f)}')
  print('\n'.join(lines))

#______________________________________________________________________________
if __name__ == '__main__':
  read()
