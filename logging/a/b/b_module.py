import logging
from a.b.c import c_module
from a.b.d import d_module

logger = logging.getLogger(__name__)

def b_do():
    logger.info("Hello from B")
    c_module.c_do()
    d_module.d_do()