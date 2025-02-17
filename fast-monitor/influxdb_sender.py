from logging import getLogger
import requests

logger = getLogger(__name__)

INFLUXDB_URL = 'http://localhost:8086/api/v2/write'
INFLUXDB_TOKEN = '4jZ5ZXaWgs4Xpg7WnK-PjYsQ4gYHjCO8kTcEnWorK14hHbyXjA0avfCq4kCxvp6XsDnHNqywmXXTF8dN8uvSkQ=='
INFLUXDB_ORG = 'k18'
INFLUXDB_BUCKET = 'field'

headers = {
  "Authorization": f"Token {INFLUXDB_TOKEN}",
  "Content-Type": "text/plain"
}
params = {
  "org": INFLUXDB_ORG,
  "bucket": INFLUXDB_BUCKET,
  "precision": "ns"
}
proxies = {"http": None, "https": None}

def send(data):
  response = requests.post(INFLUXDB_URL, headers=headers, params=params,
                           data=data, proxies=proxies)
  if response.status_code == 204:
    logger.info(f"Data successfully written to InfluxDB")
  else:
    logger.error(f"Failed to write data to InfluxDB: {response.text}")
