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
    """
    """
    def __init__(self,name,getter,thres,callback_up_thres,lower_thres = None,callback_lw_thres = None,cycle_time = 0.1):
        """

        :param name:
        :param getter:
        :param thres:
        :param callback_up_thres:
        :param lower_thres:
        :param callback_lw_thres:
        :param cycle_time:
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

        :return:
        """
        self.__running = True
        logging.info(type(self).__name__.__str__() + " - Starting Monitor for " + self.__name + " in a new Thread...")
        super().start()

    def stop(self):
        """

        :return:
        """
        self.__running = False
        logging.info(type(self).__name__.__str__() + " - Stopping Monitor for " + self.__name + "...")


    def run(self, *args, **kwargs):
        """

        :return:
        """
        while self.__running:
            val = self.__getter()
            now = datetime.now()
            if val > self.__thres and self.__reported == False:
                logging.info(type(self).__name__.__str__() + " - Value "+ self.__name + "=" +str(val)+ "passed upper threshold of " + str(self.__thres) + " at " + str(now) +".")
                self.__callback_up_thres(now, val, self.__thres, self.__name)
                self.__reported = True
            if val < self.__lw_thres and self.__reported == True:
                self.__reported = False
                logging.info(type(self).__name__.__str__() + " - Value "+ self.__name + "=" + str(val) + "passed upper threshold of " + str(self.__lw_thres) + " at " + str(now) +".")
                if self.__callback_lw_thres != None:
                    self.__callback_lw_thres(now, val, self.__lw_thres, self.__name)
            time.sleep(self.__cycle_time)
        logging.info(type(self).__name__.__str__() + " - Monitor for " + self.__name + " stopped...")

class TimeBasedMonitor(Thread):
    """
    """
    def __init__(self, name, getter, callback, cycle_time):
        """

        :param name:
        :param getter:
        :param thres:
        :param callback_up_thres:
        :param lower_thres:
        :param callback_lw_thres:
        :param cycle_time:
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

        :return:
        """
        self.__running = True
        logging.info(type(self).__name__.__str__() + " - Starting Monitor for " + self.__name + " in a new Thread...")
        super().start()

    def stop(self):
        self.__running = False
        logging.info(type(self).__name__.__str__() + " - Stopping Monitor for " + self.__name + "...")


    def run(self, *args, **kwargs):
        while self.__running:
            now = datetime.now()
            val = self.__getter()
            logging.info(type(self).__name__.__str__() + " - Read Value for " + self.__name + "="+str(val)+" at "+ str(now)+".")
            self.__callback(now, val, self.__name)
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