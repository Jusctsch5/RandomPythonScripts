import logging

from a.b import b_module

logger = logging.getLogger(__name__)

def a_do():
    logger.info("Hello from A")
    b_module.b_do()