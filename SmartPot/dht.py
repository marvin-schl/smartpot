import Adafruit_DHT
from threading import Lock
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
    """
    Wrapper Class for a DHT Device for an OOP and threadsafe access.
    """

    DHT11 = Adafruit_DHT.DHT11
    DHT22 = Adafruit_DHT.DHT22

    def __init__(self, pin, dht_type):
        """
        Creates an DHT Device.

        :param pin: Signal Pin in BCM Mode. See `sudo gpio readall`.
        :param dht_type:
        """
        self.__pin = pin
        self.__lock = Lock()
        if dht_type == "DHT22":
            self.__dht_type = DHT.DHT22
        else:
            self.__dht_type = DHT.DHT11

    def __read_values(self):
        """
        Private Method for reading humidty in percent and temperature in 'C.
        :return: (humidity, temperature)
        """
        logging.debug(type(self).__name__ + " - Acquiring Lock on DHT Device...")
        self.__lock.acquire()
        ret = Adafruit_DHT.read_retry(self.__dht_type, self.__pin)
        self.__lock.release()
        logging.debug(type(self).__name__ + " - Released Lock on DHT Device...")

        return ret

    def read_temperature(self):
        """
        Read the current temperature.
        :return: Return temperature in 'C.
        """
        return self.__read_values()[1]

    def read_humidity(self):
        """
        Read the current humidity.
        :return: Return humidity in percent.
        """
        return self.__read_values()[0]