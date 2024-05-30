# ou-logger-py

Simple logger for use in Jupyter notebooks.

This package sets up the Pyhton `logger` for immediate use in a Jupyter notebook setting.

Install as: `pip install ou_logger`

Usage:

```python
from ou_logger import logger
```

This will display an information message:

```text
Logger enabled. Set level as: logger.setLevel(LEVEL), where LEVEL is one of: DEBUG, INFO, WARNING, ERROR (default), CRITICAL.
Usage: e.g. logger.error('This is an error message')
```

Logging messages will be displayed at or above the declared logging level. For example:

- `logger(CRITICAL)` will only display `CRITICAL` messages;
- `logger(WARNING)` will display `WARNING`, `ERROR` and `CRITICAL` messages.
