#!/usr/bin/env python
from __future__ import division
from subprocess import PIPE, Popen
import psutil
import time
from ISStreamer.Streamer import Streamer
import Adafruit_DHT

# --------- User Settings ---------
# Initial State settings

# ------- Depricated Stream -------
#BUCKET_NAME = ":computer: Pi3 Performance"
#BUCKET_KEY = "pi0708"
#ACCESS_KEY = "JuEw3pLxo8nwjoK3KyNWxkFxclmW47dU"


# ------- Initial State Stream Definition ---------
BUCKET_NAME = ":computer: Ranch Office Temp and Humidity"
BUCKET_KEY = "JWVX4GNUPH4G"
ACCESS_KEY = "JuEw3pLxo8nwjoK3KyNWxkFxclmW47dU"


# Set the time between checks
MINUTES_BETWEEN_READS = 1
METRIC_UNITS = False
# ---------------------------------

sensor = Adafruit_DHT.AM2302
pin = 4

def get_cpu_temperature():
   process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
   output, _error = process.communicate()
   return float(output[output.index('=') + 1:output.rindex("'")])

def main():
   streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
   while True:
        cpu_temperature = get_cpu_temperature()
        humidity, roomtemp = Adafruit_DHT.read_retry(sensor, pin)
        
# --------- Print Room Temp, CPU Temp, and Room Humidity to Console ---------
        if humidity is not None and roomtemp is not None:
           print('Room Temp={0:0.1f}*F  CPU Temp={0:0.1f}*F Humidity={1:0.1f}%'.format((roomtemp * 9.0 / 5.0 + 32.0), (cpu_temperature * 9.0 / 5.0 + 32.0), humidity))


#------------- EXAMPLE CODE FROM GITHUB ADAFRUIT
#if humidity is not None and temperature is not None:
#    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
#else:
#    print('Failed to get reading. Try again!')

#-------------

# --------- Begin Stream Output to Initialstate.com ---------
        cpu_temperature = cpu_temperature * 9.0 / 5.0 + 32.0
        roomtemp = roomtemp * 9.0 / 5.0 + 32.0          
        streamer.log("CPU Temperature(F)",str("{0:.2f}".format(cpu_temperature)))

        if (roomtemp > 50.0 and roomtemp < 95.0) AND (humidity > 0.1 and humidity < 0.99)
           streamer.log("Room Temperature(F)",str("{0:.2f}".format(roomtemp)))
           streamer.log("Room Humidity",str("{0:.2f}".format(humidity)))
           mem = psutil.virtual_memory()
           mem_used = mem.used / 2**20
           streamer.log("Memory Used(MB)",str("{0:.2f}".format(mem_used)))

# --------- Fulush Stream and Wait Until Next Read ---------
        streamer.flush()
        time.sleep(60*MINUTES_BETWEEN_READS)

if __name__ == '__main__':
   main()
