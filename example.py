import logging
import time
from SmartPot.smartpot import SmartPot
from monitor import TimeBasedMonitor, HysteresisMonitor
from datetime import datetime
from threading import Thread


#setup logger
dt = datetime.today()
logging.basicConfig(filename='smartpot.log',
                    filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.DEBUG)

def  monitor_getter():
   return s.read_humidity(), s.read_temperature(), s.read_soil_moisture(), s.read_light_intensity()


def callback(timestamp, value, threshold, name):
    #print("Value "+ name + "=" +str(value)+ "passed threshold of " + str(threshold) + " at " + str(timestamp) +".")
    s.output_on(SmartPot.X4)


def callback3(timestamp, value, threshold, name):
    s.output_off(SmartPot.X4)



def callback2(now, val, name):
    print(str(now) + " - " +name+"="+str(val))

s = SmartPot()
s.output_off(SmartPot.X4)

print("Starting Monitors...")
humidity_mon = HysteresisMonitor("Humidity", s.read_humidity, 70, callback, callback_lw_thres=callback3, lower_thres=50)
humidity_mon2 = TimeBasedMonitor("Humidity", monitor_getter, callback2, 1)
humidity_mon.start()
humidity_mon2.start()

while True:
    time.sleep(0.1)

