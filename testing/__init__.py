"""
MODULE: services/database/testing/__init__.py
PURPOSE: Export classes and functions from the testing package
CLASSES:
    - TestTransactionManager: For managing database transactions in tests
FUNCTIONS:
    - with_transaction: Decorator to provide transaction management
DEPENDENCIES:
    - transaction_manager: Provides transaction isolation for tests

This module exports the main classes and functions from the testing package,
making them available for importing directly from the package. The package
provides functionality for database testing, including transaction isolation
and other testing utilities.

The exported components help ensure that database tests are isolated, repeatable,
and don't interfere with each other, making the test suite more reliable and
easier to maintain.

Example usage:
from services.database.testing import TestTransactionManager, with_transaction

# Use the transaction manager directly
with TestTransactionManager() as txn:
    # Make database changes that will be rolled back automatically
    txn.execute("INSERT INTO users (name) VALUES ('test_user')")
    
# Or use the decorator
@with_transaction
def test_db_operation(txn):
    txn.execute("INSERT INTO users (name) VALUES ('test_user')")
    result = txn.fetch_one("SELECT * FROM users WHERE name = 'test_user'")
    assert result is not None
"""

from .transaction_manager import TestTransactionManager, with_transaction

__all__ = [
    "TestTransactionManager",
    "with_transaction"
] 