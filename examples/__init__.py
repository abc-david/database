"""
MODULE: services/database/examples/__init__.py
PURPOSE: Package initialization for database service examples
VARIABLES:
    - __all__: List of example modules available in this package
DEPENDENCIES:
    - services.database: For database operations

This package contains example modules demonstrating various features and
usage patterns of the database services. Each example is self-contained and
can be run individually to showcase a specific feature or integration.

Examples include:
1. Mock database system (mock_db_example)
2. Transaction isolation in testing (transaction_test_example)
3. Database synchronization (sync_example)
4. Performance monitoring (performance_example)
5. DBOperator test modes (db_operator_test_modes)

To run examples, use the index module:
```
# List all examples
python -m services.database.examples.index list

# Run a specific example
python -m services.database.examples.index run mock_db_example
```
"""

# List of example modules for package exports
__all__ = [
    'mock_db_example',
    'transaction_test_example',
    'sync_example', 
    'performance_example',
    'db_operator_test_modes',
    'index'
] 