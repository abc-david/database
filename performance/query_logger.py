"""
MODULE: services/database/performance/query_logger.py
PURPOSE: Logs and analyzes database queries for performance monitoring
CLASSES:
    - QueryLogger: Logs and analyzes database queries
    - QueryLogEntry: Represents a single query log entry
FUNCTIONS:
    - None
DEPENDENCIES:
    - logging: For operational logging
    - datetime: For timestamp recording
    - typing: For type annotations
    - json: For serialization of query data
    - time: For measuring execution time

This module provides functionality for logging and analyzing database queries
for performance monitoring purposes. It can track query execution time,
parameter values, and other metrics to help identify slow queries and
performance bottlenecks.

The query logger can be used in both development and production environments
to monitor database performance, identify slow queries, and optimize database
interactions. It supports exporting data to various formats for further analysis.

Example usage:
When diagnosing performance issues in a service, the QueryLogger can be used
to track all database interactions, measure execution times, and identify
queries that exceed performance thresholds. This information can be used to
optimize the database schema, indexes, or query patterns to improve overall
system performance.
"""

import logging
import datetime
import time
import json
import statistics
from typing import Dict, Any, Optional, List, Tuple, Union, Set

class QueryLogEntry:
    """
    Represents a single query log entry.
    
    This class stores information about a single database query execution,
    including the SQL query, parameters, execution time, and timestamp.
    """
    
    def __init__(self, query: str, params: Any = None, execution_time: float = 0.0):
        """
        Initialize a query log entry.
        
        Args:
            query: SQL query string
            params: Query parameters
            execution_time: Query execution time in milliseconds
        """
        self.query = query
        self.params = params
        self.execution_time = execution_time
        self.timestamp = datetime.datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the query log entry to a dictionary.
        
        Returns:
            Dictionary representation of the log entry
        """
        return {
            "query": self.query,
            "params": self.params,
            "execution_time": self.execution_time,
            "timestamp": self.timestamp.isoformat()
        }
    
    def __str__(self) -> str:
        """
        Convert the query log entry to a string.
        
        Returns:
            String representation of the log entry
        """
        return f"Query: {self.query}\nParams: {self.params}\nExecution Time: {self.execution_time:.2f}ms\nTimestamp: {self.timestamp.isoformat()}"

class QueryLogger:
    """
    Logs and analyzes database queries.
    
    This class provides functionality for logging and analyzing database queries
    for performance monitoring purposes. It tracks query execution time, parameter
    values, and other metrics to help identify slow queries and performance bottlenecks.
    """
    
    def __init__(self, slow_threshold_ms: float = 100.0):
        """
        Initialize the query logger.
        
        Args:
            slow_threshold_ms: Threshold for slow queries in milliseconds
        """
        # Configure logging
        self.logger = logging.getLogger("query_logger")
        
        # Store initialization parameters
        self.slow_threshold_ms = slow_threshold_ms
        
        # Initialize query log
        self.queries: List[QueryLogEntry] = []
        
        # Track table access statistics
        self.table_access_counts: Dict[str, int] = {}
    
    def log_query(self, query: str, params: Any = None, execution_time: Optional[float] = None) -> None:
        """
        Log a database query.
        
        Args:
            query: SQL query string
            params: Query parameters
            execution_time: Query execution time in milliseconds (measured if None)
        """
        # Convert execution time to milliseconds if provided
        if execution_time is not None:
            execution_time_ms = execution_time
        else:
            execution_time_ms = 0.0
        
        # Create and store the log entry
        entry = QueryLogEntry(query, params, execution_time_ms)
        self.queries.append(entry)
        
        # Update table access statistics
        self._update_table_access_stats(query)
        
        # Log slow queries
        if execution_time_ms > self.slow_threshold_ms:
            self.logger.warning(f"Slow query detected ({execution_time_ms:.2f}ms): {query}")
    
    def _update_table_access_stats(self, query: str) -> None:
        """
        Update table access statistics based on the query.
        
        Args:
            query: SQL query string
        """
        # This is a simplified implementation - real implementation would use SQL parsing
        import re
        
        # Normalize the query (remove extra whitespace, make lowercase)
        normalized_query = " ".join(query.split()).lower()
        
        # Extract table names from various query types
        tables = set()
        
        # Extract from SELECT queries
        select_tables = re.findall(r'from\s+([a-zA-Z0-9_\.]+)', normalized_query)
        tables.update(select_tables)
        
        # Extract from INSERT queries
        insert_tables = re.findall(r'insert\s+into\s+([a-zA-Z0-9_\.]+)', normalized_query)
        tables.update(insert_tables)
        
        # Extract from UPDATE queries
        update_tables = re.findall(r'update\s+([a-zA-Z0-9_\.]+)', normalized_query)
        tables.update(update_tables)
        
        # Extract from DELETE queries
        delete_tables = re.findall(r'delete\s+from\s+([a-zA-Z0-9_\.]+)', normalized_query)
        tables.update(delete_tables)
        
        # Update access counts
        for table in tables:
            if table in self.table_access_counts:
                self.table_access_counts[table] += 1
            else:
                self.table_access_counts[table] = 1
    
    def get_slow_queries(self, threshold_ms: Optional[float] = None) -> List[QueryLogEntry]:
        """
        Get queries that exceeded the execution time threshold.
        
        Args:
            threshold_ms: Threshold for slow queries in milliseconds (default: self.slow_threshold_ms)
            
        Returns:
            List of slow query log entries
        """
        # Use default threshold if none provided
        if threshold_ms is None:
            threshold_ms = self.slow_threshold_ms
        
        # Filter queries by execution time
        return [entry for entry in self.queries if entry.execution_time > threshold_ms]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get query statistics.
        
        Returns:
            Dictionary with query statistics
        """
        # Handle empty query log
        if not self.queries:
            return {
                "count": 0,
                "table_access": {},
                "performance": {
                    "avg_time": 0,
                    "min_time": 0,
                    "max_time": 0,
                    "total_time": 0,
                    "median_time": 0,
                    "p95_time": 0
                }
            }
        
        # Extract execution times
        times = [entry.execution_time for entry in self.queries]
        
        # Sort times for percentile calculations
        sorted_times = sorted(times)
        
        # Calculate p95 (95th percentile)
        p95_index = int(len(sorted_times) * 0.95)
        p95_time = sorted_times[p95_index] if p95_index < len(sorted_times) else sorted_times[-1]
        
        # Create statistics dictionary
        return {
            "count": len(times),
            "table_access": self.table_access_counts,
            "performance": {
                "avg_time": sum(times) / len(times),
                "min_time": min(times),
                "max_time": max(times),
                "total_time": sum(times),
                "median_time": statistics.median(times) if len(times) > 0 else 0,
                "p95_time": p95_time
            },
            "slow_query_count": len(self.get_slow_queries())
        }
    
    def export_to_json(self, filepath: str) -> None:
        """
        Export query log to a JSON file.
        
        Args:
            filepath: Path to the output file
        """
        # Convert queries to dictionaries
        data = {
            "queries": [entry.to_dict() for entry in self.queries],
            "stats": self.get_stats()
        }
        
        # Write to file
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.logger.info(f"Exported query log to {filepath}")
    
    def export_to_csv(self, filepath: str) -> None:
        """
        Export query log to a CSV file.
        
        Args:
            filepath: Path to the output file
        """
        import csv
        
        # Write to file
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(["Timestamp", "Query", "Parameters", "Execution Time (ms)"])
            
            # Write data
            for entry in self.queries:
                writer.writerow([
                    entry.timestamp.isoformat(),
                    entry.query,
                    str(entry.params),
                    entry.execution_time
                ])
        
        self.logger.info(f"Exported query log to {filepath}")
    
    def print_summary(self) -> None:
        """
        Print a summary of query statistics to the console.
        """
        stats = self.get_stats()
        
        print("===== Database Query Summary =====")
        print(f"Total Queries: {stats['count']}")
        
        if stats['count'] > 0:
            perf = stats['performance']
            print(f"Total Execution Time: {perf['total_time']:.2f}ms")
            print(f"Average Execution Time: {perf['avg_time']:.2f}ms")
            print(f"Median Execution Time: {perf['median_time']:.2f}ms")
            print(f"95th Percentile Time: {perf['p95_time']:.2f}ms")
            print(f"Min/Max Time: {perf['min_time']:.2f}ms / {perf['max_time']:.2f}ms")
            print(f"Slow Queries: {stats['slow_query_count']} (>{self.slow_threshold_ms}ms)")
            
            print("\nTable Access:")
            for table, count in sorted(stats['table_access'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {table}: {count}")
            
            if stats['slow_query_count'] > 0:
                print("\nSlow Queries:")
                for entry in self.get_slow_queries():
                    print(f"  - {entry.execution_time:.2f}ms: {entry.query}")
        
        print("==================================")

# Create a decorator for timing queries
def time_query(func):
    """
    Decorator to time database queries and log them.
    
    This decorator measures the execution time of a database query function
    and logs it to a QueryLogger instance. The QueryLogger instance should be
    available as self.query_logger in the decorated class.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(self, *args, **kwargs):
        # Ensure we have a query logger
        if not hasattr(self, 'query_logger'):
            self.query_logger = QueryLogger()
        
        # Get the query (assumes first argument is the query)
        query = args[0] if args else kwargs.get('query')
        params = args[1] if len(args) > 1 else kwargs.get('params')
        
        # Start timing
        start_time = time.time()
        
        # Call the original function
        result = func(self, *args, **kwargs)
        
        # Calculate execution time in milliseconds
        execution_time = (time.time() - start_time) * 1000
        
        # Log the query
        self.query_logger.log_query(query, params, execution_time)
        
        return result
    
    return wrapper 