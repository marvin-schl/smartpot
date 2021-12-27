import time
import smbus
import os

class MCP3426:
    def __init__(self, busnumber):
        assert busnumber in [0, 1]
        self.busnumber = busnumber
        self.slave_address = 0x68
        self.smbus = smbus.SMBus(1)

    def _read_ch(self,conf_bits):
        """ read the signal-value of channel a from the MCP3426
            and return the voltage in volt """
        bus.write_byte(0x68, conf_bits)
        data = data = self.smbus.read_i2c_block_data(0x68, 0x00, 2)
        # Convert the data to 12-bits
        raw_adc = (data[0] & 0x0F) * 256 + data[1]
        if raw_adc > 2047:
            raw_adc -= 4095
        return raw_adc

    def read_ch1(self):
        return self._read_ch(0x10)

    def read_ch2(self):
        return self._read_ch(0x30)
