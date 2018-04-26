import logging

log_format = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
logging.basicConfig(filename='logger.log', level=logging.DEBUG, format=log_format)
