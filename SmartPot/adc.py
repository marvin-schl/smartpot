import time
import SmartPot.mcp342x as mcp342x

class MCP3426:
    def __init__(self, busnumber = 1):
        """
        Creates the an new instance of the MCP3426 ADC. This class wraps the mcp342x library for an OOP access.
        :param busnumber: (optional) i2c busnumber where the MCP is connected. Default value is 1.
        """
        assert busnumber in [0, 1]
        self.__busnumber = busnumber
        self.__slave_address = 0x68
        self.__adc = mcp342x.Mcp3426(self.__busnumber, self.__slave_address)
        self.__first_channel = mcp342x.Channel(self.__adc, 0)
        self.__second_channel = mcp342x.Channel(self.__adc, 1)


    def read_ch1(self):
        """ read the signal-value of channel a from the MCP3426
            and return the voltage in volt """
        #configure the sensor
        self.__first_channel.sample_rate = 240
        self.__first_channel.pga_gain = 1
        self.__first_channel.continuous = True
        #start the conversion
        self.__first_channel.start_conversion()
        time.sleep(self.__first_channel.conversion_time)
        #read and return the adc value
        return self.__first_channel.get_conversion_volts()

    def read_ch2(self):
        """ read the signal-value of channel a from the MCP3426
            and return the voltage in volt """
        #configure the sensor
        self.__second_channel.sample_rate = 240
        self.__second_channel.pga_gain = 1
        self.__second_channel.continuous = True
        #start the conversion
        self.__second_channel.start_conversion()
        time.sleep(self.__second_channel.conversion_time)
        #read and return the adc value
        return -self.__second_channel.get_conversion_volts() #minus because of swapped CH2+ and CH2- in rev1.1 Shield