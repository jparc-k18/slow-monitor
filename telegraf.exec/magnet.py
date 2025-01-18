import epics
import os
from multiprocessing import Pool

import myenv

pv_list = [
  'HDPS:AK18D1:CMON',
  'HDPS:AK18D1:CSET',
  'HDPS:AK18D1:POL',
  'HDPS:AK11D1:CMON',
  'HDPS:AK11D1:CSET',
  'HDPS:AK11D1:POL',
  'HDPS:AH18:CMON',
  'HDPS:AH18:CSET',
  'HDPS:AH18:POL',
  'HDPS:BSM1:CMON',
  'HDPS:BSM1:CSET',
  'HDPS:BSM1:POL',
  # 'K18MAG:S2SD1:FLD',
  # 'K18MAG:D4:FLD',
  'HDPS:K18CM1:CMON',
  'HDPS:K18CM1:CSET',
  'HDPS:K18CM1:POL',
  'HDPS:K18CM2:CMON',
  'HDPS:K18CM2:CSET',
  'HDPS:K18CM2:POL',
  'HDPS:K18CM3:CMON',
  'HDPS:K18CM3:CSET',
  'HDPS:K18CM3:POL',
  'HDPS:K18CM4:CMON',
  'HDPS:K18CM4:CSET',
  'HDPS:K18CM4:POL',
  'HDPS:K18D2:CMON',
  'HDPS:K18D2:CSET',
  'HDPS:K18D2:POL',
  'HDPS:K18D3:CMON',
  'HDPS:K18D3:CSET',
  'HDPS:K18D3:POL',
  'HDPS:K18D4:CMON',
  'HDPS:K18D4:CSET',
  'HDPS:K18D4:POL',
  'HDPS:K18D4S:CMON',
  'HDPS:K18D4S:CSET',
  'HDPS:K18D4S:POL',
  'HDPS:K18O1:CMON',
  'HDPS:K18O1:CSET',
  'HDPS:K18O1:POL',
  'HDPS:K18O2:CMON',
  'HDPS:K18O2:CSET',
  'HDPS:K18O2:POL',
  'HDPS:K18O3:CMON',
  'HDPS:K18O3:CSET',
  'HDPS:K18O3:POL',
  'HDPS:K18Q10:CMON',
  'HDPS:K18Q10:CSET',
  'HDPS:K18Q10:POL',
  'HDPS:K18Q11:CMON',
  'HDPS:K18Q11:CSET',
  'HDPS:K18Q11:POL',
  'HDPS:K18Q12:CMON',
  'HDPS:K18Q12:CSET',
  'HDPS:K18Q12:POL',
  'HDPS:K18Q13:CMON',
  'HDPS:K18Q13:CSET',
  'HDPS:K18Q13:POL',
  'HDPS:K18Q1:CMON',
  'HDPS:K18Q1:CSET',
  'HDPS:K18Q1:POL',
  'HDPS:K18Q2:CMON',
  'HDPS:K18Q2:CSET',
  'HDPS:K18Q2:POL',
  'HDPS:K18Q3:CMON',
  'HDPS:K18Q3:CSET',
  'HDPS:K18Q3:POL',
  'HDPS:K18Q4:CMON',
  'HDPS:K18Q4:CSET',
  'HDPS:K18Q4:POL',
  'HDPS:K18Q5:CMON',
  'HDPS:K18Q5:CSET',
  'HDPS:K18Q5:POL',
  'HDPS:K18Q6:CMON',
  'HDPS:K18Q6:CSET',
  'HDPS:K18Q6:POL',
  'HDPS:K18Q7:CMON',
  'HDPS:K18Q7:CSET',
  'HDPS:K18Q7:POL',
  'HDPS:K18Q8:CMON',
  'HDPS:K18Q8:CSET',
  'HDPS:K18Q8:POL',
  'HDPS:K18Q9:CMON',
  'HDPS:K18Q9:CSET',
  'HDPS:K18Q9:POL',
  'HDPS:K18S1:CMON',
  'HDPS:K18S1:CSET',
  'HDPS:K18S1:POL',
  'HDPS:K18S2:CMON',
  'HDPS:K18S2:CSET',
  'HDPS:K18S2:POL',
  'HDPS:K18S3:CMON',
  'HDPS:K18S3:CSET',
  'HDPS:K18S3:POL',
  'HDPS:K18S4:CMON',
  'HDPS:K18S4:CSET',
  'HDPS:K18S4:POL',
  'HDPS:S2SQ1:CMON',
  'HDPS:S2SQ1:CSET',
  'HDPS:S2SQ1:POL',
  'HDPS:S2SQ2:CMON',
  'HDPS:S2SQ2:CSET',
  'HDPS:S2SQ2:POL',
  'HDPS:S2SD1:CMON',
  'HDPS:S2SD1:CSET',
  'HDPS:S2SD1:POL',
]

#______________________________________________________________________________
def fetch_pv_value(pv_name):
  try:
    pv = epics.PV(pv_name)
    pv.wait_for_connection(timeout=0.2)
    value = pv.get(as_string=('POL' in pv_name))
    if isinstance(value, str):
      value = f'"{value}"'
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
    if value is not None:
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
