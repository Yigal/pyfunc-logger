#!/usr/bin/env python3
"""
Example script for analyzing function logs generated by pyfunc_logger
"""

import os
import sys
import csv
import datetime
from collections import defaultdict

# Add parent directory to path for importing pyfunc_logger
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import just for getting the default log directory
from pyfunc_logger import get_logger


def find_latest_log_file(log_dir=None):
    """Find the most recent log file in the specified directory"""
    # Use default log directory if none provided
    if log_dir is None:
        log_dir = os.path.join(os.getcwd(), "func_logs")
    
    if not os.path.exists(log_dir):
        print(f"Log directory not found: {log_dir}")
        return None
    
    log_files = [f for f in os.listdir(log_dir) if f.startswith('func_log_') and f.endswith('.csv')]
    
    if not log_files:
        print(f"No log files found in {log_dir}")
        return None
    
    # Sort by modification time (newest first)
    log_files.sort(key=lambda f: os.path.getmtime(os.path.join(log_dir, f)), reverse=True)
    return os.path.join(log_dir, log_files[0])


def analyze_log_file(log_file):
    """Analyze a function log file"""
    if not os.path.exists(log_file):
        print(f"Log file not found: {log_file}")
        return
    
    print(f"Analyzing log file: {log_file}")
    
    # Read the log file
    records = []
    with open(log_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    
    # Match entry and exit records
    call_groups = {}
    for record in records:
        call_id = record['call_id']
        if call_id not in call_groups:
            call_groups[call_id] = []
        call_groups[call_id].append(record)
    
    # Analyze function calls
    function_stats = defaultdict(list)
    total_calls = 0
    successful_calls = 0
    errored_calls = 0
    
    for call_id, call_records in call_groups.items():
        if len(call_records) != 2:
            continue
        
        # Identify entry and exit records
        entry_record = None
        exit_record = None
        for record in call_records:
            if record['is_start'] == 'True':
                entry_record = record
            else:
                exit_record = record
        
        if not entry_record or not exit_record:
            continue
        
        total_calls += 1
        function_name = entry_record['function_name']
        
        # Check if function errored
        has_error = 'Exception:' in str(exit_record['return_value'])
        if has_error:
            errored_calls += 1
        else:
            successful_calls += 1
        
        # Parse duration
        try:
            duration_ms = float(exit_record['duration_ms'])
            function_stats[function_name].append({
                'duration_ms': duration_ms,
                'has_error': has_error,
                'entry_time': entry_record['entry_timestamp'],
                'exit_time': exit_record['exit_timestamp']
            })
        except (ValueError, KeyError):
            pass
    
    # Print summary statistics
    print(f"\nSUMMARY STATISTICS:")
    print(f"Total function calls: {total_calls}")
    print(f"Successful calls: {successful_calls}")
    print(f"Errored calls: {errored_calls}")
    
    print("\nFUNCTION TIMING ANALYSIS:")
    print(f"{'Function Name':<25} {'Calls':<8} {'Min (ms)':<10} {'Max (ms)':<10} {'Avg (ms)':<10} {'Errors':<8}")
    print("-" * 75)
    
    for function_name, calls in sorted(function_stats.items()):
        durations = [call['duration_ms'] for call in calls]
        errors = sum(1 for call in calls if call['has_error'])
        
        if durations:
            min_duration = min(durations)
            max_duration = max(durations)
            avg_duration = sum(durations) / len(durations)
            
            print(f"{function_name:<25} {len(calls):<8} {min_duration:<10.2f} {max_duration:<10.2f} {avg_duration:<10.2f} {errors:<8}")
    
    # Identify potential bottlenecks
    print("\nPOTENTIAL BOTTLENECKS:")
    for function_name, calls in sorted(function_stats.items(), 
                                      key=lambda x: max([c['duration_ms'] for c in x[1]]), 
                                      reverse=True)[:3]:
        durations = [call['duration_ms'] for call in calls]
        if durations and max(durations) > 100:  # Only show functions that take > 100ms
            print(f"- {function_name}: max time {max(durations):.2f}ms, called {len(calls)} times")


if __name__ == "__main__":
    # Find the latest log file
    latest_log = find_latest_log_file()
    
    if latest_log:
        analyze_log_file(latest_log)
    else:
        # Try to get a log file from the example
        logger = get_logger()
        if os.path.exists(logger.log_file):
            analyze_log_file(logger.log_file)
        else:
            print("No log files found. Run basic_example.py first to generate log data.")
