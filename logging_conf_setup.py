import sys
import logging
import configparser

def setup():
    #setup config
    config = configparser.ConfigParser()
    config.read("smartpot.ini")
    levels = {"DEBUG": logging.DEBUG, "ERROR":logging.ERROR, "WARN":logging.WARN, "INFO":logging.INFO}
    #setup logger
    # get root Logger
    log = logging.getLogger()
    log.setLevel(levels.get(config["Logging"]["level"], "DEBUG"))

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # create stream handler if stdout is specified
    if config["Logging"]["stdout"] == "1":
        # create console handler with a higher log level
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(levels.get(config["Logging"]["level"], "DEBUG"))
        ch.setFormatter(formatter)
        log.addHandler(ch)

    #create File Handler if file is specified
    if "file" in config["Logging"]:
        fh = logging.FileHandler(config["Logging"]["file"])
        fh.setLevel(levels.get(config["Logging"]["level"], "DEBUG"))
        fh.setFormatter(formatter)
        log.addHandler(ch)