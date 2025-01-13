import epics
import os
from multiprocessing import Pool

os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'no'
os.environ['EPICS_CA_ADDR_LIST'] = '192.168.30.255 192.153.109.232'

pv_tail_list = [
  'NEG_IMON',
  'NEG_VMON',
  'NEG_VSET',
  'POS_IMON',
  'POS_VMON',
  'POS_VSET',
  'CCG_PMON',
]

#______________________________________________________________________________
def fetch_pv_value(pv_name):
  try:
    pv = epics.PV(pv_name)
    pv.wait_for_connection(timeout=1.0)
    value = pv.get()
    unit = pv.units
    return pv_name, value, unit
  except Exception as e:
    return None, e
#______________________________________________________________________________
def read():
  lines = []
  for ess in ['ESS1', 'ESS2']:
    pv_list = []
    fields = []
    for pv_tail in pv_tail_list:
      pv_name = 'HDESS:K18_' + ess + ':' + pv_tail
      pv_list.append(pv_name)
    with Pool(processes=len(pv_list)) as pool:
      results = pool.map(fetch_pv_value, pv_list)
      # print(results)
    for pv_name, value, unit in results:
      # value = epics.caget(pv_name)
      if value is not None:
        field = pv_name.split(':')[2].lower()
        fields.append(f'{field}={value}')
    lines.append(f'{ess.lower()} {",".join(fields)}')
  print('\n'.join(lines))

#______________________________________________________________________________
if __name__ == '__main__':
  read()
