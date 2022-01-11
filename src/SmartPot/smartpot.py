from src.SmartPot.adc import MCP3426
from src.SmartPot.dht import DHT
from src.SmartPot.output import PowerOutputPin
from src import logging_conf_setup
import logging
import configparser

#setup logger for the first time
logging_conf_setup.setup()
#setup config
config = configparser.ConfigParser()
config.read("smartpot.ini")
#setup logger
# get root Logger
log = logging.getLogger()


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
        Reads the value of the light intensity sensor and applies calibration of INI File.
        :return: Light intensity value according to calibration values in INI File.Default
        calibration should return percentage of maximum measureable light intensity value.
        """
        log.info(type(self).__name__ + " - Start light intensity measurement.")

        #get the adc value in volts
        intensity = self.__adc.read_ch2()

        if intensity != -999:
            # calibrate
            scale = float(config["Light"]["scaling"])
            offset = float(config["Light"]["offset"])
            intensity = scale*(intensity - offset)

        #apply saturation if configured
        if "saturation" in config["Light"]:
            saturation = float(config["Light"]["saturation"])
            intensity = intensity if intensity < saturation else saturation

        log.info(type(self).__name__ + " - Light intensity measurement finished at "+str(intensity)+" %.")
        return intensity

    def read_soil_moisture(self):
        """
        Reads the value of the soil moisture sensor.
        :return: relative soil moisture in percent
        """
        log.info(type(self).__name__ + " - Start soil moisture measurement.")

        #get the adc value in volts
        moisture = self.__adc.read_ch1()

        if moisture != -999:
            # calibrate
            scale = float(config["Soil Moisture"]["scaling"])
            offset = float(config["Soil Moisture"]["offset"])
            moisture = scale*(moisture - offset)

        #apply saturation if configured
        if "saturation" in config["Soil Moisture"]:
            saturation = float(config["Soil Moisture"]["saturation"])
            moisture = moisture if moisture < saturation else saturation

        log.info(type(self).__name__ + " - Soil moisture measurement finished at "+str(moisture)+"%.")

        return moisture
