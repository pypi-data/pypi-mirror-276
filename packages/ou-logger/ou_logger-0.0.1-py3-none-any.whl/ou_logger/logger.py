import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

# Create a logger object
logger = logging.getLogger("ou_logger")

# Remove all handlers associated with the logger object
if logger.hasHandlers():
    logger.handlers.clear()

# Create a handler to display logs in the notebook
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

print(
    "Logger enabled. Set level as: logger.setLevel(LEVEL), where LEVEL is one of: DEBUG, INFO, WARNING, ERROR (default), CRITICAL.\nUsage: e.g. logger.error('This is an error message')"
)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Set the handler level
handler.setLevel(logging.ERROR)

# Add the handler to the logger
logger.addHandler(handler)

# Expose the logger for external use
__all__ = ['logger']
