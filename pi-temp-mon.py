import Adafruit_DHT as adht
from influxdb import InfluxDBClient
import logging
import time

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def initdb():
    host = '10.78.0.155'
    port = 8086
    dbname = "pisensi"
    try:
        client = InfluxDBClient(host, port, dbname)
        client.switch_database(dbname)
    except Exception as e:
        print(e)
        time.sleep(interval)
        main()
    else:
        return client


def writetodb(client):
    measurement = "sensi01-dht22"
    location = "kitchen"
    interval = 60
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
            time.sleep(interval)
            main()
        else:
            try:
                # Send the JSON data to InfluxDB
                client.write_points(data)
            except Exception as e:
                print(e)
                time.sleep(interval)
                main()
            else:
                # Wait until it's time to query again...
                time.sleep(interval)


def main():
    client = initdb()
    writetodb(client)


if __name__ == '__main__':
    main()

