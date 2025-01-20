import datetime
import json
import logging
import html.parser
import requests
import time

measurement = 'slit'
ip_address = '192.168.30.30'
channel_map = {
  1: ['ifh_left', [35.0000, -147.7280]],
  2: ['ifh_right', [34.9865, -27.7529]],
  3: ['ifv_upper', [9.9545, -14.9513]],
  4: ['ifv_lower', [9.9618, -34.9052]],
  5: ['mom_left', [35.9202, -179.8373]],
  6: ['mom_right', [35.9202, -179.9813]],
  7: ['mass1_upper', [5.9987, -14.9899]],
  8: ['mass1_lower', [5.9983, -14.9979]],
  9: ['mass2_upper', [2.1097, -10.3952]],
  10: ['mass2_lower', [2.1268, -10.7009]],
}

#______________________________________________________________________________
class GL840(html.parser.HTMLParser):
  data_dict = dict()
  ch = None
  val = None
  unit = None

  #____________________________________________________________________________
  def handle_data(self, data):
    data = data.strip().replace(' ', '').replace('+', '')
    if len(data) == 0:
      return
    try:
      float(data)
    except ValueError:
      if 'CH' in data:
        self.ch = int(data[2:])
        self.val = None
        self.unit = None
      else:
        self.unit = data
    else:
      self.val = float(data)
    if (self.ch is not None and
        self.val is not None and
        self.unit is not None):
      self.data_dict[self.ch] = (self.val, self.unit)
      # print(f'Found data: ch={self.ch} '+
      #       f'{self.data_dict[self.ch]}')

  #____________________________________________________________________________
  def get_data(self, ch=None):
    if ch in self.data_dict:
      return self.data_dict[ch]
    else:
      return self.data_dict

  #____________________________________________________________________________
  def parse(self):
    try:
      ret = requests.get(f'http://{ip_address}/digital.cgi?chg=0')
      self.feed(ret.text)
      for ch, pair in gl840.get_data().items():
        name = channel_map[ch][0]
        p = channel_map[ch][1]
        calc = pair[0] * p[0] + p[1]
        print(f'{measurement},ch={ch:02d},name={name} raw_volt={pair[0]},calc_mm={calc}')
    except:
      pass

#______________________________________________________________________________
if __name__ == '__main__':
  gl840 = GL840()
  gl840.parse()
