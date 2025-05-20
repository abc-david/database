"""
MODULE: services/database/testing/transaction_manager.py
PURPOSE: Provides transaction isolation for database tests
CLASSES:
    - TestTransactionManager: Manages database transactions for test isolation
FUNCTIONS:
    - None
DEPENDENCIES:
    - logging: For operational logging
    - typing: For type annotations
    - psycopg2: For database connection handling

This module provides transaction management capabilities for database tests,
allowing tests to make changes to the database without affecting other tests
or requiring cleanup afterward. It uses PostgreSQL's transaction and savepoint
features to isolate database changes within a test.

The transaction manager creates savepoints that can be rolled back to, ensuring
that each test starts with a clean database state. This is particularly useful
for integration tests that need to interact with a real database.

Example usage:
When testing a service that makes database changes, the TestTransactionManager
ensures that those changes are isolated within the test and automatically
rolled back afterward, preserving the initial state of the database for
subsequent tests. This eliminates the need for complex test cleanup logic.
"""

import logging
import psycopg2
from psycopg2 import extras
from typing import Optional, List, Any

class TestTransactionManager:
    """
    Manages database transactions for test isolation.
    
    This class provides a context manager for database transactions, allowing
    tests to make changes to the database without affecting other tests or
    requiring cleanup afterward. It supports savepoints for more granular
    control over transaction state.
    """
    
    def __init__(self, connection_string: str = None, connection = None):
        """
        Initialize the transaction manager.
        
        Args:
            connection_string: Database connection string (ignored if connection provided)
            connection: Existing database connection (optional)
        """
        # Configure logging
        self.logger = logging.getLogger("transaction_manager")
        
        # Store initialization parameters
        self.connection_string = connection_string
        self.conn = connection
        self.savepoints: List[str] = []
        self.own_connection = False
    
    def __enter__(self):
        """
        Enter the context manager, establishing a database connection.
        
        Returns:
            Self for context manager
        """
        # If no connection was provided, create one
        if self.conn is None:
            if self.connection_string is None:
                # Try to get connection string from settings
                try:
                    from config.settings import TEST_DB_USER, TEST_DB_PASS, TEST_DB_HOST, TEST_DB_PORT, TEST_DB_NAME
                    self.connection_string = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
                except ImportError:
                    raise ValueError("No connection string provided and could not load from settings")
                    
            self.logger.debug(f"Creating database connection for transaction")
            self.conn = psycopg2.connect(self.connection_string)
            self.own_connection = True
        
        # Disable autocommit to enable transaction management
        self.conn.autocommit = False
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager, handling transaction state.
        
        If an exception occurred, roll back the transaction.
        If no exception, commit the transaction.
        If we created the connection, close it.
        
        Args:
            exc_type: Exception type, if any
            exc_val: Exception value, if any
            exc_tb: Exception traceback, if any
        """
        if exc_type is not None:
            # An exception occurred, roll back the transaction
            self.logger.warning(f"Exception in transaction, rolling back: {exc_val}")
            self.conn.rollback()
        else:
            # No exception, commit the transaction
            self.logger.debug("Transaction completed successfully, committing")
            self.conn.commit()
        
        # If we created the connection, close it
        if self.own_connection:
            self.logger.debug("Closing database connection")
            self.conn.close()
    
    def create_savepoint(self, name: Optional[str] = None) -> str:
        """
        Create a savepoint to roll back to.
        
        Args:
            name: Savepoint name (auto-generated if None)
            
        Returns:
            Savepoint name
        """
        # Generate a savepoint name if none provided
        if name is None:
            name = f"sp_{len(self.savepoints)}"
        
        # Create the savepoint
        self.logger.debug(f"Creating savepoint: {name}")
        cursor = self.conn.cursor()
        cursor.execute(f"SAVEPOINT {name}")
        cursor.close()
        
        # Remember the savepoint
        self.savepoints.append(name)
        
        return name
    
    def rollback_to_savepoint(self, name: Optional[str] = None) -> None:
        """
        Roll back to the specified savepoint or last created.
        
        Args:
            name: Savepoint name (defaults to last created)
            
        Raises:
            ValueError: If no savepoints available or specified savepoint not found
        """
        # Ensure we have savepoints
        if not self.savepoints:
            raise ValueError("No savepoints available")
        
        # Use the last savepoint if none specified
        if name is None:
            name = self.savepoints[-1]
        elif name not in self.savepoints:
            raise ValueError(f"Savepoint {name} not found")
        
        # Roll back to the savepoint
        self.logger.debug(f"Rolling back to savepoint: {name}")
        cursor = self.conn.cursor()
        cursor.execute(f"ROLLBACK TO SAVEPOINT {name}")
        cursor.close()
    
    def release_savepoint(self, name: Optional[str] = None) -> None:
        """
        Release the specified savepoint or last created.
        
        Args:
            name: Savepoint name (defaults to last created)
            
        Raises:
            ValueError: If no savepoints available or specified savepoint not found
        """
        # Ensure we have savepoints
        if not self.savepoints:
            raise ValueError("No savepoints available")
        
        # Use the last savepoint if none specified
        if name is None:
            name = self.savepoints[-1]
            self.savepoints.pop()
        elif name in self.savepoints:
            self.savepoints.remove(name)
        else:
            raise ValueError(f"Savepoint {name} not found")
        
        # Release the savepoint
        self.logger.debug(f"Releasing savepoint: {name}")
        cursor = self.conn.cursor()
        cursor.execute(f"RELEASE SAVEPOINT {name}")
        cursor.close()
    
    def execute(self, query: str, params: Any = None) -> None:
        """
        Execute a SQL statement without returning results.
        
        Args:
            query: SQL query
            params: Query parameters
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
        finally:
            cursor.close()
    
    def fetch_one(self, query: str, params: Any = None) -> Optional[dict]:
        """
        Execute a SQL query and return one result.
        
        Args:
            query: SQL query
            params: Query parameters
            
        Returns:
            Dictionary with row data or None
        """
        cursor = self.conn.cursor(cursor_factory=extras.RealDictCursor)
        try:
            cursor.execute(query, params)
            return cursor.fetchone()
        finally:
            cursor.close()
    
    def fetch_all(self, query: str, params: Any = None) -> List[dict]:
        """
        Execute a SQL query and return all results.
        
        Args:
            query: SQL query
            params: Query parameters
            
        Returns:
            List of dictionaries with row data
        """
        cursor = self.conn.cursor(cursor_factory=extras.RealDictCursor)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()

# Convenience function to create a transaction manager
def with_transaction(func):
    """
    Decorator to provide a transaction manager to a function.
    
    This decorator creates a transaction manager and passes it to the decorated
    function as its first argument. If the function completes without raising
    an exception, the transaction is committed. If an exception is raised, the
    transaction is rolled back.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        with TestTransactionManager() as txn:
            return func(txn, *args, **kwargs)
    return wrapper 