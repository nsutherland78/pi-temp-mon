import logging
import socket
import time

import adafruit_dht as adht
import board
from influxdb import InfluxDBClient

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

FAILCOUNT = 0
INTERVAL = 60


def initdb():
    global FAILCOUNT
    global INTERVAL
    host = '10.78.0.155'
    port = 8086
    dbname = "pisensi"
    try:
        client = InfluxDBClient(host, port, dbname)
        client.switch_database(dbname)
    except Exception as exc:
        logging.error(exc, exc_info=True)
        FAILCOUNT = FAILCOUNT + 1
        time.sleep(INTERVAL * FAILCOUNT)
        main()
    else:
        return client


def writetodb(client, dht):
    global FAILCOUNT
    global INTERVAL
    hostname = socket.gethostname()
    measurement = hostname + "-dht22"
    # Run until you get a CTRL+C
    while True:
        try:
            humidity = dht.humidity
            temperature = dht.temperature
            data = [
            {
              "measurement": measurement,
                  "tags": {},
                  "time": time.asctime(),
                  "fields": {
                      "temperature" : temperature,
                      "humidity": humidity
                  }
              }
            ]
        except KeyboardInterrupt:
            pass
        except RuntimeError as exc:
            logging.error(exc)
            continue
        except Exception as exc:
            logging.error(exc, exc_info=True)
            time.sleep(INTERVAL)
            main()
        else:
            try:
                # Send the JSON data to InfluxDB
                client.write_points(data)
            except Exception as exc:
                logging.error(exc, exc_info=True)
                time.sleep(INTERVAL * FAILCOUNT)
                FAILCOUNT = FAILCOUNT + 1
                main()
            else:
                # Successful write to DB, reset FAILCOUNT and Wait until it's time to read/write values again...
                FAILCOUNT = 0
                time.sleep(INTERVAL)


def main():
    dht = adht.DHT22(board.D4, False)
    client = initdb()
    writetodb(client, dht)


if __name__ == '__main__':
    main()
