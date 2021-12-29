import RPi.GPIO as GPIO
from threading import Lock
from datetime import datetime
import logging

#setup logger
dt = datetime.today()
logging.basicConfig(filename='smartpot.log',
                    filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.DEBUG)

class PowerOutputPin:

    def __init__(self, pin):
        """
        Creates a new PowerOutputPin. Corresponding to SmartPot RaspberryShield rev 1.1 the Pin can drive up to. Wraps
        the RPi.GPIO module into a threadsafe environment.
        1.5A@12V.

        :param pin: Pin Number (Mode BCM). Check with `sudo gpio readall`.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.__pin = pin
        self.__pwm_on = False
        self.__pwm = None
        self.__lock = Lock()

    @property
    def pin(self):
        """
        Implicit getter for the pin Property
        :return: Pin Number
        """
        return self.__pin

    def on(self):
        """
        Sets this PowerOutputPin high.
        :return:
        """
        logging.debug(type(self).__name__ + " - Acquiring Lock on GPIO " + self.__pin + "(BCM Mode).")
        with self.__lock:
            GPIO.output(self.__pin, GPIO.HIGH)
            logging.debug(type(self).__name__ + " - GPIO " + self.__pin + "(BCM Mode) was set to HIGH.")

    def off(self):
        """
        Sets this PowerOutputPin low.
        :return: None
        """
        logging.debug(type(self).__name__ + " - Acquiring Lock on GPIO " + self.__pin + "(BCM Mode).")
        with self.__lock:
            GPIO.output(self.__pin, GPIO.LOW)
            logging.debug(type(self).__name__ + " - GPIO " + self.__pin + "(BCM Mode) was set to LOW.")

        logging.debug(type(self).__name__ + " - Released Lock on GPIO " + self.__pin + "(BCM Mode).")

    def start_pwm(self, freq, dc):
        """
        Starts a PWM on this PowerOutputPin.

        :param freq: Frequency in Hertz
        :param dc:  Duty Cycle in percent (0 <= dc <= 100.0)
        :return: None
        """
        logging.debug(type(self).__name__ + " - Acquiring Lock on GPIO " + self.__pin + "(BCM Mode).")
        with self.__lock:
            self.__pwm = GPIO.PWM(self.__pin, freq)
            self.__pwm.start(dc)
            logging.debug(type(self).__name__ + " - PWM on GPIO " + self.__pin + "(BCM Mode) started.")

        logging.debug(type(self).__name__ + " - Released Lock on GPIO " + self.__pin + "(BCM Mode).")

    def stop_pwm(self):
        """
        Stops the PWM on this PowerOutputPin.
        :return: True if stopping was successfull. False if no PWM was started yet.
        """
        logging.debug(type(self).__name__ + " - Acquiring Lock on GPIO " + self.__pin + "(BCM Mode).")
        with self.__lock:
            if self.__pwm:
                self.__pwm.stop()
                self.__pwm = None
                ret = True
                logging.debug(type(self).__name__ + " - PWM on GPIO " + self.__pin + "(BCM Mode) stopped.")

            else:
                logging.warning(type(self).__name__ + " - PWM can not be stopped if never started.")
                ret = False
        logging.debug(type(self).__name__ + " - Released Lock on GPIO " + self.__pin + "(BCM Mode).")

        return ret

    def change_freq(self, freq):
        """
        Changes the PWM Frequency of a running PWM.
        :param freq: New Frequency in Hertz.
        :return: True if successfull. False if no PWM was started yet.
        """
        logging.debug(type(self).__name__ + " - Acquiring Lock on GPIO " + self.__pin + "(BCM Mode).")
        with self.__lock:
            if self.__pwm:
                self.__pwm.ChangeFrequency(freq)
                logging.debug(type(self).__name__ + " - Changed PWM frequency on GPIO " + self.__pin + "(BCM Mode) to" + str(freq) + "Hz.")
                ret = True
            else:
                logging.warning(type(self).__name__ + " - Frequency cannot be changend if no PWM is started")
                ret = False
        logging.debug(type(self).__name__ + " - Released Lock on GPIO " + self.__pin + "(BCM Mode).")

        return ret

    def change_dc(self, dc):
        """
        Changes the Duty Cycle of a Running PWM
        :param dc: New Duty Cycle in percent (0 <= dc <= 100.0)
        :return: True if successfull. False if no PWM was started yet.
        """
        #no logging in dc change, could possibly overload logfile
        #logging.debug(type(self).__name__ + " - Acquiring Lock on GPIO " + self.__pin + "(BCM Mode).")
        with self.__lock:
            if self.__pwm:
                self.__pwm.ChangeDutyCycle(dc)
                #logging.debug(type(self).__name__ + " - Changed PWM duty cycle on GPIO " + self.__pin + "(BCM Mode) to" + str(dc) + "%.")
                ret = True
            else:
                logging.warning(type(self).__name__ + " - Duty Cycle cannot be changend if no PWM is started")
                ret = False
        #logging.debug(type(self).__name__ + " - Released Lock on GPIO " + self.__pin + "(BCM Mode).")
        return ret