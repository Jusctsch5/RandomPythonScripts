
import logging


logger = logging.getLogger("a.b.f.f_module")
logger.setLevel(logging.INFO)
def f_do():
    logger.info("Hello from F")