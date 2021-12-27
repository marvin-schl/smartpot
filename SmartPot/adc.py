import time
import smbus
import os

class MCP3426:
    def __init__(self, busnumber):
        assert busnumber in [0, 1]
        self.busnumber = busnumber
        self.slave_address = 0x68
        self.smbus = smbus.SMBus(1)

    def _swap_bytes(self, word):
        """ swap the two bytes of the given word
            example: word = 0xABCD -> return 0xCDAB """
        return ((word << 8) & 0xFF00) + (word >> 8)

    def _two_complement(self, word):
        """ convert the given word in two's complement to an integer with
        sign """
        if (word >= 0x8000):
            return -((0xFFFF - word) + 1)
        else:
            return word

    def _read_ch(self,channel):
        """ read the signal-value of channel a from the MCP3426
            and return the voltage in volt """
        rdwo = self.smbus.read_word_data(self.slave_address, channel)
        word = self._swap_bytes(rdwo)
        voltage = self._two_complement(word)
        return voltage / 1000

    def read_ch1(self):
        self.smbus .write_byte(0x68, 0x10)
        return self._read_ch(0x00)

    def read_ch2(self):
        self.smbus .write_byte(0x68, 0x30)
        return self._read_ch(0x00)
