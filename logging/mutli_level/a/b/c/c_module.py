import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def c_do():
    logger.info("Hello from C")