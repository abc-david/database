"""
MODULE: services/database/decorators.py
PURPOSE: Provides decorators for async database operations
CLASSES:
    - None
FUNCTIONS:
    - with_db_connection: Decorator for injecting database connections
DEPENDENCIES:
    - functools: For decorator support
    - inspect: For function signature inspection
    - db_connector: For database connectivity

This module provides decorators for simplifying database operations in async
functions, particularly for use in Celery tasks. The decorators handle connection
lifecycle management and transaction handling automatically.
"""

import functools
import inspect
import logging
from typing import Callable, Any, Awaitable, TypeVar

from services.database.db_connector import DBConnector

logger = logging.getLogger(__name__)

T = TypeVar('T')  # Return type of the decorated function

def with_db_connection(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    """
    Async decorator that provides a database connection to a coroutine function.
    
    This decorator:
    1. Automatically acquires a database connection from the pool
    2. Manages the connection lifecycle (release back to pool)
    3. Provides transaction support (commit on success, rollback on failure)
    4. Works with both instance methods and standalone functions
    
    Usage:
        @with_db_connection
        async def my_db_function(conn, arg1, arg2):
            # The conn parameter is injected by the decorator
            result = await conn.execute("SELECT * FROM users WHERE id = $1", (arg1,))
            return result
            
        @with_db_connection
        async def my_method(self, conn, arg1):
            # Works with instance methods too
            return await conn.execute(...)
    
    Args:
        func: The async function to decorate
        
    Returns:
        Decorated function with automatic connection handling
        
    Raises:
        Any exceptions from the decorated function
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Determine if this is a method call (instance method)
        is_method = args and not inspect.isclass(args[0]) and hasattr(args[0], func.__name__)
        
        # Create the connector and get a connection
        connector = DBConnector()
        
        try:
            # Use the transaction context manager to handle connection lifecycle
            async with connector.transaction() as conn:
                # Call the wrapped function with the connection as first argument
                # For methods, self is args[0], so insert connection as second arg
                if is_method:
                    result = await func(args[0], conn, *args[1:], **kwargs)
                else:
                    result = await func(conn, *args, **kwargs)
                return result
        except Exception as e:
            # Log the error (transaction rollback is handled by the context manager)
            logger.error(f"Database error in {func.__name__}: {str(e)}")
            raise
        finally:
            # Close the connector to ensure proper cleanup
            await connector.close()
    
    return wrapper 