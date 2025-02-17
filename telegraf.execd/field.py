from epics import PV
from threading import Thread, Lock
import sys
import time

send_interval = 10

buffer = []
lock = Lock()

#______________________________________________________________________________
def on_change(pvname=None, value=None, timestamp=None, **kwargs):
  global buffer
  with lock:
    timestamp_ns = int(timestamp * 1e9)
    line_protocol = f"field,magnet={pvname.replace('K18MAG:', '').replace(':', '_').lower().replace('_fld', '')} value={value} {timestamp_ns}"
    # print(line_protocol)
    # sys.stdout.flush()
    buffer.append(line_protocol)

#______________________________________________________________________________
# def monitor_pv(pv_name):
#   pv = PV(pv_name, callback=on_change)
#   time.sleep(1)
#   while True:
#     if not pv.connected:
#       pv = PV(pv_name, callback=on_change)
#       time.sleep(5)
#     time.sleep(1)

#______________________________________________________________________________
def send_to_influxdb():
  global buffer
  while True:
    time.sleep(send_interval)
    data = []
    with lock:
      if buffer:
        data = "\n".join(buffer)
        buffer = []
    if data:
      print(data)
      sys.stdout.flush()

#______________________________________________________________________________
if __name__ == "__main__":
  pv_list = ["K18MAG:D4:FLD", "K18MAG:S2SD1:FLD"]
  # monitor_threads = []
  for pv_name in pv_list:
    # thread = Thread(target=monitor_pv, args=(pv_name,), daemon=True)
    # thread.start()
    # monitor_threads.append(thread)
    PV(pv_name, callback=on_change)
  send_thread = Thread(target=send_to_influxdb, daemon=True)
  send_thread.start()
  try:
    while True:
      line = sys.stdin.readline()
      if not line:
        break
      time.sleep(1)
  except KeyboardInterrupt:
    print("Stopping...", file=sys.stderr)
  print('done', file=sys.stderr)
