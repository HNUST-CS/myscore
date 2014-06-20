
import logging  
import sys  

def getloger():
    logger = logging.getLogger("endlesscode")  
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%Y %b %d %H:%M:%S',)  
    
    log_file_handler = logging.FileHandler("myscore.log")  
    log_file_handler.setFormatter(file_formatter)  
    logger.addHandler(log_file_handler)  
    
    stream_handler = logging.StreamHandler(sys.stdout)  
    stdout_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%H:%M:%S',)  
    stream_handler.setFormatter(stdout_formatter)
    logger.addHandler(stream_handler)  
    logger.setLevel(logging.DEBUG)
    return logger
