"""
MODULE: services/database/utils/connection_helpers.py
PURPOSE: Utility functions for database connections
FUNCTIONS:
    - format_query_params: Format parameters for SQL queries
    - format_db_error: Format database errors for display
    - format_column_name: Format a column name for SQL queries
DEPENDENCIES:
    - logging: For operation logging
    - psycopg2: For error types

This module provides utility functions for working with database connections
and formatting SQL queries.
"""

import logging
import re
from typing import Any, List, Dict, Optional, Union, Tuple

# Import psycopg2 errors for error handling
try:
    import psycopg2
    from psycopg2 import errors as pg_errors
except ImportError:
    # Define dummy error classes if psycopg2 is not available
    class pg_errors:
        class UniqueViolation(Exception): pass
        class ForeignKeyViolation(Exception): pass
        class CheckViolation(Exception): pass
        class NotNullViolation(Exception): pass
        class StringDataRightTruncation(Exception): pass
        class NumericValueOutOfRange(Exception): pass
        class InvalidDatetimeFormat(Exception): pass
        class UndefinedTable(Exception): pass
        class UndefinedColumn(Exception): pass
        class DuplicateTable(Exception): pass
        class DuplicateObject(Exception): pass
        class OperationalError(Exception): pass

# Set up logging
logger = logging.getLogger(__name__)

def format_query_params(params: Any) -> str:
    """
    Format query parameters for logging or display.
    
    Args:
        params: Query parameters (tuple, list, dict, or other)
        
    Returns:
        Formatted string representation of parameters
    """
    if params is None:
        return "None"
        
    if isinstance(params, (tuple, list)):
        return ", ".join(f"'{p}'" if isinstance(p, str) else str(p) for p in params)
    elif isinstance(params, dict):
        return ", ".join(f"{k}='{v}'" if isinstance(v, str) else f"{k}={v}" for k, v in params.items())
    else:
        return str(params)
        
def format_db_error(error: Exception) -> Dict[str, Any]:
    """
    Format a database error into a structured dictionary.
    
    Args:
        error: Database exception
        
    Returns:
        Structured error information
    """
    # Default error info
    error_info = {
        "type": error.__class__.__name__,
        "message": str(error),
        "user_message": "A database error occurred.",
        "code": None,
        "detail": None,
        "hint": None
    }
    
    # Check for psycopg2 errors
    if hasattr(error, "pgcode"):
        error_info["code"] = getattr(error, "pgcode")
        error_info["detail"] = getattr(error, "diag", {}).get("message_detail")
        error_info["hint"] = getattr(error, "diag", {}).get("message_hint")
        
        # Provide user-friendly messages for common errors
        if isinstance(error, pg_errors.UniqueViolation):
            error_info["user_message"] = "A record with the same unique value already exists."
        elif isinstance(error, pg_errors.ForeignKeyViolation):
            error_info["user_message"] = "The operation would violate a foreign key constraint."
        elif isinstance(error, pg_errors.CheckViolation):
            error_info["user_message"] = "The operation would violate a check constraint."
        elif isinstance(error, pg_errors.NotNullViolation):
            error_info["user_message"] = "A required field was missing."
        elif isinstance(error, pg_errors.StringDataRightTruncation):
            error_info["user_message"] = "A text value was too long for its field."
        elif isinstance(error, pg_errors.NumericValueOutOfRange):
            error_info["user_message"] = "A numeric value was out of range for its field."
        elif isinstance(error, pg_errors.InvalidDatetimeFormat):
            error_info["user_message"] = "A date or time value was invalid."
        elif isinstance(error, pg_errors.UndefinedTable):
            error_info["user_message"] = "The requested table does not exist."
        elif isinstance(error, pg_errors.UndefinedColumn):
            error_info["user_message"] = "The requested column does not exist."
        elif isinstance(error, pg_errors.DuplicateTable):
            error_info["user_message"] = "A table with that name already exists."
        elif isinstance(error, pg_errors.DuplicateObject):
            error_info["user_message"] = "An object with that name already exists."
            
    # Log the error
    logger.error(f"Database error: {error_info['type']}: {error_info['message']}")
    
    return error_info
    
def format_column_name(column_name: str) -> str:
    """
    Format a column name for use in SQL queries.
    
    Ensures column names are properly sanitized and quoted.
    
    Args:
        column_name: Column name to format
        
    Returns:
        Formatted column name
    """
    # Remove any quotes that might already be there
    clean_name = re.sub(r'["\']', '', column_name)
    
    # Check if the column name needs quoting (contains special characters or keywords)
    needs_quotes = (
        not clean_name.isalnum() or 
        clean_name.upper() in ["SELECT", "FROM", "WHERE", "JOIN", "GROUP", "ORDER", "BY", "HAVING", "LIMIT", "OFFSET"]
    )
    
    if needs_quotes:
        return f'"{clean_name}"'
    else:
        return clean_name 