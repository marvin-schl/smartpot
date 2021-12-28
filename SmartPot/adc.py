import time
import SmartPot.mcp342x as mcp342x

class MCP3426:
    def __init__(self, busnumber):
        assert busnumber in [0, 1]
        self.__busnumber = busnumber
        self.__slave_address = 0x68
        self.__adc = mcp342x.Mcp3426(self.__slave_address, self.__busnumber)
        self.__first_channel = mcp342x.Channel(self.__adc, 0)
        self.__second_channel = mcp342x.Channel(self.__adc, 1)


    def read_ch1(self):
        """ read the signal-value of channel a from the MCP3426
            and return the voltage in volt """
        self.__first_channel.sample_rate = 240
        self.__first_channel.pga_gain = 1
        self.__first_channel.continuous = True
        self.__first_channel.start_conversion()
        time.sleep(self.__first_channel.conversion_time)
        return self.__first_channel.get_conversion_volts()

    def read_ch2(self):
        """ read the signal-value of channel a from the MCP3426
            and return the voltage in volt """
        self.__second_channel.sample_rate = 240
        self.__second_channel.pga_gain = 1
        self.__second_channel.continuous = True
        self.__second_channel.start_conversion()
        time.sleep(self.__second_channel.conversion_time)
        return -self.__second_channel.get_conversion_volts() #minus because of swapped CH2+ and CH2- in rev1.1 Shield