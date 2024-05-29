# Verbose Terminal [![Python](https://img.shields.io/pypi/v/verbose-terminal.svg)](https://pypi.org/project/verbose-terminal/) [![Downloads](https://static.pepy.tech/badge/verbose-terminal)](https://pepy.tech/project/verbose-terminal)

## Description

Verbose Terminal is a Python library that provides a simple and easy-to-use interface for displaying stylish messages in the terminal. It includes predefined styles for log, debug, info, success, warning, error and critical messages, and also has support for logging.

## Requirements

- Python 3.10+

## Installation

You can install the package via pip:

```bash
pip install verbose-terminal
```

## Usage

Import the `console` class from the `verbose_terminal` module and use its methods to print styled messages. The following examples demonstrate how to use the library:

### Basic Usage

```python
from verbose_terminal import console

# Displaying messages with different styles
console.log("This is a plain message.")
console.debug("This is a debug message.")
console.info("Here is some information.")
console.success("Operation completed successfully!")
console.warning("This is a warning message.")
console.error("An error has occurred.")
console.critical("This is a critical message.")
```

## Verbose Flag

By default, the `verbose` flag is set to `True`. This means that the messages will be displayed on the terminal. To not display messages in the terminal, set the `verbose` flag to `False`.

```python
from verbose_terminal import console

# Displaying messages in the terminal
console.log("This message will be displayed.")
console.log("This message will not be displayed.", verbose=False)
```

## Logging

Verbose Terminal can also log all messages to a file, whether they are printed to the terminal or not.

### Enable Logging

To enable logging, use the `enable_logging` method and specify a log file:

```python
from verbose_terminal import console

# Enable logging to 'messages.log'
console.enable_logging('messages.log')
```

### Log flag level

By default, the `log_level` flag is set to `INFO`. Only messages will be recorded: info, success, warning, error and critical, if you want to add the debug and log messages you must pass the `LOG` flag

```python
from verbose_terminal import console

# Enable logging to 'messages.log'
console.enable_logging('messages.log', log_level='LOG')
```

### Disable Logging

To disable logging, use the `disable_logging` method:

```python
from verbose_terminal import console

# Disable logging
console.disable_logging()
```

### View Logs

To view the logs, use the `view_logs` method:

```python
from verbose_terminal import console

# View logs
print(console.view_logs())
```

### Clear Logs

To clear the logs, use the `clear_logs` method:

```python
from verbose_terminal import console

# Clear logs
console.clear_logs()
```

### Save Logs

To save the logs to a file, use the `save_logs` method:

```python
from verbose_terminal import console

# Save logs to 'logs.txt'
console.save_logs('logs.txt')
```

## Running Tests

To run the tests, run the following command:

```bash
pytest
```

This will execute the unit tests and display the styled messages in the terminal, allowing you to visually verify the output.

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push your branch to GitHub.
4. Submit a pull request.

Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for more details.

## Support

Feel free to explore the code and customize the styles as per your requirements. If you encounter any issues or have suggestions for improvements, please open an issue on GitHub.

## Changelog

Please see the [CHANGELOG.md](CHANGELOG.md) file for details on recent changes and releases.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/wipodev/Verbose_Terminal/blob/main/LICENSE) file for more details.

---
