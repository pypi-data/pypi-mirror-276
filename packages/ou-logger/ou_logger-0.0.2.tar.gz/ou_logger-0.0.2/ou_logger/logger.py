import logging
import re
from IPython.display import display, Javascript

# Default logging level
DEFAULT = logging.ERROR

# Define a custom logging handler that speaks the log messages using browser TTS
class BrowserTTSHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        # Use JavaScript to speak the message in the browser
        display(
            Javascript(f'speechSynthesis.speak(new SpeechSynthesisUtterance("{msg}"))')
        )


# Create a logger object
logger = logging.getLogger("ou_logger")

# Remove all handlers associated with the logger object
if logger.hasHandlers():
    logger.handlers.clear()

print(
    "Logger enabled. Set level as: logger.setLevel(LEVEL), where LEVEL is one of: DEBUG, INFO, WARNING, ERROR (default), CRITICAL.\nSet text and/or text-to-speech output: set_handler('text, tts')\nUsage: e.g. logger.error('This is an error message')"
)

def set_handler(typ="text"):
    """Set handler for logger."""
    # By default we expect a string
    if type(typ)==str:
        typ = re.split(r"[ :,;]+", typ)
    # If passed a list, it should also work...
    typ = [t.strip().lower() for t in typ]

    # Remove all handlers associated with the logger object
    if logger.hasHandlers():
        logger.handlers.clear()
    for t in typ:
        if t=="text":
            print("Using text handler for logger...")
            # Create a handler to display logs in the notebook
            handler = logging.StreamHandler()
            # Set the handler level
            handler.setLevel(DEFAULT)
            # Create a formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            # Add the handler to the logger
            logger.addHandler(handler)

        if t=="tts":
            print("Using tts handler for logger...")
            # Create a TTS handler
            tts_handler = BrowserTTSHandler()
            tts_handler.setLevel(DEFAULT)
            # Add the TTS handler to the logger
            logger.addHandler(tts_handler)

set_handler("text")

# Expose the logger for external use
__all__ = ["logger", "set_handler"]
