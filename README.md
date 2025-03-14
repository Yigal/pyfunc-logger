# PyFunc Logger

[![PyPI version](https://img.shields.io/pypi/v/pyfunc_logger.svg)](https://pypi.org/project/pyfunc-logger/)
[![GitHub](https://img.shields.io/github/license/Yigal/pyfunc-logger)](https://github.com/Yigal/pyfunc-logger)

A lightweight, thread-safe function call logger with precise timing for Python.

## Features

- **Function Call Tracing**: Track function entry and exit points with microsecond-precision timestamps
- **Execution Time Measurement**: Accurately measure function execution time in milliseconds
- **Argument Logging**: Record function argument types and values
- **Return Value Capture**: Log function return values
- **Exception Tracking**: Capture exceptions thrown by functions
- **CSV Output**: Thread-safe logging to CSV for easy analysis
- **Minimal Overhead**: Designed to have minimal impact on function performance
- **No Dependencies**: Pure Python with no external dependencies

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install pyfunc_logger
```

### Option 2: Install from GitHub

```bash
pip install git+https://github.com/Yigal/pyfunc-logger.git
```

### Option 3: Manual Installation

Simply copy the `pyfunc_logger` directory to your project.

## Basic Usage

```python
from pyfunc_logger import log_function

# Basic usage - just add the decorator
@log_function
def my_function(arg1, arg2):
    return arg1 + arg2

# Call the function normally
result = my_function(5, 10)
```

## Configuration Options

The `@log_function` decorator supports several configuration options:

```python
# Custom log directory
@log_function(log_dir="my_custom_logs")
def function_a():
    pass

# Limit number of arguments to log
@log_function(max_arg_count=3)
def function_b(a, b, c, d, e):  # Only a, b, c will be logged
    pass

# Set maximum length for logged values
@log_function(truncate_length=50)
def function_c(large_data):
    pass
```

## Accessing the Logger

You can access the logger instance to get the log file path:

```python
from pyfunc_logger import get_logger

logger = get_logger()
print(f"Logs are being written to: {logger.log_file}")
```

## Advanced Usage

### Custom Logger Configuration

```python
from pyfunc_logger import get_logger

# Configure a custom logger
logger = get_logger(
    log_dir="debug/logs",
    max_arg_count=5,
    truncate_length=200
)

# All subsequent @log_function calls will use this configuration
```

### Analyzing Logs

The package includes an example script for analyzing logs:

```bash
python examples/analyze_logs.py
```

This script shows function call statistics including:
- Call counts
- Min/max/average execution times
- Error rates
- Potential bottlenecks

## Log File Format

The CSV log file contains the following columns:

- `call_id`: Unique identifier for matching entry/exit pairs
- `function_name`: Name of the called function
- `relative_folder`: Folder containing the source file
- `file_name`: File containing the function
- `entry_timestamp`: When the function was entered (ISO format with microseconds)
- `exit_timestamp`: When the function exited (only present in exit records)
- `duration_ms`: Execution time in milliseconds (only present in exit records)
- `is_start`: Boolean indicating if this is an entry (True) or exit (False) record
- `arg1_type` through `argN_type`: Type of each argument
- `arg1_value` through `argN_value`: Value of each argument
- `return_type`: Type of the return value (only in exit records)
- `return_value`: Value returned by the function (only in exit records)

## Examples

See the `examples` directory for complete examples:

- `basic_example.py`: Demonstrates basic usage
- `analyze_logs.py`: Shows how to analyze log files

## Performance Considerations

The logger is designed to be lightweight, but logging does introduce some overhead. For extremely performance-sensitive code, consider:

1. Only logging the specific functions you need to measure
2. Using a custom `log_dir` parameter to separate logs from different parts of your application
3. Setting appropriate `max_arg_count` and `truncate_length` to limit log file size

## Thread Safety

The logger is thread-safe and can be used in multithreaded applications without issues.

## License

MIT
