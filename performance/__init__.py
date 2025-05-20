"""
MODULE: services/database/performance/__init__.py
PURPOSE: Export classes and functions from the performance package
CLASSES:
    - QueryLogger: For logging and analyzing database queries
    - QueryLogEntry: Represents a single query log entry
FUNCTIONS:
    - time_query: Decorator for timing database queries
DEPENDENCIES:
    - query_logger: Provides query logging and analysis functionality

This module exports the main classes and functions from the performance package,
making them available for importing directly from the package. The package
provides functionality for database performance monitoring, including query
logging, timing, and analysis.

The exported components help identify slow queries, track database usage patterns,
and optimize database interactions for better performance.

Example usage:
from services.database.performance import QueryLogger, time_query

# Create a query logger
logger = QueryLogger(slow_threshold_ms=50.0)

# Use the decorator to automatically log query execution times
class MyDatabaseService:
    def __init__(self):
        self.query_logger = logger
        
    @time_query
    def execute_query(self, query, params=None):
        # Execute the query...
        pass
        
# Print a summary of query performance
logger.print_summary()
"""

from .query_logger import QueryLogger, QueryLogEntry, time_query

__all__ = [
    "QueryLogger",
    "QueryLogEntry",
    "time_query"
] 