"""
Example Script to demonstrate monitor usage.
"""
import time
from SmartPot.smartpot import SmartPot
from monitor import TimeBasedMonitor, HysteresisMonitor
from datetime import datetime
import logging
import configparser
import sys
#setup config
config = configparser.ConfigParser()
config.read("smartpot.ini")
levels = {"DEBUG": logging.DEBUG, "ERROR":logging.ERROR, "WARN":logging.WARN, "INFO":logging.INFO}
#setup logger
# create logger with 'smartpot'
log = logging.getLogger('smartpot')
log.setLevel(levels.get(config["Logging"]["level"], "DEBUG"))

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# create file handler which logs even debug messages
fh = logging.FileHandler(config["Logging"]["file"])
fh.setLevel(levels.get(config["Logging"]["level"], "DEBUG"))
fh.setFormatter(formatter)
log.addHandler(fh)

if config["Logging"]["stdout"] == "1":
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(levels.get(config["Logging"]["level"], "DEBUG"))
    ch.setFormatter(formatter)
    log.addHandler(ch)

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

log.debug("Starting Monitors...")
humidity_mon = HysteresisMonitor("Humidity", s.read_humidity, 70, callback, callback_lw_thres=callback3, lower_thres=50)
humidity_mon2 = TimeBasedMonitor("Humidity", monitor_getter, callback2, 1)
humidity_mon.start()
humidity_mon2.start()
log.debug("finisgin")

while True:
    time.sleep(0.1)

