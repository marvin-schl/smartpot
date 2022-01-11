import time
from datetime import datetime
from threading import Thread
from abc import ABC, abstractmethod
import logging
import configparser
#setup config
config = configparser.ConfigParser()
config.read("smartpot.ini")
#setup logger
# get root Logger
log = logging.getLogger()

class Monitor(Thread, ABC):
    """
    Implements a abstract monitor. This class handles every action all monitors have in common. Namely this is the
    retrieving of the monitored value, retrieving a timestamp and waiting the cycle time repeatedly until the stop method
    is called.
    """
    def __init__(self, name, getter, cycle_time):
        """
        Initilizes a new Monitor.
        :param name: A String representation of the value that is monitored. Mainly for logging purposes.
        :param getter: A callable which return value should be the value of the monitored variable.
        :param cycle_time: Time to wait beween retrieving new values in seconds. Default value is 0.1s.
        """
        super().__init__()
        self.__getter = getter
        self.__name = name
        self.__cycle_time = cycle_time
        self.__running = False

    @property
    def running(self):
        return self.__running

    @property
    def name(self):
        return self.__name

    def start(self):
        """
        Starts the run() method in a new Thread.
        :return: None
        """
        self.__running = True
        log.info(type(self).__name__.__str__() + " - Starting Monitor for " + self.__name + " in a new Thread...")
        super().start()

    def stop(self):
        """
        Stops the running Monitor Thread.
        :return: None
        """
        self.__running = False
        log.info(type(self).__name__.__str__() + " - Stopping Monitor for " + self.__name + "...")

    def run(self,*args,**kwargs):
        #do as long as self.__running is true
        while self.__running:
            val = self.__getter()
            now = datetime.now()
            self.handle(val,now)
            # wait the cycle time until next value is retrieved
            time.sleep(self.__cycle_time)
        log.info(type(self).__name__.__str__() + " - Monitor for " + self.__name + " stopped...")

    @abstractmethod
    def handle(self, val, now):
        """
        The specific handling of the monitored value. Has to be implemented by the subclass.
        :param val: Monitored Value
        :param now: Timestamp
        :return:
        """
        pass

class HysteresisMonitor(Monitor):

    def __init__(self,name,getter,thres,callback_up_thres,lower_thres = None,callback_lw_thres = None,cycle_time = 0.1):
        """
        Initilizes a new HysteresisMonitor class. A callback is called by this class as soon as a defined threshold value
        is exceeded. Optionally a second callback can be passed when the monitored value falls below a lower threshold.
        :param name: A String representation of the value that is monitored. Mainly for logging purposes.
        :param getter: A callable which return value should be the value of the monitored variable.
        :param thres: The upper threshold.
        :param callback_up_thres: A callable which is called when getter() > thres.
                                    Signature should be: `callback_up_thres(name, val, thres, timestamp)`
        :param lower_thres: (optionally) A lower threshold value. Default value is equal to thres.
        :param callback_lw_thres: (optionally) A callable which is called when getter() < lower_thres. When not passed nothing is executed.
                                    Signature should be: `callback_lw_thres(name, val, thres, timestamp)`
        :param cycle_time: (optionally) Time to wait beween retrieving new values in seconds. Default value is 0.1s.
        """
        log.info("Initiliazing Monitor for "+ name + ".")
        super().__init__(name, getter, cycle_time)
        self.__thres = thres
        self.__lw_thres = self.__thres if lower_thres == None else lower_thres
        if self.__lw_thres > self.__thres:
            log.warning(type(self).__name__.__str__() + " - Lower Threshold for Value " + self.name + " of "
                            + str(self.__lw_thres)+ "is greater than upper threshold of " + str(self.__thres) + ".")
        self.__callback_up_thres = callback_up_thres
        self.__callback_lw_thres = callback_lw_thres
        self.__reported = False
        log.info(type(self).__name__.__str__() + " - Successfully initilized " + self.name + " Monitor.")


    def handle(self, val, now):
        """
        Hanlde method which is does the actual handling of the monitored value.
        :param val: Monitored Value
        :param now: Timestamp
        :return: None
        """
        if val > self.__thres and self.__reported == False:
            # do this if self.__thres is exceeded for the first time, do some logging
            log.info(type(self).__name__.__str__() + " - Value "+ self.name + "=" +str(val)+ "passed upper threshold of " + str(self.__thres) + " at " + str(now) +".")
            #call the callback
            self.__callback_up_thres(now, val, self.__thres, self.name)
            #set reported to True to make sure that the callback is not called every single cycle while val is greater than threshold
            self.__reported = True
        if val < self.__lw_thres and self.__reported == True:
            # do this if a exceed was reported and the val falls bellow lower threshold
            # reset the reported value so next up_threshold exceed will be reported and do some logging
            self.__reported = False
            log.info(type(self).__name__.__str__() + " - Value "+ self.name + "=" + str(val) + "passed upper threshold of " + str(self.__lw_thres) + " at " + str(now) +".")
            # if a callback is provided for this case, execute in
            if self.__callback_lw_thres != None:
                self.__callback_lw_thres(now, val, self.__lw_thres, self.name)


class TimeBasedMonitor(Monitor):

    def __init__(self, name, getter, callback, cycle_time):
        """
        Initilizes a new TimeBasedMonitor. A TimeBasedMonitor monitors a specific variable by retrieving its value
        in defined time steps.

        :param name: A String representation of the value that is monitored. Mainly for logging purposes.
        :param getter: A callable which return value should be the value of the monitored variable.
        :param callback: A callback functioin which is called every cycle.
                            Signature should be: `callback(name, val, timestamp)`
        :param cycle_time: Time to wait beween retrieving new values in seconds.
        """
        log.info(type(self).__name__.__str__() + " - Initiliazing Monitor for "+ name + ".")
        super().__init__(name, getter, cycle_time)
        self.__callback = callback
        log.info(type(self).__name__.__str__() + " - Successfully initilized " + name + " Monitor.")


    def handle(self, val, now):
        """
        Hanlde method which is does the actual handling of the monitored value.
        :param val: Monitored Value
        :param now: Timestamp
        :return: None
        """
        #do some logging and exceute the callback
        log.info(type(self).__name__.__str__() + " - Read Value for " + self.name + "="+str(val)+" at "+ str(now)+".")
        self.__callback(now, val, self.name)


if __name__=="__main__":

    x = 0
    thres = 12

    def get_x():
        return x

    def callback(timestamp, value, threshold, name):
        print("Value "+ name + "=" +str(value)+ "passed threshold of " + str(threshold) + " at " + str(timestamp) +".")

    def callback2(now, val, name):
        print(str(now) + " - " +name+"="+str(val))

    log.info("Starting Monitors...")
    m = HysteresisMonitor("x", get_x, thres, callback, callback_lw_thres=callback)
    m2 = TimeBasedMonitor("x", get_x, callback2, 1)
    m.start()
    m2.start()


    log.debug("Starting counting up...")
    while x < 14:
        x += 0.3
        time.sleep(0.2)
    log.debug("Starting counting down...")
    while x >= 0:
        x -= 0.3
        time.sleep(0.2)

    m.stop()
    m2.stop()
    m.join()
    m2.join()