import logging
from a import a_module
from z import z_module

logger = logging.getLogger(__name__)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

logger.info("Main")

a_module.a_do()
z_module.z_do()


def walk_loggers():
    for name, logger in sorted(logging.root.manager.loggerDict.items()):
        if isinstance(logger, logging.Logger):
            indent = '    ' * name.count('.')
            print(f"{indent}{name} (Level: {logging.getLevelName(logger.level)})")

walk_loggers()