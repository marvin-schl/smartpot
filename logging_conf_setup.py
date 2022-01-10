import logging
import configparser
import sys
from threading import Lock

lock = Lock()

def get_setup():
    lock.acquire()
    #setup config
    config = configparser.ConfigParser()
    config.read("smartpot.ini")
    levels = {"DEBUG": logging.DEBUG, "ERROR":logging.ERROR, "WARN":logging.WARN, "INFO":logging.INFO}
    #setup logger
    # create logger with
    log = logging.getLogger()
    log.setLevel(levels.get(config["Logging"]["level"], "DEBUG"))

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # create file handler which logs even debug messages
    if config["Logging"]["stdout"] == "1":
        # create console handler with a higher log level
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(levels.get(config["Logging"]["level"], "DEBUG"))
        ch.setFormatter(formatter)
        log.addHandler(ch)
    lock.release()
    return log, config