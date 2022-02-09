import logging

def logging_data():
    log = logging.getLogger('urllib3')  
    log.setLevel(logging.DEBUG) 
    fh = logging.FileHandler("requests.log")
    log.addHandler(fh)
