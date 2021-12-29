from SmartPot.adc import MCP3426
from SmartPot.dht import DHT
from SmartPot.PowerOutputPin import PowerOutputPin



class SmartPot:
    X4 = 13
    X5 = 19
    X6 = 26

    def __init__(self, dht_type = "DHT11"):
        """
        Creates a new instance of a SmartPot. The implementation is threadsafe.
        :param dht_type: (optional) "DHT11" or "DHT22" depending on the connected DHT sensor. Default Value is "DHT11".
        """
        power_pins = [SmartPot.X4, SmartPot.X5, SmartPot.X6]
        dht_pin = 18
        adc_bus = 1

        self.__adc = MCP3426(adc_bus)
        self.__dht = DHT(dht_pin, dht_type)

        self.__power_pins = {}
        for pin in power_pins:
            self.__power_pins[pin] = PowerOutputPin(pin)

    def output_on(self, pin):
        """
        Sets an power output HIGH
        :param pin: SmartPot.X4, SmartPot.X5 or SmartPot.X6
        :return: None
        """
        self.__power_pins[pin].on()

    def output_off(self, pin):
        """
        Sets an power output LOW
        :param pin:  SmartPot.X4, SmartPot.X5 or SmartPot.X6
        :return: None
        """
        return self.__power_pins[pin].off()

    def output_pwm_on(self, pin, freq, dc):
        """
        Starts a PWM on an power output.
        :param pin: SmartPot.X4, SmartPot.X5 or SmartPot.X6
        :param freq: Frequency in Hertz
        :param dc: Duty Cycle in percent
        :return: None
        """
        return self.__power_pins[pin].start_pwm(freq, dc)

    def output_pwm_off(self, pin):
        """
        Stops a PWM on an power output
        :param pin: SmartPot.X4, SmartPot.X5 or SmartPot.X6
        :return: True if successfull, False if no PWM was started yet
        """
        return self.__power_pins[pin].stop_pwm()

    def output_pwm_change_freq(self, pin, freq):
        """
        Changes PWM Frequency of an power output
        :param pin: SmartPot.X4, SmartPot.X5 or SmartPot.X6
        :param freq: New frequency in Hertz
        :return: True if successfull, False if no PWM was started yet
        """
        return self.__power_pins[pin].change_freq(freq)

    def output_pwm_change_dc(self, pin, dc):
        """
        Changes the duty cycle of an power output
        :param pin: SmartPot.X4, SmartPot.X5 or SmartPot.X6
        :param dc: New duty cycle in percent
        :return: True if successfull, False if no PWM was started yet
        """
        return  self.__power_pins[pin].change_dc(dc)

    def read_temperature(self):
        """
        Reads the temperature of an connected DHT sensor.
        :return: Temperature in degree celsius
        """
        return self.__dht.read_temperature()

    def read_humidity(self):
        """
        Reads the humidity  of an connected DHT sensor.
        :return: relative humidity in percent
        """
        return self.__dht.read_humidity()

    def read_light_intensity(self):
        """
        Reads the value of the light intensity snesor
        :return: currently only returns output voltage of the sensor, in the future return value will be a appropriate
        light intensity value (see TODO)
        """
        #get the adc value in volts
        adc_value = self.__adc.read_ch2()

        #TODO: calculate an appropriate intensity value
        intensity = adc_value

        return intensity

    def read_soil_moisture(self):
        """
        Reads the value of the soil moisture sensor.
        :return: currently only returns output voltage of the sensor, in the future return value will be a appropriate
        moisture value (see TODO)
        """
        #get the adc value in volts
        adc_value = self.__adc.read_ch1()

        # TODO: calculate an appropriate moisture value
        moisture = adc_value

        return moisture