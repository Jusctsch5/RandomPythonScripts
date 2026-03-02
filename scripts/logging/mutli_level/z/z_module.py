import logging

from a import a_module
from a.b import b_module
from a.b.c import c_module
from a.b.d import d_module

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def z_do():
    logger.info("Hello from Z")
    a_module.a_do()
    b_module.b_do()
    c_module.c_do()
    d_module.d_do()