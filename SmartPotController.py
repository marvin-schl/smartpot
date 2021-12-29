import logging
from datetime import datetime

#setup logger
dt = datetime.datetime.today()
logging.basicConfig(filename='logs/'+dt.strftime("%Y%m%d")+'_smartpot.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
