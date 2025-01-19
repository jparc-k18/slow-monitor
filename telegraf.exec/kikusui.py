import epics
import numpy
import os
from multiprocessing import Pool

import myenv

measurement = 'pmx'

pv_list = [
  'PMX:SDC3_VTH:VMON',
  'PMX:SDC3_VTH:IMON',
  'PMX:SDC4_VTH:VMON',
  'PMX:SDC4_VTH:IMON',
  'PMX:SDC5_VTH:VMON',
  'PMX:SDC5_VTH:IMON',
  'PMX:LSO1:VMON',
  'PMX:LSO1:IMON',
  'PMX:LSO2:VMON',
  'PMX:LSO2:IMON',
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
    device = pv_name.lower().split(':')[1]
    field = pv_name.lower().split(':')[2]
    return measurement, device, field, value, unit
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
  for measurement, device, field, value, unit in results:
    if value is not None:
      # print(measurement, device, field, value)
      if device not in fields:
        tags[device] = {}
        fields[device] = []
      tags[device][field] = f'device={device}'
      fields[device].append(f'{field}={value}')
  # print(f'tags = {tags}')
  # print(f'fields = {fields}')
  for l, f in fields.items():
    lines.append(f'{measurement},device={l} {",".join(f)}')
  print('\n'.join(lines))

#______________________________________________________________________________
if __name__ == '__main__':
  read()
