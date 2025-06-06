"""
MODULE: services/database/db_connector.py
PURPOSE: Provides asynchronous database connectivity with connection pooling for PostgreSQL
AUTHOR: Generated by Cursor AI

This module provides a PostgreSQL connector with connection pooling via asyncpg.
The DBConnector class serves as the base for all database operations, handling
connections, query execution, and transaction management.
"""

import asyncio
import logging
import os
import time
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional, Tuple, Union

import asyncpg
from asyncpg.transaction import Transaction

from config.settings import DB_CONFIG, TEST_MODE

logger = logging.getLogger(__name__)

class ConnectionError(Exception):
    """
    Connection-related errors.
    
    These errors occur when there's a problem establishing a database connection,
    managing the connection pool, or when a connection unexpectedly drops.
    """
    pass

class QueryError(Exception):
    """
    Query-related errors.
    
    These errors occur when there's a problem executing a SQL query,
    such as syntax errors, constraint violations, or timeout issues.
    """
    pass

class TransactionError(Exception):
    """
    Transaction-related errors.
    
    These errors occur when there's a problem with a database transaction,
    such as a failed commit, rollback errors, or serialization failures.
    """
    pass

class DBConnector:
    """
    PostgreSQL connector with connection pooling via asyncpg.
    
    This class serves as the base for all database operations, handling connections,
    query execution, and transaction management.
    
    Attributes:
        _pool: Shared connection pool for database connections
    """
    
    _pool = None
    
    @classmethod
    async def get_pool(cls):
        """
        Get or create the connection pool.
        
        Returns:
            asyncpg.pool.Pool: The connection pool
            
        Raises:
            ConnectionError: If the connection pool cannot be created
        """
        if cls._pool is None:
            logger.info("Initializing asyncpg database connection pool")
            logger.info(f"Using database configuration: {DB_CONFIG}")
            
            try:
                cls._pool = await asyncpg.create_pool(
                    host=DB_CONFIG["host"],
                    port=DB_CONFIG["port"],
                    user=DB_CONFIG["user"],
                    password=DB_CONFIG["password"],
                    database=DB_CONFIG["database"],
                    min_size=5,
                    max_size=20
                )
                logger.info("Database connection pool initialized")
            except Exception as e:
                logger.error(f"Failed to create connection pool: {str(e)}")
                raise ConnectionError(f"Failed to create connection pool: {str(e)}") from e
                
        return cls._pool
    
    async def execute(self, 
                     query: str, 
                     params: tuple = None, 
                     fetch_val: bool = False,
                     fetch_row: bool = False, 
                     fetch_all: bool = False, 
                     schema: str = None) -> Any:
        """
        Execute a query with proper error handling.
        
        Args:
            query: SQL query string
            params: Query parameters (values for $1, $2, etc.)
            fetch_val: Return single value (first column of first row)
            fetch_row: Return single row as dictionary
            fetch_all: Return all rows as list of dictionaries
            schema: Schema to set before query
            
        Returns:
            Query result based on fetch parameters:
            - fetch_val: Single value
            - fetch_row: Single row as dictionary
            - fetch_all: List of dictionaries
            - default: Query status string
            
        Raises:
            QueryError: If the query execution fails
            ConnectionError: If the connection cannot be acquired
        """
        pool = await self.get_pool()
        
        try:
            async with pool.acquire() as conn:
                # Optionally set schema
                if schema:
                    await conn.execute(f"SET search_path TO {schema}")
                
                if fetch_val:
                    return await conn.fetchval(query, *(params or ()))
                elif fetch_row:
                    row = await conn.fetchrow(query, *(params or ()))
                    return dict(row) if row else None
                elif fetch_all:
                    rows = await conn.fetch(query, *(params or ()))
                    return [dict(row) for row in rows] if rows else []
                else:
                    return await conn.execute(query, *(params or ()))
        except asyncpg.PostgresError as e:
            logger.error(f"Database query error: {str(e)}")
            logger.error(f"Query: {query}")
            if params:
                logger.error(f"Params: {params}")
            raise QueryError(f"Database query error: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error during query execution: {str(e)}")
            logger.error(f"Query: {query}")
            if params:
                logger.error(f"Params: {params}")
            raise
    
    @asynccontextmanager
    async def transaction(self):
        """
        Context manager for transactions.
        
        Usage:
            async with db.transaction() as conn:
                await conn.execute(...)
        
        Yields:
            asyncpg.Connection: Connection with active transaction
            
        Raises:
            TransactionError: If transaction operations fail
        """
        pool = await self.get_pool()
        connection = await pool.acquire()
        transaction = None
        
        try:
            transaction = connection.transaction()
            await transaction.start()
            
            # Create method for dictionary query results without modifying connection object
            async def fetch_dict(query, *args):
                row = await connection.fetchrow(query, *args)
                return dict(row) if row else None
                
            async def fetch_all_dict(query, *args):
                rows = await connection.fetch(query, *args)
                return [dict(row) for row in rows] if rows else []
            
            # Instead of adding these methods to the connection directly, create a wrapper
            class ConnectionWrapper:
                def __init__(self, connection):
                    self.connection = connection
                    
                async def execute(self, query, *args):
                    # If args[0] is a tuple and it's the only arg, we need to unpack it
                    if len(args) == 1 and isinstance(args[0], tuple):
                        return await connection.execute(query, *args[0])
                    return await connection.execute(query, *args)
                    
                async def fetchval(self, query, *args):
                    if len(args) == 1 and isinstance(args[0], tuple):
                        return await connection.fetchval(query, *args[0])
                    return await connection.fetchval(query, *args)
                    
                async def fetchrow(self, query, *args):
                    if len(args) == 1 and isinstance(args[0], tuple):
                        return await connection.fetchrow(query, *args[0])
                    return await connection.fetchrow(query, *args)
                    
                async def fetch(self, query, *args):
                    if len(args) == 1 and isinstance(args[0], tuple):
                        return await connection.fetch(query, *args[0])
                    return await connection.fetch(query, *args)
                    
                async def fetch_dict(self, query, *args):
                    if len(args) == 1 and isinstance(args[0], tuple):
                        return await fetch_dict(query, *args[0])
                    return await fetch_dict(query, *args)
                    
                async def fetch_all_dict(self, query, *args):
                    if len(args) == 1 and isinstance(args[0], tuple):
                        return await fetch_all_dict(query, *args[0])
                    return await fetch_all_dict(query, *args)
                    
            # Yield the wrapped connection
            yield ConnectionWrapper(connection)
            await transaction.commit()
        except Exception as e:
            if transaction:
                try:
                    await transaction.rollback()
                except Exception as rb_error:
                    logger.error(f"Error rolling back transaction: {str(rb_error)}")
            logger.error(f"Transaction error: {str(e)}")
            raise TransactionError(f"Transaction error: {str(e)}") from e
        finally:
            await pool.release(connection)
    
    async def close(self):
        """
        Close all connections in the pool.
        
        This should be called when the application is shutting down.
        """
        if self.__class__._pool:
            await self.__class__._pool.close()
            self.__class__._pool = None
            logger.info("Database connection pool closed")


# Exception classes
class ConnectionError(Exception):
    """Error connecting to the database."""
    pass

class QueryError(Exception):
    """Error executing a database query."""
    pass

class TransactionError(Exception):
    """Error with database transactions."""
    pass

class SchemaError(Exception):
    """Error with database schema operations."""
    pass 