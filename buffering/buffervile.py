
# Configure logging to flush immediately with reasonable formatting.
import logging
import sys


logging.basicConfig(format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def __main__():
    """
    Script logs some things
    """

    logger.info("This is an info message via logger.info")
    logger.warning("This is a warning message via logger.warning")
    logger.error("This is an error message via logger.error")

    print("This is a print statement")


if __name__ == "__main__":
    __main__()
