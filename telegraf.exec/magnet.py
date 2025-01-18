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

# pv_list = [
#   'HDPS:AK18D1:CMON',
#   'HDPS:AK18D1:CSET',
#   'HDPS:AK18D1:POL',
#   'HDPS:AK11D1:CMON',
#   'HDPS:AK11D1:CSET',
#   'HDPS:AK11D1:POL',
#   'HDPS:AH18:CMON',
#   'HDPS:AH18:CSET',
#   'HDPS:AH18:POL',
#   'HDPS:BSM1:CMON',
#   'HDPS:BSM1:CSET',
#   'HDPS:BSM1:POL',
#   # 'K18MAG:S2SD1:FLD',
#   # 'K18MAG:D4:FLD',
#   'HDPS:K18CM1:CMON',
#   'HDPS:K18CM1:CSET',
#   'HDPS:K18CM1:POL',
#   'HDPS:K18CM2:CMON',
#   'HDPS:K18CM2:CSET',
#   'HDPS:K18CM2:POL',
#   'HDPS:K18CM3:CMON',
#   'HDPS:K18CM3:CSET',
#   'HDPS:K18CM3:POL',
#   'HDPS:K18CM4:CMON',
#   'HDPS:K18CM4:CSET',
#   'HDPS:K18CM4:POL',
#   'HDPS:K18D2:CMON',
#   'HDPS:K18D2:CSET',
#   'HDPS:K18D2:POL',
#   'HDPS:K18D3:CMON',
#   'HDPS:K18D3:CSET',
#   'HDPS:K18D3:POL',
#   'HDPS:K18D4:CMON',
#   'HDPS:K18D4:CSET',
#   'HDPS:K18D4:POL',
#   'HDPS:K18D4S:CMON',
#   'HDPS:K18D4S:CSET',
#   'HDPS:K18D4S:POL',
#   'HDPS:K18O1:CMON',
#   'HDPS:K18O1:CSET',
#   'HDPS:K18O1:POL',
#   'HDPS:K18O2:CMON',
#   'HDPS:K18O2:CSET',
#   'HDPS:K18O2:POL',
#   'HDPS:K18O3:CMON',
#   'HDPS:K18O3:CSET',
#   'HDPS:K18O3:POL',
#   'HDPS:K18Q10:CMON',
#   'HDPS:K18Q10:CSET',
#   'HDPS:K18Q10:POL',
#   'HDPS:K18Q11:CMON',
#   'HDPS:K18Q11:CSET',
#   'HDPS:K18Q11:POL',
#   'HDPS:K18Q12:CMON',
#   'HDPS:K18Q12:CSET',
#   'HDPS:K18Q12:POL',
#   'HDPS:K18Q13:CMON',
#   'HDPS:K18Q13:CSET',
#   'HDPS:K18Q13:POL',
#   'HDPS:K18Q1:CMON',
#   'HDPS:K18Q1:CSET',
#   'HDPS:K18Q1:POL',
#   'HDPS:K18Q2:CMON',
#   'HDPS:K18Q2:CSET',
#   'HDPS:K18Q2:POL',
#   'HDPS:K18Q3:CMON',
#   'HDPS:K18Q3:CSET',
#   'HDPS:K18Q3:POL',
#   'HDPS:K18Q4:CMON',
#   'HDPS:K18Q4:CSET',
#   'HDPS:K18Q4:POL',
#   'HDPS:K18Q5:CMON',
#   'HDPS:K18Q5:CSET',
#   'HDPS:K18Q5:POL',
#   'HDPS:K18Q6:CMON',
#   'HDPS:K18Q6:CSET',
#   'HDPS:K18Q6:POL',
#   'HDPS:K18Q7:CMON',
#   'HDPS:K18Q7:CSET',
#   'HDPS:K18Q7:POL',
#   'HDPS:K18Q8:CMON',
#   'HDPS:K18Q8:CSET',
#   'HDPS:K18Q8:POL',
#   'HDPS:K18Q9:CMON',
#   'HDPS:K18Q9:CSET',
#   'HDPS:K18Q9:POL',
#   'HDPS:K18S1:CMON',
#   'HDPS:K18S1:CSET',
#   'HDPS:K18S1:POL',
#   'HDPS:K18S2:CMON',
#   'HDPS:K18S2:CSET',
#   'HDPS:K18S2:POL',
#   'HDPS:K18S3:CMON',
#   'HDPS:K18S3:CSET',
#   'HDPS:K18S3:POL',
#   'HDPS:K18S4:CMON',
#   'HDPS:K18S4:CSET',
#   'HDPS:K18S4:POL',
#   'HDPS:S2SQ1:CMON',
#   'HDPS:S2SQ1:CSET',
#   'HDPS:S2SQ1:POL',
#   'HDPS:S2SQ2:CMON',
#   'HDPS:S2SQ2:CSET',
#   'HDPS:S2SQ2:POL',
#   'HDPS:S2SD1:CMON',
#   'HDPS:S2SD1:CSET',
#   'HDPS:S2SD1:POL',
# ]

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
    lines.append(f'current,magnet={m},order={magnet_list.index(m.upper()):02d} {",".join(f)}')
  print('\n'.join(lines))

#______________________________________________________________________________
if __name__ == '__main__':
  read()
