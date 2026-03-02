import logging
from a.b.e import e_module
from a.b.f import f_module

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def c_do():
    logger.info("Hello from C")
    e_module.e_do()
    f_module.f_do()
