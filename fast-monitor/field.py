from epics import PV
from threading import Thread, Lock
from logging import getLogger, basicConfig, INFO
from rich.logging import RichHandler
import sys
import time

import influxdb_sender

send_interval = 10

buffer = []
lock = Lock()

logger = getLogger(__name__)
basicConfig(level=INFO, format='%(message)s', handlers=[RichHandler()])

#______________________________________________________________________________
def monitor_pv(pv_name):
  def on_change(pvname=None, value=None, timestamp=None, **kwargs):
    global buffer
    with lock:
      timestamp_ns = int(timestamp * 1e9)
      line_protocol = f"field,magnet={pvname.replace('K18MAG:', '').replace(':', '_').lower().replace('_fld', '')} value={value} {timestamp_ns}"
      buffer.append(line_protocol)
      logger.info(f"{line_protocol}")
  pv = PV(pv_name, callback=on_change)
  logger.info(f"Monitoring PV: {pv_name}")
  time.sleep(1)
  while True:
    if not pv.connected:
      logger.info(f'{pv_name} disconnected. Trying to reconnect...')
      pv = PV(pv_name, callback=on_change)
      time.sleep(5)
    time.sleep(1)

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
      try:
        influxdb_sender.send(data)
      except Exception as e:
        logger.error(f"Error sending data to InfluxDB: {e}")
        sys.exit(1)
    else:
      logger.warningt('Data is empty')

#______________________________________________________________________________
if __name__ == "__main__":
  pv_list = ["K18MAG:D4:FLD", "K18MAG:S2SD1:FLD"]
  monitor_threads = []
  for pv_name in pv_list:
    thread = Thread(target=monitor_pv, args=(pv_name,), daemon=True)
    thread.start()
    monitor_threads.append(thread)
  send_thread = Thread(target=send_to_influxdb, daemon=True)
  send_thread.start()
  logger.info("Press Ctrl+C to stop")
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    logger.info("Stopping...")
  logger.info('done')
