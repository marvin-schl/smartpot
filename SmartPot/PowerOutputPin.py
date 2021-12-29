import RPi.GPIO as GPIO
from threading import Lock


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
        with self.__lock:
            GPIO.output(self.__pin, GPIO.HIGH)

    def off(self):
        """
        Sets this PowerOutputPin low.
        :return: None
        """
        with self.__lock:
            GPIO.output(self.__pin, GPIO.LOW)


    def start_pwm(self, freq, dc):
        """
        Starts a PWM on this PowerOutputPin

        :param freq: Frequency in Hertz
        :param dc:  Duty Cycle in percent (0 <= dc <= 100.0)
        :return: None
        """
        with self.__lock
            self.__pwm = GPIO.PWM(self.__pin, freq)
            self.__pwm.start(dc)

    def stop_pwm(self):
        """
        Stops the PWM on this PowerOutputPin.
        :return: True if stopping was successfull. False if no PWM was started yet.
        """
        with self.__lock:
            if self.__pwm:
                self.__pwm.stop()
                self.__pwm = None
                ret = True
            else:
                ret = False
        return ret

    def change_freq(self, freq):
        """
        Changes the PWM Frequency of a running PWM.
        :param freq: New Frequency in Hertz.
        :return: True if successfull. False if no PWM was started yet.
        """
        with self.__lock:
            if self.__pwm:
                self.__pwm.ChangeFrequency(freq)
                ret = True
            else:
                ret = False
        return ret

    def change_dc(self, dc):
        """
        Changes the Duty Cycle of a Running PWM
        :param dc: New Duty Cycle in percent (0 <= dc <= 100.0)
        :return: True if successfull. False if no PWM was started yet.
        """
        with self.__lock:
            if self.__pwm:
                self.__pwm.ChangeDutyCycle(dc)
                ret = True
            else:
                ret = False
        return ret