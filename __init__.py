"""
Database service module providing asynchronous PostgreSQL operations.

This package provides a robust, fully asynchronous database interface for
PostgreSQL using asyncpg. It implements standardized methods for common 
database operations with intelligent column matching and comprehensive 
error handling.

Key components:
- DBConnector: Low-level database connection manager
- DBOperator: Higher-level API with standardized methods
- SchemaSetup: Utility for setting up and verifying schemas
- with_db_connection: Decorator for injecting database connections

Testing & Development Tools:
- mock: Schema-aware mock data generation for testing
- testing: Transaction isolation and other testing utilities
- performance: Query logging and performance monitoring
- sync: Database synchronization between environments
"""

from .db_connector import (
    DBConnector,
    ConnectionError,
    QueryError,
    TransactionError,
    SchemaError
)

from .db_operator import (
    DBOperator,
    ColumnMatchError,
    match_column
)

from .schema_setup import SchemaSetup
from .sql_templates import SQL_TEMPLATES, get_required_tables
from .decorators import with_db_connection

# Import mock package
from .mock import SchemaRegistry, MockDataGenerator

# Import testing package
from .testing import TestTransactionManager, with_transaction

# Import performance package
from .performance import QueryLogger, QueryLogEntry, time_query

# Import sync package
from .sync import DatabaseSyncManager

__all__ = [
    # Core classes
    'DBConnector',
    'DBOperator',
    'SchemaSetup',
    
    # Exceptions
    'ConnectionError',
    'QueryError',
    'TransactionError',
    'SchemaError',
    'ColumnMatchError',
    
    # Utilities
    'match_column',
    'SQL_TEMPLATES',
    'get_required_tables',
    
    # Decorators
    'with_db_connection',
    
    # Mock package
    'SchemaRegistry',
    'MockDataGenerator',
    
    # Testing package
    'TestTransactionManager',
    'with_transaction',
    
    # Performance package
    'QueryLogger',
    'QueryLogEntry',
    'time_query',
    
    # Sync package
    'DatabaseSyncManager'
]
