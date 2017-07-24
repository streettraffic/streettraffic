from logtest import app
import logging

# create logger with 'spam_application'
logger = logging.getLogger('logtest')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
file_handler = logging.FileHandler("my.log")
file_handler.setLevel(logging.DEBUG)

# create console handler with a higher log level
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

app.test()

## put this file outside of main_program