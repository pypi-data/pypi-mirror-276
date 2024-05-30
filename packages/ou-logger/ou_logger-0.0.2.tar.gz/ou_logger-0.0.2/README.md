# ou-logger-py

Simple logger for use in Jupyter notebooks.

This package sets up the Pyhton `logger` for immediate use in a Jupyter notebook setting.

Install as: `pip install ou-logger`

Usage:

```python
# Variously:
from ou_logger import logger
from ou_logger import logger, set_handler
from ou_logger import *
```

Importing the logger will display an information message:

```text
Logger enabled. Set level as: logger.setLevel(LEVEL), where LEVEL is one of: DEBUG, INFO, WARNING, ERROR (default), CRITICAL.
Set text and/or text-to-speech output: set_handler('text, tts')
Usage: e.g. logger.error('This is an error message')
```

Logging messages will be displayed at or above the declared logging level. For example:

- `logger(CRITICAL)` will only display `CRITICAL` messages;
- `logger(WARNING)` will display `WARNING`, `ERROR` and `CRITICAL` messages.

By default, messages will be displayed as text:

![Example of logger message displayed on a pink background as notebook streeamed output](images/logger_text.png)

### Text to speech messages

Logged messages can also be spoken aloud using the browser text-to-speech (TTS) engine.

Enable text and/or TTS output by setting:

```python
set_handler("text")
set_handler("text, tts")
set_handler("tts")
```

## DEVELOPMENT

Build as: `python -m build .`

Push to PyPi as: `twine upload dist/ou_logger*0.0.2*`
