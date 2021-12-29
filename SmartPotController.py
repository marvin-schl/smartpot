import logging
from datetime import datetime
import threading

#setup logger
dt = datetime.datetime.today()
logging.basicConfig(filename='smartpot.log',
                    filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

class SmartPotController:
    """
    This class implements the high level control of an SmartPot instance. It uses a SmartPot instance and implements
    dependencies between it's inputs and outputs.
    """

    def __init__(self):
        pass

    def tempeature_monitor(self):
        pass

    def humidity_monitor(self):
        pass

    def lightsense_monitor(self):
        pass

    def moisture_monitor(self):
        pass



