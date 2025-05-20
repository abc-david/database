# Database Environments

## Overview

The content generator system uses separate production and test database environments to ensure robust development, testing, and deployment. This document explains the relationship between these environments, how they're configured, and best practices for working with them.

## Environment Separation

The system maintains two separate database environments:

1. **Production Database**: Contains live, user-facing data and is used by production services
2. **Test Database**: Used for development and testing, with a controlled, predictable state

Each environment is a complete PostgreSQL database with identical schema structures but potentially different data.

## Database Connections

### Production Database

- Database name: `contentgen_db` (default)
- Purpose: Stores production data used by live services
- Connection managed through: `DBConnector` with no test mode

### Test Database

- Database name: `contentgen_test_db` (default)
- Purpose: Used for development, testing, and CI/CD pipelines
- Connection managed through: `DBConnector` with `test_mode="e2e"`

## Schema and Data Mirroring

### Public Schema Mirroring

The test database's public schema maintains a specific relationship with the production database:

#### Fully Mirrored Tables (Structure + Data)

These tables have identical structure AND data between environments:

- `object_models`: Ensures tests run against the same object model definitions
- `prompts`: Provides consistent prompt templates for testing

This mirroring enables tests to work with the same canonical definitions as production, ensuring that object validation and prompt rendering behave identically.

#### Structure-Only Mirrored Tables

These tables have the same structure but different data:

- `projects`: Contains test projects instead of production projects
- `clients`: Contains test clients instead of production clients
- `llm_usage`: Contains test usage records

### Project Schema Mirroring

Project schemas in the test database:

1. Have identical table structure to production
2. Contain controlled test data rather than production data
3. May include additional test-only projects that don't exist in production

## Data Synchronization

The database service includes tools for synchronizing schemas and data between environments:

```python
from services.database.sync import DatabaseSyncManager

# Create a sync manager
sync_manager = DatabaseSyncManager()

# Sync object_models and prompts from production to test
sync_manager.sync_tables(
    source_db="production",
    target_db="test",
    tables=["object_models", "prompts"],
    schemas=["public"]
)
```

The `DatabaseSyncManager` provides utilities for:
- Creating database dumps
- Restoring from dumps
- Synchronizing specific tables or schemas
- Comparing schema structures

## Access Credentials

### Credential Sources

Database credentials are managed through a layered approach:

1. **Configuration Files**: Primary source in `config/settings.py`
2. **Environment Variables**: Secondary source through `.env` files
3. **Default Fallbacks**: Used when neither configuration nor environment variables are available

### Configuration in settings.py

Production and test database credentials are stored separately:

```python
# Production database
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "contentgen_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "")

# Test database
TEST_DB_HOST = os.getenv("TEST_DB_HOST", "localhost")
TEST_DB_PORT = os.getenv("TEST_DB_PORT", "5432")
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "contentgen_test_db")
TEST_DB_USER = os.getenv("TEST_DB_USER", "test_runner_user")
TEST_DB_PASS = os.getenv("TEST_DB_PASS", "test123")
```

### Environment Variables

For local development or deployment, credentials can be provided via environment variables:

```bash
# Production database credentials
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=contentgen_db
export DB_USER=postgres
export DB_PASS=secure_password

# Test database credentials
export TEST_DB_HOST=localhost
export TEST_DB_PORT=5432
export TEST_DB_NAME=contentgen_test_db
export TEST_DB_USER=test_runner_user
export TEST_DB_PASS=test123
```

### Accessing the Right Database

The `DBOperator` automatically selects the correct database based on the `test_mode` parameter:

```python
# Connect to production database
prod_db = DBOperator(test_mode=None)  # or omit the parameter

# Connect to test database
test_db = DBOperator(test_mode="e2e")
```

### Test Database Permissions

The test database user should have specific permissions:

1. Full CRUD access to all tables
2. Schema creation and modification rights
3. The ability to create and drop tables

These permissions allow tests to create, modify, and clean up data as needed.

## Database Initialization

### Production Database

The production database is typically initialized through migration scripts or the application's schema setup utilities:

```python
from services.database import SchemaSetup

# Initialize production schemas
schema_setup = SchemaSetup()
await schema_setup.ensure_public_schema()
```

### Test Database

The test database can be initialized:

1. **From Scratch**: Using schema setup utilities
2. **From Production**: By cloning the production database structure
3. **From Scripts**: Using initialization scripts in CI/CD pipelines

```python
# Initialize test database from scratch
test_schema_setup = SchemaSetup(test_mode="e2e")
await test_schema_setup.ensure_public_schema()

# Alternatively, clone from production
from services.database.sync import DatabaseSyncManager
sync_manager = DatabaseSyncManager()
await sync_manager.clone_structure(source="production", target="test")
```

## Database Reset and Seeding

The test database often needs to be reset to a known state between test runs:

```python
from services.database import DBOperator

# Create operator for test database
db = DBOperator(test_mode="e2e")

# Reset database to clean state
await db.reset_test_database()

# Load seed data
await db.load_seed_data("tests/data/seed_data.json")
```

Seed data typically includes:
- Test projects
- Object model instances
- Test content entries
- Any other data needed for testing

## Best Practices

1. **Never use production database for testing**
2. **Keep object_models and prompts synchronized** between environments
3. **Use transaction isolation** for tests to prevent cross-test contamination
4. **Maintain seed data** in version control for repeatable tests
5. **Explicitly specify test_mode** when connecting to databases
6. **Reset the test database** to a known state before test suites
7. **Never hardcode database credentials** in application code

Following these practices ensures clean separation between environments, predictable test results, and a secure handling of database access. 