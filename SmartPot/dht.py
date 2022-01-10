import Adafruit_DHT
from threading import Lock
import logging
import configparser
#setup config
config = configparser.ConfigParser()
config.read("smartpot.ini")
#setup logger
# get root Logger
log = logging.getLogger()

class DHT:
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
        log.debug(type(self).__name__ + " - Acquiring Lock on DHT Device...")
        self.__lock.acquire()
        ret = Adafruit_DHT.read_retry(self.__dht_type, self.__pin)
        self.__lock.release()
        log.debug(type(self).__name__ + " - Released Lock on DHT Device...")

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
