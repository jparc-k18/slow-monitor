import epics
import os
from multiprocessing import Pool

import myenv

pv_list = [
  # 'HDSYS:RUN_NO',
  # 'HDSYS:SHOT_NO',
  # 'HDSYS:MR_CYCLE',
  # 'HDSYS:MR_POWER',
  # 'MRMON:DCCT_073_1:VAL:MRPWR',
  'HDSYS:OPR:MODE',
  # 'HDMON:MR_P3:INTENSITY',
  # 'HDMON:SYIM:POWER',
  # 'HDMON:SYIM:INTENSITY',
  # 'HDMON:BDMPIM:INTENSITY',
  # 'MRSLW:SXOPR_D2:VAL:DUTY',
  # 'MRSLW:SXOPR_D2:VAL:ExtEffi',
  # 'MRSLW:SXOPR_D2:VAL:SpLen',
  # 'HDRGPM:T1IN:MEAN_X',
  # 'HDRGPM:T1IN:MEAN_Y',
  # 'HDRGPM:T1IN:SIGMA_X',
  # 'HDRGPM:T1IN:SIGMA_Y',
  # 'HDPPS:K18:CNTR1_1S',
  # 'HDPPS:K18:CNTR1_INTG_HR',
  # 'HDPPS:K18BR:CNTR1_1S',
  # 'HDPPS:K18BR:CNTR1_INTG_HR',
  # 'RADHD:ORG0201G:VAL:LEVEL',
  # 'RADHD:ORG0201N:VAL:LEVEL',
  # 'RADHD:ORG0202G:VAL:LEVEL',
  # 'RADHD:ORG0202N:VAL:LEVEL',
]

#______________________________________________________________________________
def fetch_pv_value(pv_name):
  try:
    pv = epics.PV(pv_name)
    pv.wait_for_connection(timeout=1.0)
    print(help(pv))
    value = pv.get(as_string=True)
    unit = pv.units
    return pv_name, value, unit
  except Exception as e:
    return None, e

#______________________________________________________________________________
def read():
  lines = []
  measurements = []
  fields = {}
  with Pool(processes=8) as pool:
    results = pool.map(fetch_pv_value, pv_list)
    # print(results)
  for pv_name, value, unit in results:
    # value = epics.caget(pv_name)
    if value is not None:
      # field = pv_name.split(':')[2].lower()
      measurement = pv_name.split(':')[0].lower()
      field = '_'.join(pv_name.split(':')[1:])
      if measurement not in fields:
        fields[measurement] = []
      fields[measurement].append(f'{field.lower()}={value}')
  for m, f in fields.items():
    lines.append(f'{m} {",".join(f)}')
  print('\n'.join(lines))

#______________________________________________________________________________
if __name__ == '__main__':
  read()
