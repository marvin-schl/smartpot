from SmartPot.adc import MCP3426
from SmartPot.dht import DHT
from SmartPot.PowerOutputPin import PowerOutputPin



class SmartPot:
    X5 = 13
    X6 = 16
    X7 = 26

    def __init__(self):
        power_pins = [SmartPot.X5, SmartPot.X6, SmartPot.X7]
        dht_pin = 21
        adc_bus = 1

        self.__adc = MCP3426(adc_bus)
        self.__dht = DHT(dht_pin)
        self.__power_pins = {}
        for pin in power_pins:
            self.__power_pins[pin] = PowerOutputPin(pin)

    def output_on(self, pin):
        self.__power_pins[pin].on()

    def output_off(self, pin):
        return self.__power_pins[pin].off()

    def output_pwm_on(self, pin, freq, dc):
        return self.__power_pins[pin].start_pwm(freq, dc)

    def output_pwm_off(self, pin):
        return self.__power_pins[pin].stop_pwm()

    def output_pwm_change_freq(self, pin, freq):
        return self.__power_pins[pin].change_freq(freq)

    def output_pwm_change_dc(self, pin, dc):
        return  self.__power_pins[pin].change_dc(dc)

    def read_temperature(self):
        return self.__dht.read_temperature()

    def read_humidity(self):
        return self.__dht.read_humidity()

    def read_light_intensity(self):
        adc_value = self.__adc.read_ch2()

        #TODO: calculate an appropriate intensity value
        intensity = adc_value

        return intensity

    def read_soil_moisture(self):
        adc_value = self.__adc.read_ch1()

        # TODO: calculate an appropriate moisture value
        moisture = adc_value

        return moisture

