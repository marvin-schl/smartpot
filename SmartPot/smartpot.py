from SmartPot.adc import MCP3426
from SmartPot.dht import DHT
from SmartPot.output import PowerOutputPin
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
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(levels.get(config["Logging"]["level"], "DEBUG"))
    ch.setFormatter(formatter)
    log.addHandler(ch)

class SmartPot:
    """
    This class represents a physical SmartPot rev1.1. It handles the simple functions like controlling single outputs,
    reading temperature, humidity, light intensity and soil moisture values.
    """

    X4 = 13
    X5 = 19
    X6 = 26
    pin_names = {13:"X4",19: "X5" ,26: "X6"}

    def __init__(self, dht_type = "DHT11"):
        """
        Creates a new instance of a SmartPot. The implementation is threadsafe.
        :param dht_type: (optional) "DHT11" or "DHT22" depending on the connected DHT sensor. Default Value is "DHT11".
        """
        power_pins = [SmartPot.X4, SmartPot.X5, SmartPot.X6]
        dht_pin = 18
        adc_bus = 1

        log.info(type(self).__name__ + " - Initializing ADC on Bus Number " + adc_bus.__str__())
        self.__adc = MCP3426(adc_bus)
        log.info(type(self).__name__ + " - Initializing "+dht_type+" on pin "+dht_pin.__str__()+"...")
        self.__dht = DHT(dht_pin, dht_type)

        log.info(type(self).__name__ + " - Initializing PowerOutputPins X4,X5 and X6...")
        self.__power_pins = {}
        for pin in power_pins:
            self.__power_pins[pin] = PowerOutputPin(pin)
        log.info(type(self).__name__ + " - SmartPot initalized")


    def output_on(self, pin):
        """
        Sets an power output HIGH
        :param pin: SmartPot.X4, SmartPot.X5 or SmartPot.X6
        :return: None
        """
        log.info(type(self).__name__ + " - Turning PowertOuput "+ SmartPot.pin_names[pin]+" on.")
        self.__power_pins[pin].on()

    def output_off(self, pin):
        """
        Sets an power output LOW
        :param pin:  SmartPot.X4, SmartPot.X5 or SmartPot.X6
        :return: None
        """
        log.info(type(self).__name__ + " - Turning PowertOuput "+SmartPot.pin_names[pin]+" off.")
        return self.__power_pins[pin].off()

    def output_pwm_on(self, pin, freq, dc):
        """
        Starts a PWM on an power output.
        :param pin: SmartPot.X4, SmartPot.X5 or SmartPot.X6
        :param freq: Frequency in Hertz
        :param dc: Duty Cycle in percent
        :return: None
        """
        log.info(type(self).__name__ + " - Turning PWM at "+SmartPot.pin_names[pin]+" on. f=" +str(freq)+"Hz, dc="+str(dc)+"%")
        return self.__power_pins[pin].start_pwm(freq, dc)

    def output_pwm_off(self, pin):
        """
        Stops a PWM on an power output
        :param pin: SmartPot.X4, SmartPot.X5 or SmartPot.X6
        :return: True if successfull, False if no PWM was started yet
        """
        log.info(type(self).__name__ + " - Turning PWM at "+SmartPot.pin_names[pin]+" off.")
        return self.__power_pins[pin].stop_pwm()

    def output_pwm_change_freq(self, pin, freq):
        """
        Changes PWM Frequency of an power output
        :param pin: SmartPot.X4, SmartPot.X5 or SmartPot.X6
        :param freq: New frequency in Hertz
        :return: True if successfull, False if no PWM was started yet
        """
        log.info(type(self).__name__ + " - Changing  PWM Frequency at "+SmartPot.pin_names[pin]+" to f="+str(freq)+"Hz.")
        return self.__power_pins[pin].change_freq(freq)

    def output_pwm_change_dc(self, pin, dc):
        """
        Changes the duty cycle of an power output
        :param pin: SmartPot.X4, SmartPot.X5 or SmartPot.X6
        :param dc: New duty cycle in percent
        :return: True if successfull, False if no PWM was started yet
        """
        #no dc cycle change logging because -> eventually overloading the logfile
        #log.debug("Changing PWM DC at "+SmartPot.pin_names[pin]+" to dc="+str(dc)+"%.")
        return  self.__power_pins[pin].change_dc(dc)

    def read_temperature(self):
        """
        Reads the temperature of an connected DHT sensor.
        :return: Temperature in degree celsius
        """
        log.info(type(self).__name__ + " - Start temperature measurement.")
        temp = self.__dht.read_temperature()
        log.info(type(self).__name__ + " - Temperature measurement finished at "+str(temp)+"'C.")
        return temp

    def read_humidity(self):
        """
        Reads the humidity  of an connected DHT sensor.
        :return: relative humidity in percent
        """
        log.info(type(self).__name__ + " - Start humidity measurement.")
        hum = self.__dht.read_humidity()
        log.info(type(self).__name__ + " - Humidity measurement finished at "+str(hum)+"%.")
        return hum

    def read_light_intensity(self):
        """
        Reads the value of the light intensity snesor
        :return: Percentage of maximum measurable light intensity.
        """
        log.info(type(self).__name__ + " - Start light intensity measurement.")

        #get the adc value in volts
        adc_value = self.__adc.read_ch2()

        #TODO: calculate an appropriate intensity value
        max_val = 1.8
        intensity = adc_value/max_val * 100 if adc_value < max_val else 100

        log.info(type(self).__name__ + " - Light intensity measurement finished at "+str(intensity)+" %.")
        return intensity

    def read_soil_moisture(self):
        """
        Reads the value of the soil moisture sensor.
        :return: relative soil moisture in percent
        """
        log.info(type(self).__name__ + " - Start soil moisture measurement.")

        #get the adc value in volts
        adc_value = self.__adc.read_ch1()

        # TODO: calculate an appropriate moisture value
        max_val = 1.9
        moisture = adc_value/max_val*100 if adc_value < max_val else 100

        log.info(type(self).__name__ + " - Soil moisture measurement finished at "+str(moisture)+"%.")

        return moisture
