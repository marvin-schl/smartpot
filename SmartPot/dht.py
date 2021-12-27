import Adafruit_DHT

DHT11 = Adafruit_DHT.DHT11
DHT22 = Adafruit_DHT.DHT22

class DHT:
    """
    Wrapper Class for a DHT Device for an OOP access.
    """

    def __init__(self, pin, dht_type=DHT11):
        """
        Creates an DHT Device.

        :param pin: Signal Pin in BCM Mode. See `sudo gpio readall`.
        :param dht_type:
        """
        self.__pin = pin
        self.__dht_type = dht_type

    def __read_values(self):
        """
        Private Method for reading humidty in percent and temperature in 'C.
        :return: (humidity, temperature)
        """
        return Adafruit_DHT.read_retry(self.__dht_type, self.__pin)

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