# Database Service

This service provides a robust, fully asynchronous database interface for PostgreSQL using `asyncpg`. 
It implements standardized methods for common database operations with intelligent column matching 
and comprehensive error handling.

## Key Components

### DBConnector

Low-level database connection manager with connection pooling.

- **Purpose**: Provides core database connectivity and query execution
- **Features**:
  - Async connection pooling
  - Transaction management
  - Error handling
  - Schema-aware queries

```python
# Create a connector
db = DBConnector()

# Execute a query
result = await db.execute(
    "SELECT * FROM users WHERE id = $1", 
    (user_id,), 
    fetch_row=True
)

# Use with a transaction
async with db.transaction() as conn:
    await conn.execute("INSERT INTO users (name) VALUES ($1)", ("John Doe",))
    await conn.execute("INSERT INTO profiles (user_id) VALUES (currval('users_id_seq'))")
```

### DBOperator

Higher-level API for standardized operations across tables and schemas.

- **Purpose**: Provides a consistent interface for common database operations
- **Features**:
  - Schema-aware operations
  - Intelligent column matching
  - Standardized methods
  - Detailed error reporting
  - Data formatting utilities
  - Test support utilities

```python
# Create an operator
db = DBOperator()

# Fetch a record by UUID
user = await db.get_by_uuid("users", "550e8400-e29b-41d4-a716-446655440000", schema="public")

# Fetch records by name
user = await db.get_by_name("users", "john.doe", name_column="username", schema="public")

# Insert a new record
new_user = await db.insert("users", {
    "name": "Jane Smith",
    "email": "jane@example.com",
    "role": "user"
})

# Test utilities
await db.load_seed_data("tests/data/seed_projects.json")
await db.cleanup_non_protected()
```

## Standard Methods

The `DBOperator` provides the following standardized methods, all accepting a `schema` parameter:

| Method | Description |
|--------|-------------|
| `fetch` | Fetch multiple records with optional filtering, ordering, limits |
| `fetch_one` | Fetch a single record matching conditions |
| `get_by_uuid` | Get a record by UUID value |
| `get_by_name` | Get a record by name value |
| `get_by_column` | Get a record by a specific column value |
| `insert` | Insert a new record |
| `update` | Update records matching conditions |
| `upsert` | Insert or update a record based on unique columns |
| `delete` | Delete records matching conditions |
| `execute_raw` | Execute a raw SQL query |
| `table_exists` | Check if a table exists |
| `schema_exists` | Check if a schema exists |
| `create_schema` | Create a schema if it doesn't exist |

## Formatting Utilities

The `DBOperator` includes built-in formatting utilities for standardizing data storage and logging:

| Method | Description |
|--------|-------------|
| `_format_for_logging` | Format data for logging with sensible truncation |
| `_log_data` | Log formatted data if verbose logging is enabled |
| `_format_variable` | Format variables for storage with appropriate type handling |
| `_prepare_variables_for_storage` | Prepare variables dictionary for database storage |
| `_format_response_for_storage` | Format response data for storage |
| `clean_response_for_storage` | Clean and format response strings for storage |

The formatting utilities handle various data types including:
- JSON data (dicts and lists)
- Datetime objects
- Long strings
- Nested structures

## Test Support

The `DBOperator` includes testing utilities to support development and testing:

| Method | Description |
|--------|-------------|
| `load_seed_data` | Load seed data from JSON files into the database |
| `clone_project` | Clone an existing project with a new ID |
| `clone_prompt_template` | Clone an existing prompt template with a new ID |
| `cleanup_non_protected` | Remove non-protected records (preserves seed data) |
| `get_active_e2e_tests` | Get active end-to-end tests from the registry |

These utilities help with:
- Setting up test environments
- Creating test data
- Isolating tests
- Cleaning up after tests

## Column Matching

The database service includes an intelligent column matching system that can handle:

- Exact matches
- Case insensitivity
- Pluralization/singularization
- Underscores vs. camelCase

When a column match fails, the error message includes helpful suggestions:

```
Column 'userId' not found in table 'users'. Available columns: id, name, email, created_at. 
Did you mean: user_id?
```

## Error Handling

The service defines several error types for different database issues:

- `ConnectionError`: Problems connecting to the database
- `QueryError`: SQL syntax errors or constraint violations
- `SchemaError`: Issues with database schemas or tables
- `ColumnMatchError`: Failed column name matching

## Connection Pooling

The service uses `asyncpg` connection pooling for performance optimization:

- Minimum connections: 5
- Maximum connections: 20
- Connections are automatically returned to the pool after use

## Transactions

Transactions are supported using async context managers:

```python
# Transaction with DBConnector
async with db_connector.transaction() as conn:
    await conn.execute("INSERT INTO users (name) VALUES ($1)", ("Alice",))
    await conn.execute("INSERT INTO users (name) VALUES ($1)", ("Bob",))

# Transaction with DBOperator
async with db_operator.transaction() as conn:
    await conn.execute("INSERT INTO users (name) VALUES ($1)", ("Charlie",))
    # If any operation fails, the entire transaction is rolled back
```

## Async Decorators

For Celery compatibility, the database service provides an async decorator for injecting database connections:

```python
from services.database import with_db_connection

@with_db_connection
async def process_data(conn, data_id):
    # The connection is automatically injected
    result = await conn.fetch_dict("SELECT * FROM data WHERE id = $1", data_id)
    
    # Do something with the data
    await conn.execute(
        "UPDATE data SET processed = TRUE WHERE id = $1", 
        data_id
    )
    
    return result
```

The decorator handles:
1. Connection acquisition from the pool
2. Transaction management (commit on success, rollback on failure)
3. Connection release back to the pool
4. Works with both standalone functions and instance methods

For Celery tasks:

```python
from celery import shared_task
from services.database import with_db_connection

@shared_task
@with_db_connection
async def process_task(conn, task_id, parameters):
    # Use the connection for database operations
    # All operations are in a transaction
    # ...
    return result
```

## Schema Structures

### Required Tables for Project Schemas

- **content**: Main table for generated content
- **metadata**: Additional content metadata
- **vocabulary**: Project-specific terminology

### Core Tables in Public Schema

- **projects**: Project definitions and metadata
- **prompts**: Stored prompts for the LLM
- **object_models**: Schema definitions for content types
- **llm_usage**: Tracking of LLM usage and costs

## Usage Examples

### Basic Usage

```python
from services.database.db_operator import DBOperator

async def get_user_data():
    db = DBOperator()
    try:
        # Get a user by ID
        user = await db.get_by_uuid("users", "550e8400-e29b-41d4-a716-446655440000")
        
        # Insert a new record
        new_record = await db.insert("content", {
            "title": "New Content",
            "content": "This is the content",
            "content_type": "article"
        }, schema="b2b_saas")
        
        return user, new_record
    finally:
        await db.close()
```

### Working with Schemas

```python
from services.database.schema_setup import SchemaSetup

async def setup_project():
    setup = SchemaSetup()
    try:
        # Ensure public schema is ready
        await setup.ensure_public_schema()
        
        # Create or verify a project schema
        await setup.ensure_project_schema("new_project")
        
        # Verify all required tables exist
        verification = await setup.verify_schema("new_project")
        for table, exists in verification.items():
            print(f"Table {table}: {'✅' if exists else '❌'}")
    finally:
        await setup.close()
```

### Test Support Usage

```python
from services.database.db_operator import DBOperator

async def setup_test_environment():
    db = DBOperator()
    try:
        # Load seed data for testing
        await db.load_seed_data("tests/data/seed_projects.json")
        
        # Clone a project for testing
        test_project = await db.clone_project(
            "source-project-id", 
            f"test-project-{uuid.uuid4()}"
        )
        
        # Run your tests...
        
        # Clean up after tests
        await db.cleanup_non_protected()
    finally:
        await db.close()
```

### Transaction Management

```python
from services.database.db_operator import DBOperator

async def transfer_data(from_user_id, to_user_id, amount):
    db = DBOperator()
    try:
        async with db.transaction() as conn:
            # Deduct from one account
            await conn.execute(
                "UPDATE accounts SET balance = balance - $1 WHERE user_id = $2",
                (amount, from_user_id)
            )
            
            # Add to another account
            await conn.execute(
                "UPDATE accounts SET balance = balance + $1 WHERE user_id = $2",
                (amount, to_user_id)
            )
            
            # If any operation fails, the entire transaction is rolled back
    finally:
        await db.close()
```

## Implementation Status

Current development priorities:

1. **HIGH**: Fix schema creation to include all required tables
2. **HIGH**: Fix async implementation issues
3. **HIGH**: Implement transaction support
4. **MEDIUM**: Improve error handling and recovery
5. **MEDIUM**: Add schema migration support

## Testing

Unit tests are available in the `services/database/tests` directory.

Run tests with:

```bash
pytest services/database/tests
```

## Database Services

This module provides comprehensive database services for PostgreSQL integration, including connection management, schema setup, and testing utilities.

### Key Components

#### Core Database Services

- **DBConnector**: Low-level connection management and query execution
- **DBOperator**: High-level API with standardized methods for database operations
- **SchemaSetup**: Utilities for creating and verifying database schemas

#### Testing & Development Services

- **Mock System**: Schema-aware mock data generation
- **Testing Utilities**: Transaction isolation and database testing tools
- **Performance Monitoring**: Query logging and performance analysis
- **Database Synchronization**: Tools for dumping and restoring databases across environments

### Usage Examples

#### Basic Database Operations

```python
from services.database import DBOperator

# Create an operator
db = DBOperator()

try:
    # Insert data
    user_id = await db.insert(
        "users", 
        {"name": "John Doe", "email": "john@example.com"},
        schema="public"
    )
    
    # Fetch data
    user = await db.fetch_one(
        "SELECT * FROM public.users WHERE id = $1",
        (user_id,)
    )
    
    print(f"Created user: {user}")
finally:
    await db.close()
```

#### Schema Operations

```python
from services.database import SchemaSetup

# Initialize schema setup
schema_setup = SchemaSetup()

try:
    # Create project schema
    await schema_setup.ensure_project_schema("my_project")
    
    # Verify schema
    verification = await schema_setup.verify_schema("my_project")
    for table, exists in verification.items():
        print(f"Table {table}: {'✓' if exists else '✗'}")
finally:
    await schema_setup.close()
```

#### Transaction Management

```python
from services.database import TestTransactionManager

# Use transaction context manager
with TestTransactionManager() as txn:
    # Create savepoint
    txn.create_savepoint("before_changes")
    
    # Make changes
    txn.execute("INSERT INTO users (name) VALUES ('Test User')")
    
    # Roll back to savepoint if needed
    txn.rollback_to_savepoint("before_changes")
```

#### Schema-Aware Mocking

```python
from services.database import SchemaRegistry, MockDataGenerator

# Create schema registry and mock data generator
registry = SchemaRegistry()
generator = MockDataGenerator(registry)

# Generate mock data based on schema
mock_user = generator.generate_row("public", "users")
print(f"Mock user: {mock_user}")

# Generate related data
mock_data = generator.generate_related_rows(
    "public", "users",
    {"posts": {"count": 3, "fk_column": "user_id"}}
)
print(f"Mock user with posts: {mock_data}")
```

#### Performance Monitoring

```python
from services.database import QueryLogger, time_query

# Create a query logger
logger = QueryLogger(slow_threshold_ms=50)

# Create a service with query logging
class UserService:
    def __init__(self):
        self.query_logger = logger
        
    @time_query
    def get_user(self, user_id):
        # Execute query...
        pass

# Get statistics
stats = logger.get_stats()
print(f"Average query time: {stats['performance']['avg_time']}ms")

# Print summary
logger.print_summary()
```

#### Database Synchronization

```python
from services.database import DatabaseSyncManager

# Create sync manager
sync_manager = DatabaseSyncManager()

# Dump databases
prod_path, test_path = sync_manager.dump_all()

# Restore from dumps
sync_manager.restore_database(prod_path, is_test_db=False)

# Sync from another device
sync_manager.sync_from_dumps("user@otherhost")

# Commit dumps to git
sync_manager.commit_dumps_to_git("Update database state")
```

### Command-Line Tools

The database services include a command-line interface for database synchronization:

```bash
# Dump both databases
python -m services.database.sync.db_sync_cli dump --all

# Restore from latest dumps
python -m services.database.sync.db_sync_cli restore --latest

# Sync from another device
python -m services.database.sync.db_sync_cli sync --from user@otherhost

# Execute a common workflow
python -m services.database.sync.db_sync_cli workflow --dump-and-commit --push-after-commit
```

### Testing Framework Integration

The database services integrate with pytest for testing:

```python
import pytest
from services.database import with_transaction

# Use the transaction decorator for test isolation
@with_transaction
def test_user_creation(txn):
    # Create a user
    txn.execute("INSERT INTO users (name) VALUES ('Test User')")
    
    # Verify creation
    result = txn.fetch_one("SELECT * FROM users WHERE name = 'Test User'")
    assert result is not None
    
    # Transaction is automatically rolled back after test
```

### Directory Structure

```
services/database/
├── mock/               # Schema-aware mock data generation
│   ├── schema_registry.py
│   └── mock_data_generator.py
├── testing/            # Testing utilities
│   └── transaction_manager.py
├── performance/        # Performance monitoring
│   └── query_logger.py
├── sync/               # Database synchronization
│   ├── db_sync_manager.py
│   └── db_sync_cli.py
├── db_connector.py     # Core database connection
├── db_operator.py      # High-level database API
├── schema_setup.py     # Schema management
└── decorators.py       # Utility decorators
```

## Usage Examples

The `examples` directory contains working examples that demonstrate various features of the database services. To explore these examples:

```bash
# List all available examples
python -m services.database.examples.index list

# Run a specific example
python -m services.database.examples.index run mock_db_example
```

Available examples include:

1. **mock_db_example.py**: Demonstrates how to use the mock database system with DBOperator
2. **transaction_test_example.py**: Shows how to use transaction isolation in database tests
3. **sync_example.py**: Illustrates database synchronization between environments
4. **performance_example.py**: Shows how to monitor database query performance
5. **db_operator_test_modes.py**: Demonstrates the different test modes (production, e2e, mock)

Each example includes detailed comments explaining the functionality and usage patterns.

## Command-line Tools

Database synchronization tools are available through the command-line interface:

```bash
# Create a database dump
python -m services.database.sync.cli dump --output=db_dump.sql

# Restore from a dump
python -m services.database.sync.cli restore --input=db_dump.sql

# Sync from another device (requires SSH access)
python -m services.database.sync.cli sync --remote=user@host --db-name=db_name

# Execute common workflows
python -m services.database.sync.cli workflow --name=refresh_test_db
```

## Integration with Pytest

The database services integrate with pytest for efficient testing:

```python
import pytest
from services.database import DBOperator
from services.database.testing import with_transaction

class TestMyService:
    def setup_method(self):
        self.db = DBOperator(test_mode="e2e")
        
    @with_transaction
    def test_database_operation(self):
        # This test runs in an isolated transaction that will be rolled back
        result = self.db.insert("schema", "table", {"key": "value"})
        assert result is not None
```

## Directory Structure

```
services/database/
  ├── __init__.py              # Main package exports
  ├── README.md                # This documentation
  ├── connection.py            # Database connection management
  ├── operations.py            # DBOperator implementation
  ├── schema.py                # Schema setup and management
  ├── examples/                # Example scripts demonstrating usage
  ├── mock/                    # Mock data generation system
  ├── testing/                 # Testing utilities and transaction isolation
  ├── performance/             # Query logging and performance monitoring
  └── sync/                    # Database synchronization tools
``` 