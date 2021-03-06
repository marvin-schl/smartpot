import time
from src import mcp342x
from src.mcp342x import I2CBussError
from threading import Lock
import logging
import configparser
#setup config
config = configparser.ConfigParser()
config.read("smartpot.ini")
#setup logger
# get root Logger
log = logging.getLogger()

class MCP3426:
    def __init__(self, busnumber = 1):
        """
        Creates the an new instance of the MCP3426 ADC. This class wraps the mcp342x library for an OOP and threadsafe access.
        :param busnumber: (optional) i2c busnumber where the MCP is connected. Default value is 1.
        """
        assert busnumber in [0, 1]
        self.__busnumber = busnumber
        self.__slave_address = 0x68
        self.__adc = mcp342x.Mcp3426(self.__busnumber, self.__slave_address)
        self.__first_channel = mcp342x.Channel(self.__adc, 0)
        self.__second_channel = mcp342x.Channel(self.__adc, 1)
        self.__lock = Lock()


    def read_ch1(self):
        """ read the signal-value of channel a from the MCP3426
            and return the voltage in volt """
        #locking the adc so no other thread can mess up conversion
        log.debug(type(self).__name__ + " - Acquiring Lock for Channel 1.")
        with self.__lock:
            #configure the sensor
            self.__first_channel.sample_rate = 240
            self.__first_channel.pga_gain = 1
            self.__first_channel.continuous = True
            log.debug(type(self).__name__ + " - Configuring Channel 1. SPS="+str(self.__first_channel.sample_rate)+
                                                                    ", Gain="+str(self.__first_channel.pga_gain)+
                                                                    ", continuous="+str(self.__first_channel.continuous))
            try:
                #start the conversion
                log.debug(type(self).__name__ + " - Starting Conerversion on Channel 1. Waiting "+ str(self.__first_channel.conversion_time/1000) +"ms till finished")
                self.__first_channel.start_conversion()
                time.sleep(self.__first_channel.conversion_time)
                #read and return the adc value
                voltage = self.__first_channel.get_conversion_volts()
                log.debug(type(self).__name__ + " - Conversion on Channel 1 should be finished. Conversion Result is "+str(voltage)+"V")
                #release lock after conversion
            except I2CBussError as e:
                log.error(type(self).__name__ + " - I2CBusError: Device may be not connected correctly. " + str(e))
                voltage = -999
        log.debug(type(self).__name__ + " - Released Lock for Channel 1.")

        return voltage

    def read_ch2(self):
        """ read the signal-value of channel a from the MCP3426
            and return the voltage in volt """
        # locking the adc so no other thread can mess up conversion
        log.debug(type(self).__name__ + " - Acquiring Lock for Channel 2.")
        with self.__lock:
            #configure the sensor
            self.__second_channel.sample_rate = 240
            self.__second_channel.pga_gain = 1
            self.__second_channel.continuous = True
            log.debug(
                type(self).__name__ + " - Configuring Channel 2 SPS=" + str(self.__first_channel.sample_rate) +
                ", Gain=" + str(self.__first_channel.pga_gain) +
                ", continuous="+str(self.__first_channel.continuous))
            try:
                #start the conversion
                log.debug(type(self).__name__ + " - Starting Conerversion on Channel 2. Waiting "+ str(self.__second_channel.conversion_time/1000) +"ms till finished")
                self.__second_channel.start_conversion()
                time.sleep(2*self.__second_channel.conversion_time)
                #read and return the adc value
                voltage = -self.__second_channel.get_conversion_volts() #minus because of swapped CH2+ and CH2- in rev1.1 Shield
                log.debug(type(self).__name__ + " - Conversion on Channel 2 should be finished. Conversion Result is "+str(voltage)+"V")
            except I2CBussError as e:
                log.error(type(self).__name__ + " - I2CBusError: Device may be not connected correctly. " + str(e))
                voltage = -999
        log.debug(type(self).__name__ + " - Released Lock for Channel 2.")
        return voltage
