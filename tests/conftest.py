"""
MODULE: services/database/tests/conftest.py
PURPOSE: Database-specific test fixtures
"""

import pytest
import asyncio
from datetime import datetime

# Import the component being tested
from services.database import DBOperator

# Import the test_project fixture
from services.database.tests.test_project_fixture import test_project

@pytest.fixture
async def db():
    """Create a database operator for database tests."""
    db_operator = DBOperator()
    try:
        yield db_operator
    finally:
        await db_operator.close()


@pytest.fixture
async def test_table(db, test_project):
    """
    Create a test table for database testing.
    
    This fixture creates a table specifically for database service tests.
    It uses the local test_project fixture.
    """
    # Create the schema if it doesn't exist
    await db.execute_raw(f"CREATE SCHEMA IF NOT EXISTS {test_project}")
    
    # Create a test table
    await db.execute_raw(
        f"""
        CREATE TABLE IF NOT EXISTS {test_project}.test_db_items (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name TEXT NOT NULL,
            description TEXT,
            data JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
        """
    )
    
    yield
    
    # Clean up after test
    await db.execute_raw(f"DROP TABLE IF EXISTS {test_project}.test_db_items")
    await db.execute_raw(f"DROP SCHEMA IF EXISTS {test_project} CASCADE")


@pytest.fixture
async def sample_records(db, test_project, test_table):
    """
    Insert sample records for testing database operations.
    
    This fixture inserts test data that can be used by multiple tests.
    """
    record_ids = []
    
    # Insert sample records
    for i in range(1, 4):
        record = await db.insert(
            "test_db_items",
            {
                "name": f"Sample Item {i}",
                "description": f"This is test item {i}",
                "created_at": datetime.now().isoformat()
            },
            schema=test_project
        )
        record_ids.append(record["id"])
    
    yield record_ids
    
    # Clean up the inserted records (though test_table fixture will drop the table anyway)
    for record_id in record_ids:
        await db.delete("test_db_items", {"id": record_id}, schema=test_project) 