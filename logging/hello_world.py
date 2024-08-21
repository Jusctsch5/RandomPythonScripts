import logging

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Log "Hello, World!"
logging.info('Hello, World! - with logging module')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("Hello, World! - with instanced logger logger")
