"""
MODULE: services/database/tests/test_db_operator.py
PURPOSE: Test the DBOperator class
CLASSES:
    - TestDBOperator: Test class for DBOperator
FUNCTIONS:
    - None
DEPENDENCIES:
    - pytest: For test fixtures and assertions
    - pytest_asyncio: For async test support
    - services.database.db_operator: For the DBOperator class
    - services.database.schema_setup: For setting up test schemas

This module tests the functionality of the DBOperator class, including
CRUD operations, column matching, error handling, and transactions.
"""

import pytest
import pytest_asyncio
import uuid
import asyncio
from typing import Dict, Any

from services.database.db_operator import DBOperator, ColumnMatchError
from services.database.schema_setup import SchemaSetup

# Test schema name (will be created and dropped for tests)
TEST_SCHEMA = "db_operator_test"

@pytest_asyncio.fixture
async def setup_test_schema():
    """
    Fixture to set up and tear down the test schema.
    Creates a test schema with required tables, and drops it after tests.
    """
    # Create schema setup utility
    schema_setup = SchemaSetup()
    
    try:
        # Create test schema
        await schema_setup._create_schema(TEST_SCHEMA)
        
        # Create required tables
        await schema_setup.ensure_project_schema(TEST_SCHEMA)
        
        # Create test data tables
        test_tables = {
            "test_users": f"""
            CREATE TABLE IF NOT EXISTS {TEST_SCHEMA}.test_users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                username TEXT NOT NULL,
                email TEXT,
                active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
            """,
            "test_items": f"""
            CREATE TABLE IF NOT EXISTS {TEST_SCHEMA}.test_items (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL,
                description TEXT,
                user_id UUID REFERENCES {TEST_SCHEMA}.test_users(id) ON DELETE CASCADE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
            """
        }
        
        # Create test tables
        for table, sql in test_tables.items():
            await schema_setup._connector.execute(sql)
            
        yield
    finally:
        # Drop test schema and all its tables
        try:
            await schema_setup._connector.execute(f"DROP SCHEMA {TEST_SCHEMA} CASCADE")
        except Exception as e:
            print(f"Error dropping test schema: {e}")
        finally:
            await schema_setup.close()

@pytest_asyncio.fixture
async def db_operator():
    """
    Fixture to create and close a DBOperator instance.
    """
    operator = DBOperator()
    yield operator
    await operator.close()

@pytest_asyncio.fixture
async def test_user(db_operator, setup_test_schema):
    """
    Fixture to create a test user and clean it up after tests.
    """
    # Insert test user
    user = await db_operator.insert(
        "test_users",
        {
            "username": "testuser",
            "email": "test@example.com"
        },
        schema=TEST_SCHEMA
    )
    
    yield user
    
    # No need to clean up, as the schema will be dropped

class TestDBOperator:
    """Test class for DBOperator."""
    
    @pytest.mark.asyncio
    async def test_insert_and_get(self, db_operator, setup_test_schema):
        """Test inserting a record and retrieving it by UUID."""
        # Insert a record
        inserted = await db_operator.insert(
            "test_users",
            {
                "username": "johndoe",
                "email": "john@example.com"
            },
            schema=TEST_SCHEMA
        )
        
        assert inserted is not None
        assert inserted["username"] == "johndoe"
        assert inserted["email"] == "john@example.com"
        assert "id" in inserted
        
        # Get the record by UUID
        retrieved = await db_operator.get_by_uuid(
            "test_users",
            inserted["id"],
            schema=TEST_SCHEMA
        )
        
        assert retrieved is not None
        assert retrieved["id"] == inserted["id"]
        assert retrieved["username"] == "johndoe"
        assert retrieved["email"] == "john@example.com"
    
    @pytest.mark.asyncio
    async def test_get_by_name(self, db_operator, test_user):
        """Test retrieving a record by name."""
        # Get by username
        user = await db_operator.get_by_name(
            "test_users",
            "testuser",
            name_column="username",
            schema=TEST_SCHEMA
        )
        
        assert user is not None
        assert user["username"] == "testuser"
        assert user["email"] == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_update(self, db_operator, test_user):
        """Test updating a record."""
        # Update the email
        updated = await db_operator.update(
            "test_users",
            {"email": "updated@example.com"},
            {"id": test_user["id"]},
            schema=TEST_SCHEMA
        )
        
        assert updated is not None
        assert updated["email"] == "updated@example.com"
        
        # Verify the update
        retrieved = await db_operator.get_by_uuid(
            "test_users",
            test_user["id"],
            schema=TEST_SCHEMA
        )
        
        assert retrieved is not None
        assert retrieved["email"] == "updated@example.com"
    
    @pytest.mark.asyncio
    async def test_fetch(self, db_operator, test_user):
        """Test fetching records with conditions."""
        # Insert another user
        await db_operator.insert(
            "test_users",
            {
                "username": "janedoe",
                "email": "jane@example.com",
                "active": False
            },
            schema=TEST_SCHEMA
        )
        
        # Fetch active users
        active_users = await db_operator.fetch(
            "test_users",
            {"active": True},
            schema=TEST_SCHEMA
        )
        
        assert len(active_users) == 1
        assert active_users[0]["username"] == "testuser"
        
        # Fetch all users
        all_users = await db_operator.fetch(
            "test_users",
            schema=TEST_SCHEMA
        )
        
        assert len(all_users) == 2
    
    @pytest.mark.asyncio
    async def test_delete(self, db_operator, test_user):
        """Test deleting a record."""
        # Delete the user
        deleted = await db_operator.delete(
            "test_users",
            {"id": test_user["id"]},
            returning=True,
            schema=TEST_SCHEMA
        )
        
        assert len(deleted) == 1
        assert deleted[0]["id"] == test_user["id"]
        
        # Verify the deletion
        retrieved = await db_operator.get_by_uuid(
            "test_users",
            test_user["id"],
            schema=TEST_SCHEMA
        )
        
        assert retrieved is None
    
    @pytest.mark.asyncio
    async def test_column_matching(self, db_operator, test_user):
        """Test column matching functionality."""
        # Test with different case
        user = await db_operator.get_by_column(
            "test_users",
            "USERNAME",
            "testuser",
            schema=TEST_SCHEMA
        )
        
        assert user is not None
        assert user["username"] == "testuser"
        
        # Test with singular/plural
        await db_operator.insert(
            "test_items",
            {
                "name": "Test Item",
                "description": "A test item",
                "userId": test_user["id"]  # camelCase and different name
            },
            schema=TEST_SCHEMA
        )
        
        # Fetch items by user ID with different column style
        items = await db_operator.fetch(
            "test_items",
            {"user_id": test_user["id"]},
            schema=TEST_SCHEMA
        )
        
        assert len(items) == 1
        assert items[0]["name"] == "Test Item"
    
    @pytest.mark.asyncio
    async def test_column_matching_error(self, db_operator, setup_test_schema):
        """Test column matching error handling."""
        # Try to insert with a non-existent column
        with pytest.raises(ColumnMatchError) as exc_info:
            await db_operator.insert(
                "test_users",
                {"nonexistent_column": "value"},
                schema=TEST_SCHEMA
            )
        
        # Check that the error message includes available columns
        assert "Column 'nonexistent_column' not found" in str(exc_info.value)
        assert "Available columns" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_transaction(self, db_operator, setup_test_schema):
        """Test transaction handling."""
        # Successful transaction
        async with db_operator.transaction() as conn:
            # Insert a user
            await conn.execute(
                f"INSERT INTO {TEST_SCHEMA}.test_users (username, email) VALUES ($1, $2)",
                ("transaction_user", "transaction@example.com")
            )
            
            # Insert an item for the user
            await conn.execute(
                f"""
                INSERT INTO {TEST_SCHEMA}.test_items (name, description, user_id) 
                VALUES ($1, $2, (SELECT id FROM {TEST_SCHEMA}.test_users WHERE username = $3))
                """,
                ("Transaction Item", "Created in transaction", "transaction_user")
            )
        
        # Verify both records were created
        user = await db_operator.get_by_name(
            "test_users",
            "transaction_user",
            name_column="username",
            schema=TEST_SCHEMA
        )
        
        assert user is not None
        
        items = await db_operator.fetch(
            "test_items",
            {"user_id": user["id"]},
            schema=TEST_SCHEMA
        )
        
        assert len(items) == 1
        assert items[0]["name"] == "Transaction Item"
        
        # Failed transaction
        with pytest.raises(Exception):
            async with db_operator.transaction() as conn:
                # Insert a user
                await conn.execute(
                    f"INSERT INTO {TEST_SCHEMA}.test_users (username, email) VALUES ($1, $2)",
                    ("rollback_user", "rollback@example.com")
                )
                
                # This will fail due to an invalid user ID
                await conn.execute(
                    f"""
                    INSERT INTO {TEST_SCHEMA}.test_items (name, description, user_id) 
                    VALUES ($1, $2, $3)
                    """,
                    ("Rollback Item", "Will be rolled back", "invalid-uuid")
                )
        
        # Verify the user was not created (transaction rolled back)
        user = await db_operator.get_by_name(
            "test_users",
            "rollback_user",
            name_column="username",
            schema=TEST_SCHEMA
        )
        
        assert user is None 