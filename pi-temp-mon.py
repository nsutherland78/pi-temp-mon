import Adafruit_DHT as adht
from influxdb import InfluxDBClient
import logging
import time

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
    except Exception as e:
        print(e)
        FAILCOUNT = FAILCOUNT + 1
        time.sleep(INTERVAL * FAILCOUNT)
        main()
    else:
        return client


def writetodb(client):
    global FAILCOUNT
    global INTERVAL
    measurement = "sensi01-dht22"
    location = "kitchen"
    # Run until you get a CTRL+C
    while True:
        try:
            humidity,temperature = adht.read_retry(adht.DHT22, 4)
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
        except Exception as e:
            print(e)
            time.sleep(INTERVAL)
            main()
        else:
            try:
                # Send the JSON data to InfluxDB
                client.write_points(data)
            except Exception as e:
                print(e)
                time.sleep(INTERVAL * FAILCOUNT)
                FAILCOUNT = FAILCOUNT + 1
                main()
            else:
                # Successful write to DB, reset FAILCOUNT and Wait until it's time to read/write values again...
                FAILCOUNT = 0
                time.sleep(INTERVAL)


def main():
    client = initdb()
    writetodb(client)


if __name__ == '__main__':
    main()