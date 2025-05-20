# Database Service Tests

This directory contains tests specific to the database service component.

## Test Files

- `test_basic_operations.py`: Tests for basic CRUD operations of the database service
- Add more test files as needed for different aspects of the database service

## Component-Specific Fixtures

The `conftest.py` file in this directory provides fixtures specific to database testing:

- `db`: A database operator instance for testing
- `test_table`: Creates a test table for database operations
- `sample_records`: Inserts sample records for testing queries and updates

These fixtures build on the global fixtures defined in the top-level `/tests/conftest.py`.

## Running Tests

To run all database tests:

```bash
python -m pytest services/database/tests/
```

To run a specific test file:

```bash
python -m pytest services/database/tests/test_basic_operations.py
```

## Database Test Best Practices

1. **Use transaction isolation**:
   - Prefer using the global `isolated_test_project` fixture for tests that modify data
   - This ensures all changes are rolled back after the test completes

2. **Create specific test tables**:
   - Use the `test_table` fixture to create tables specifically for testing
   - Don't use production tables for tests

3. **Clean up after tests**:
   - Always clean up any data created during tests
   - Use fixture teardown or try/finally blocks to ensure cleanup happens

4. **Test real SQL queries**:
   - Test the actual SQL queries that will be used in production
   - Don't simplify or mock database operations unless necessary

5. **Test edge cases**:
   - Test handling of NULL values, empty results, and other edge cases
   - Test error conditions and exception handling 