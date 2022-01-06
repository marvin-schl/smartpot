import logging
import time
from datetime import datetime
from threading import Thread

#setup logger
dt = datetime.today()
logging.basicConfig(filename='smartpot.log',
                    filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.DEBUG)

class HysteresisMonitor(Thread):

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
        logging.info("Initiliazing Monitor for "+ name + ".")
        super(HysteresisMonitor, self).__init__()
        self.__getter = getter
        self.__name = name
        self.__thres = thres
        self.__lw_thres = self.__thres if lower_thres == None else lower_thres
        if self.__lw_thres > self.__thres:
            logging.warning(type(self).__name__.__str__() + " - Lower Threshold for Value " + name + " of "
                            + str(self.__lw_thres)+ "is greater than upper threshold of " + str(self.__thres) + ".")
        self.__callback_up_thres = callback_up_thres
        self.__callback_lw_thres = callback_lw_thres
        self.__cycle_time = cycle_time
        self.__running = False
        self.__reported = False
        logging.info(type(self).__name__.__str__() + " - Successfully initilized " + name + " Monitor.")

    def start(self):
        """
        Starts the run() method in a new Thread.
        :return: None
        """
        self.__running = True
        logging.info(type(self).__name__.__str__() + " - Starting Monitor for " + self.__name + " in a new Thread...")
        super().start()

    def stop(self):
        """
        Stops the running Monitor Thread.
        :return: None
        """
        self.__running = False
        logging.info(type(self).__name__.__str__() + " - Stopping Monitor for " + self.__name + "...")


    def run(self, *args, **kwargs):
        """
        Run method which is started in a new thread when calling start() method. To stop the Thread call stop() method.
        :return: None
        """
        #do as long as self.__running is true
        while self.__running:
            val = self.__getter()
            now = datetime.now()

            if val > self.__thres and self.__reported == False:
                # do this if self.__thres is exceeded for the first time, do some logging
                logging.info(type(self).__name__.__str__() + " - Value "+ self.__name + "=" +str(val)+ "passed upper threshold of " + str(self.__thres) + " at " + str(now) +".")
                #call the callback
                self.__callback_up_thres(now, val, self.__thres, self.__name)
                #set reported to True to make sure that the callback is not called every single cycle while val is greater than threshold
                self.__reported = True
            if val < self.__lw_thres and self.__reported == True:
                # do this if a exceed was reported and the val falls bellow lower threshold
                # reset the reported value so next up_threshold exceed will be reported and do some logging
                self.__reported = False
                logging.info(type(self).__name__.__str__() + " - Value "+ self.__name + "=" + str(val) + "passed upper threshold of " + str(self.__lw_thres) + " at " + str(now) +".")
                # if a callback is provided for this case, execute it
                if self.__callback_lw_thres != None:
                    self.__callback_lw_thres(now, val, self.__lw_thres, self.__name)
            # wait the cycle time until next value is retrieved
            time.sleep(self.__cycle_time)
        logging.info(type(self).__name__.__str__() + " - Monitor for " + self.__name + " stopped...")

class TimeBasedMonitor(Thread):

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
        logging.info(type(self).__name__.__str__() + " - Initiliazing Monitor for "+ name + ".")
        super(TimeBasedMonitor, self).__init__()
        self.__getter = getter
        self.__name = name
        self.__callback = callback
        self.__cycle_time = cycle_time
        self.__running = False
        logging.info(type(self).__name__.__str__() + " - Successfully initilized " + name + " Monitor.")

    def start(self):
        """
        Starts the run() method in a new Thread.
        :return: None
        """
        self.__running = True
        logging.info(type(self).__name__.__str__() + " - Starting Monitor for " + self.__name + " in a new Thread...")
        super().start()

    def stop(self):
        """
        Stops the running Monitor Thread.
        :return: None
        """
        self.__running = False
        logging.info(type(self).__name__.__str__() + " - Stopping Monitor for " + self.__name + "...")


    def run(self, *args, **kwargs):
        """
        Run method which is started in a new thread when calling start() method. To stop the Thread call stop() method.
        :return: None
        """
        #do as long as self.__running is true
        while self.__running:
            # get current time and current value
            now = datetime.now()
            val = self.__getter()

            #do some logging and exceute the callback
            logging.info(type(self).__name__.__str__() + " - Read Value for " + self.__name + "="+str(val)+" at "+ str(now)+".")
            self.__callback(now, val, self.__name)

            #wait cycle time until next call
            time.sleep(self.__cycle_time)

        logging.info(type(self).__name__.__str__() + " - Monitor for " + self.__name + " stopped...")

if __name__=="__main__":

    x = 0
    thres = 12

    def get_x():
        return x

    def callback(timestamp, value, threshold, name):
        print("Value "+ name + "=" +str(value)+ "passed threshold of " + str(threshold) + " at " + str(timestamp) +".")

    def callback2(now, val, name):
        print(str(now) + " - " +name+"="+str(val))

    print("Starting Monitors...")
    m = HysteresisMonitor("x", get_x, thres, callback, callback_lw_thres=callback)
    m2 = TimeBasedMonitor("x", get_x, callback2, 1)
    m.start()
    m2.start()


    print("Starting counting up...")
    while x < 14:
        x += 0.3
        time.sleep(0.2)
    print("Starting counting down...")
    while x >= 0:
        x -= 0.3
        time.sleep(0.2)

    m.stop()
    m2.stop()
    m.join()
    m2.join()