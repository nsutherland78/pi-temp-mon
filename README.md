# pi-temp-mon

## Requirements

You will require the following physical components:
* Raspberry Pi
* DHT22 Sensor + board <https://www.amazon.com/gp/product/B018JO5BRK>

You will require the following technical components:
* An influx DB instance
* Python3 + Below modules
 * influxdb 
 * Adafruit_DHT

## Install

Once that is done, perform the following to install necessary requirements:
```
sudo pip3 install -r requirements.txt
```

Clone the repo into the home directory:
```
git clone git@github.com:nsutherland78/pi-temp-mon.git
```

Start the program as a daemon in screen
```
screen
sudo python3 pi-temp-mon.py &
```

Voila!

## Resources
* <https://www.amazon.com/gp/product/B018JO5BRK>
* <https://create.arduino.cc/projecthub/mafzal/temperature-monitoring-with-dht22-arduino-15b013>
* <https://medium.com/@hemant6488/monitoring-temperature-and-humidity-using-influxdb-and-grafana-on-raspberry-pi-eb4f3ece3674>
* <https://www.ardumotive.com/how-to-use-dht-22-sensor-en.html>
* <https://www.influxdata.com/blog/getting-started-python-influxdb/>


## Contributors
Nathan Sutherland (nathan.sutherland@gmail.com)
