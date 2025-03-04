#!/usr/bin/env python3
"""
Basic example demonstrating usage of the pyfunc_logger package
"""

import os
import sys
import time

# Add parent directory to path for importing pyfunc_logger
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the function logger
from pyfunc_logger import log_function, get_logger


# Simple examples with different decorators
@log_function
def add(a, b):
    """Simple addition function"""
    return a + b


@log_function(log_dir="custom_logs")
def multiply(a, b):
    """Simple multiplication with custom log directory"""
    return a * b


@log_function(max_arg_count=3)
def concatenate_strings(*args):
    """Concatenate multiple strings"""
    return " ".join(args)


@log_function(truncate_length=10)
def process_large_data(data):
    """Process large data with truncated logging"""
    # Simulate processing by sleeping
    time.sleep(0.5)
    return f"Processed {len(data)} items"


# Example with a nested function call
@log_function
def complex_calculation(x, y, z):
    """Function that calls other logged functions"""
    # Call several other functions
    result1 = add(x, y)
    result2 = multiply(result1, z)
    
    # Simulate more complex processing
    time.sleep(0.3)
    
    return result2 + 10


# Function that might raise an exception
@log_function
def risky_function(divisor):
    """Function that might raise an exception"""
    return 100 / divisor


if __name__ == "__main__":
    # Get logger for displaying info
    logger = get_logger()
    print(f"Function logger initialized. Logs will be saved to: {logger.log_file}")
    
    print("\nRunning example functions...")
    
    # Basic function calls
    add(5, 7)
    multiply(3, 4)
    concatenate_strings("Hello", "World", "Python", "Logging")
    
    # Call with large data
    large_list = [f"item-{i}" for i in range(100)]
    process_large_data(large_list)
    
    # Nested function call
    result = complex_calculation(2, 3, 4)
    print(f"Complex calculation result: {result}")
    
    # Exception handling
    try:
        risky_function(0)
    except ZeroDivisionError:
        print("Caught expected exception from risky_function")
    
    # Good case - no exception
    result = risky_function(2)
    print(f"Safe risky_function result: {result}")
    
    print(f"\nAll function calls have been logged to: {logger.log_file}")
    print("You can open this CSV file to analyze function execution time and arguments.")
