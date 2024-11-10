logging-utils
===============

A simple, flexible logging utility for Python that enables easy configuration of both console and file logging. This package supports custom log levels, file rotation, and timezone-aware timestamps for streamlined logging in various environments.

Features
--------

*   Configurable logging for both console and file outputs
    
*   Rotating log files based on file size
    
*   Automatic timezone handling based on the TZ environment variable
    
*   Fully customizable log levels and formats

Installation
------------

```bash
pip install logging-by-oriash
```

Usage
-----

To start logging with custom settings, import and use the `setup_logger` function.

### Basic Example

```python
from logging_utils import setup_logger

logger = setup_logger(__name__)  # or use any other name
logger.info("This is an info message.")
logger.error("This is an error message.")
```

Output:
```
2024-11-07 12:34:56,789 - __main__ - INFO [example.py:10] - This is an info message.
2024-11-07 12:34:56,790 - __main__ - ERROR [example.py:11] - This is an error message.
```

### Advanced Configuration

The `setup_logger` function allows you to customize log levels, formats, and file-based logging options.

```python
import logging

from logging_utils import setup_logger, LogFileConfig

logger = setup_logger(
    name=__name__,
    log_level=logging.DEBUG,
    log_format="%(asctime)s - %(levelname)s - %(message)s",
    enable_log_file=True,
    log_file_config=LogFileConfig(
        log_file_level=logging.WARNING,
        log_filename="custom.log",
        max_bytes=100_000,
        backup_count=3
    )
)

logger.debug("This is a debug message.")
logger.warning("This is a warning message.")
```

Output:
```
2024-11-07 12:34:56,789 - DEBUG - This is a debug message.
2024-11-07 12:34:56,790 - WARNING - This is a warning message.
```

Configuration Options
---------------------

### `setup_logger` Parameters

*   **name** (str): Name of the logger instance.
    
*   **log_level** (int | str): Log level for the logger. Defaults to the LOG_LEVEL environment variable or logging.INFO.
    
*   **log_format** (str): Format for log messages. Defaults to DEFAULT_LOG_FORMAT.
    
*   **enable_log_file** (bool): Enables file logging if set to True. Defaults to False.
    
*   **log_file_config** (LogFileConfig): Configuration object for file logging settings.


### LogFileConfig Options

LogFileConfig is a data class used to specify file-based logging settings:

*   **log_file_level** (int | str | None): Log level for file logging. Defaults to the logger’s level if not set.
    
*   **log_filename** (str): Path to the log file. Defaults to "app.log".
    
*   **max_bytes** (int): Max file size in bytes before rotating. Defaults to 1 MiB.
    
*   **backup_count** (int): Number of backup files to keep after rotation. Defaults to 5.


### Environment Variables

*   **LOG_LEVEL**: Sets the default log level for the logger.
    
*   **TZ**: Specifies the timezone for timestamps in logs (e.g., "Asia/Tokyo").


### Example with Environment Variables

You can also configure the logger using environment variables. For example:

```bash
export LOG_LEVEL=DEBUG
export TZ=Asia/Tokyo
```

This configuration sets the log level to logging.DEBUG and formats timestamps in the Tokyo timezone.

License
-------

This project is licensed under the MIT License. See the LICENSE file for more details.

Contributing
------------

Contributions, issues, and feature requests are welcome! Feel free to check out the issues page or submit a pull request.