# Database Testing Methodology

## Overview

The content generator system provides a comprehensive database testing framework with multiple testing modes and isolation strategies. This document explains how to effectively test database interactions, use decorators for transaction isolation, and leverage mock data generation.

## Testing Modes

The database service supports three distinct testing modes:

1. **Production Mode**: Uses the real production database (only for live services)
2. **End-to-End (e2e) Mode**: Uses the test database with real database interactions
3. **Mock Mode**: Uses schema-aware mock data without any database connection

Each mode serves different testing needs and use cases.

## Setting the Test Mode

The test mode is set when creating the `DBOperator`:

```python
from services.database import DBOperator

# Production mode (default)
db = DBOperator()  # or DBOperator(test_mode=None)

# E2E test mode
db = DBOperator(test_mode="e2e")

# Mock mode
db = DBOperator(test_mode="mock")
```

## End-to-End Testing with Transaction Isolation

End-to-end tests interact with a real test database but should not affect each other. The database service provides transaction isolation to ensure tests don't interfere with each other.

### The with_transaction Decorator

The `with_transaction` decorator automatically wraps test functions in a database transaction that gets rolled back after the test completes:

```python
from services.database import DBOperator
from services.database.testing import with_transaction

class TestUserService:
    def setup_method(self):
        # Create a database connection to the test database
        self.db = DBOperator(test_mode="e2e")
        self.user_service = UserService(self.db)
    
    @with_transaction
    def test_create_user(self, txn):
        # The transaction manager is injected as the first argument
        
        # Create a test user
        user_data = {"name": "Test User", "email": "test@example.com"}
        user_id = self.user_service.create_user(user_data)
        
        # Verify the user was created
        user = self.user_service.get_user(user_id)
        assert user["name"] == "Test User"
        
        # After the test, the transaction will be rolled back automatically
        # so the test user won't affect other tests
```

### Transaction Manager

For more complex scenarios, you can use the `TestTransactionManager` directly:

```python
from services.database.testing import TestTransactionManager

def test_complex_scenario():
    # Create a transaction manager
    with TestTransactionManager() as txn:
        # Create savepoint
        txn.create_savepoint("before_changes")
        
        # Make some changes
        txn.execute("INSERT INTO users (name) VALUES ('Test User')")
        
        # Check the result
        user = txn.fetch_one("SELECT * FROM users WHERE name = 'Test User'")
        assert user is not None
        
        # Roll back to savepoint if needed
        txn.rollback_to_savepoint("before_changes")
        
        # Transaction is automatically rolled back after the with block
```

## Mock Testing with Schema-Aware Data

The mock mode provides a way to test database interactions without a real database. It uses schema-aware mock data that realistically represents what the database would return.

### Configuring the Mock System

To use the mock system, you need to configure a `SchemaRegistry` and attach it to the `DBOperator`:

```python
from services.database import DBOperator, SchemaRegistry

def test_with_mock_data():
    # Create a schema registry
    registry = SchemaRegistry()
    registry.initialize()
    
    # Create a DBOperator in mock mode with the registry
    db = DBOperator(test_mode="mock")
    db.schema_registry = registry
    
    # Now database operations will return realistic mock data
    user = db.fetch_one("SELECT * FROM users WHERE id = %s", (1,))
    assert "id" in user
    assert "name" in user
```

### How Mock Data Generation Works

The mock system generates data that accurately represents the database structure:

1. It extracts schema information (tables, columns, types, constraints)
2. It generates data that matches those constraints
3. It handles relationships between tables
4. It provides consistent reference integrity

For example, when mocking a query with foreign key relationships:

```python
# This will return a user with ID 1
user = db.fetch_one("SELECT * FROM users WHERE id = %s", (1,))

# This will return posts with user_id matching the first user
posts = db.fetch_all("SELECT * FROM posts WHERE user_id = %s", (user["id"],))
```

The mock data maintains referential integrity between related objects.

### Mock Data Customization

You can customize mock data generation for specific scenarios:

```python
from services.database.mock import MockDataGenerator

def test_with_custom_mock_data():
    # Create a schema registry
    registry = SchemaRegistry()
    registry.initialize()
    
    # Create a mock data generator
    generator = MockDataGenerator(registry)
    
    # Generate custom mock data
    custom_user = generator.generate_row(
        "public", "users", 
        override_values={"name": "Custom User"}
    )
    
    # Generate related data
    related_data = generator.generate_related_rows(
        "public", "users",
        {"posts": {"count": 3, "fk_column": "user_id"}},
        count=2  # Generate 2 users with related posts
    )
```

## Decorator-Based Testing Approach

The recommended approach for database testing is to use decorators that configure the test environment for you:

```python
from functools import wraps
from services.database import DBOperator, SchemaRegistry
from services.database.testing import with_transaction

def db_operation(mode: str = None):
    """
    Decorator for configuring database operations with a test mode.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create the appropriate DBOperator based on the mode
            db = DBOperator(test_mode=mode)
            
            # If using mock mode, set up mock data
            if mode == 'mock':
                registry = SchemaRegistry()
                registry.initialize()
                db.schema_registry = registry
                
            # Pass the DBOperator to the function
            return func(db, *args, **kwargs)
        return wrapper
    return decorator

# Use in tests or functions
@db_operation(mode="mock")
def test_user_service_with_mock(db):
    # Test with mock data
    user_service = UserService(db)
    user = user_service.get_user(1)
    assert user is not None

@db_operation(mode="e2e")
@with_transaction
def test_user_service_e2e(db, txn):
    # Test with real database in a transaction
    user_service = UserService(db)
    user_id = user_service.create_user({"name": "Test"})
    assert user_id is not None
```

## Test-Driven Development with Database Services

For effective test-driven development with database services:

1. **Start with mock tests** to outline the expected behavior
2. **Implement the feature** using the mock tests as a guide
3. **Add e2e tests** to verify the functionality with a real database
4. **Use transaction isolation** to keep tests independent

This approach provides good test coverage while keeping tests fast and reliable.

## Seeded Test Data

For tests that require specific data scenarios:

```python
from services.database import DBOperator

def setup_module():
    """Set up data before all tests in the module."""
    db = DBOperator(test_mode="e2e")
    db.load_seed_data("tests/data/users_seed.json")
    
@with_transaction
def test_specific_scenario(txn):
    """Test with the seeded data (which won't be modified permanently)."""
    db = DBOperator(test_mode="e2e")
    user = db.get_by_name("users", "seeded_test_user")
    assert user is not None
```

## Performance Testing

The database service includes tools for performance monitoring in tests:

```python
from services.database import DBOperator
from services.database.performance import QueryLogger

def test_query_performance():
    db = DBOperator(test_mode="e2e")
    
    # Create a query logger
    logger = QueryLogger(slow_threshold_ms=50)
    db.set_query_logger(logger)
    
    # Execute queries
    db.fetch_all("SELECT * FROM users")
    db.fetch_all("SELECT * FROM posts WHERE user_id = 1")
    
    # Analyze performance
    stats = logger.get_stats()
    assert stats["performance"]["avg_time"] < 100
    assert stats["slow_query_count"] == 0
```

## Test Data Clean-up

For test suites that need to clean up after themselves:

```python
def setup_module():
    """Initialize the test environment."""
    db = DBOperator(test_mode="e2e")
    db.reset_test_database()
    db.load_seed_data("tests/data/base_seed.json")

def teardown_module():
    """Clean up after all tests."""
    db = DBOperator(test_mode="e2e")
    db.cleanup_non_protected()  # Keep protected seed data, remove test artifacts
```

## Integration with Pytest

The database testing tools integrate well with pytest:

```python
# conftest.py
import pytest
from services.database import DBOperator

@pytest.fixture
def db():
    """Fixture providing a database connection to the test database."""
    return DBOperator(test_mode="e2e")

@pytest.fixture
def mock_db():
    """Fixture providing a mock database connection."""
    db = DBOperator(test_mode="mock")
    registry = SchemaRegistry()
    registry.initialize()
    db.schema_registry = registry
    return db
```

Then use in tests:

```python
def test_user_service(mock_db):
    """Test with a mock database."""
    user_service = UserService(mock_db)
    # Test implementation
```

## Best Practices

1. **Use the right test mode** for the test's needs
2. **Always use transaction isolation** for e2e tests
3. **Keep mock tests fast** and focused on behavior verification
4. **Use e2e tests** to verify real database interactions
5. **Never modify the production database** in tests
6. **Use fixtures** to set up test environments
7. **Clean up after tests** to prevent test pollution
8. **Test all database operations**: queries, inserts, updates, and deletes

Following these practices ensures reliable, fast, and maintainable database tests. 