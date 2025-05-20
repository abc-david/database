"""
MODULE: tests/services/database/test_basic_operations.py
PURPOSE: Unit tests for basic database operations
"""

import pytest
import uuid
import asyncio
from datetime import datetime

from services.database import DBOperator


@pytest.mark.unit
@pytest.mark.asyncio
async def test_insert_and_fetch_public():
    """Test inserting and fetching records in the public schema."""
    db = DBOperator()
    try:
        # Create test table in public schema
        table_name = "test_items_temp"  # Use a temp name to avoid conflicts
        schema = "public"
        await db.execute_raw(
            f"""
            CREATE TABLE IF NOT EXISTS {schema}.{table_name} (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL,
                description TEXT,
                data JSONB,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
            """
        )
        
        # Test data for public schema
        data = {
            "name": "Test Item 1",
            "description": "Test item for database operations",
            "created_at": datetime.now()  # Use Python datetime object
        }
        
        try:
            # Insert a record
            inserted = await db.insert(table_name, data, schema=schema)
            
            # Verify it has an ID
            assert "id" in inserted
            record_id = inserted["id"]
            
            # Fetch the record by ID
            fetched = await db.fetch_one(table_name, {"id": record_id}, schema=schema)
            
            # Verify the fetched record matches the inserted data
            assert fetched is not None
            for key, value in data.items():
                assert key in fetched
                # For datetime fields, just check type not exact value
                if key == "created_at":
                    assert isinstance(fetched[key], datetime)
                else:
                    assert fetched[key] == value
                    
            # Clean up
            await db.delete(table_name, {"id": record_id}, schema=schema)
        finally:
            # Drop the temporary table
            await db.execute_raw(f"DROP TABLE IF EXISTS {schema}.{table_name}")
    finally:
        await db.close()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_insert_and_fetch_project_schema():
    """Test inserting and fetching records in a project schema."""
    db = DBOperator()
    try:
        # Create a test schema
        test_schema = f"test_db_{uuid.uuid4().hex[:8]}"
        await db.execute_raw(f"CREATE SCHEMA IF NOT EXISTS {test_schema}")
        
        # Create a test table
        await db.execute_raw(
            f"""
            CREATE TABLE IF NOT EXISTS {test_schema}.test_items (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL,
                description TEXT,
                data JSONB,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
            """
        )
        
        # Test data
        table_name = "test_items"
        data = {
            "name": "Test Prompt",
            "description": "This is a test prompt with variables",
            "created_at": datetime.now()  # Use Python datetime object
        }
        
        try:
            # Insert a record
            inserted = await db.insert(table_name, data, schema=test_schema)
            
            # Verify it has an ID
            assert "id" in inserted
            record_id = inserted["id"]
            
            # Fetch the record by ID
            fetched = await db.fetch_one(table_name, {"id": record_id}, schema=test_schema)
            
            # Verify the fetched record matches the inserted data
            assert fetched is not None
            for key, value in data.items():
                assert key in fetched
                # For datetime fields, just check type not exact value
                if key == "created_at":
                    assert isinstance(fetched[key], datetime)
                else:
                    assert fetched[key] == value
        finally:
            # Drop schema regardless of test outcome
            await db.execute_raw(f"DROP SCHEMA IF EXISTS {test_schema} CASCADE")
    finally:
        await db.close()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_update_record():
    """Test updating a record."""
    db = DBOperator()
    try:
        # Create a test schema
        test_schema = f"test_db_{uuid.uuid4().hex[:8]}"
        await db.execute_raw(f"CREATE SCHEMA IF NOT EXISTS {test_schema}")
        
        # Create a test table
        await db.execute_raw(
            f"""
            CREATE TABLE IF NOT EXISTS {test_schema}.test_items (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL,
                description TEXT,
                data JSONB,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
            """
        )
        
        try:
            # Insert a test record
            record = await db.insert(
                "test_items",
                {
                    "name": "Item to Update",
                    "description": "This will be updated",
                    "created_at": datetime.now()  # Use Python datetime object
                },
                schema=test_schema
            )
            
            record_id = record["id"]
            
            # Update the record
            updated_values = {
                "name": "Updated Item Name",
                "description": "This has been updated"
            }
            
            updated = await db.update(
                "test_items",
                updated_values,
                {"id": record_id},
                schema=test_schema
            )
            
            # Verify update returned updated record or row count
            assert updated is not None
            if isinstance(updated, dict):
                # If it returns the updated record
                assert updated["name"] == updated_values["name"]
                assert updated["description"] == updated_values["description"]
            else:
                # If it returns number of rows updated
                assert updated >= 1
            
            # Fetch the updated record
            fetched = await db.fetch_one("test_items", {"id": record_id}, schema=test_schema)
            
            # Verify the update worked
            assert fetched["name"] == updated_values["name"]
            assert fetched["description"] == updated_values["description"]
        finally:
            # Drop schema regardless of test outcome
            await db.execute_raw(f"DROP SCHEMA IF EXISTS {test_schema} CASCADE")
    finally:
        await db.close()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_delete_record():
    """Test deleting a record."""
    db = DBOperator()
    try:
        # Create a test schema
        test_schema = f"test_db_{uuid.uuid4().hex[:8]}"
        await db.execute_raw(f"CREATE SCHEMA IF NOT EXISTS {test_schema}")
        
        # Create a test table
        await db.execute_raw(
            f"""
            CREATE TABLE IF NOT EXISTS {test_schema}.test_items (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL,
                description TEXT,
                data JSONB,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
            """
        )
        
        try:
            # Insert a test record
            record = await db.insert(
                "test_items",
                {
                    "name": "Item to Delete",
                    "description": "This will be deleted",
                    "created_at": datetime.now()  # Use Python datetime object
                },
                schema=test_schema
            )
            
            record_id = record["id"]
            
            # Verify it exists
            exists_before = await db.fetch_one("test_items", {"id": record_id}, schema=test_schema)
            assert exists_before is not None
            
            # Delete the record
            deleted = await db.delete(
                "test_items",
                {"id": record_id},
                schema=test_schema
            )
            
            # Verify delete returned number of rows deleted
            assert deleted >= 1
            
            # Verify it no longer exists
            exists_after = await db.fetch_one("test_items", {"id": record_id}, schema=test_schema)
            assert exists_after is None
        finally:
            # Drop schema regardless of test outcome
            await db.execute_raw(f"DROP SCHEMA IF EXISTS {test_schema} CASCADE")
    finally:
        await db.close()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_transaction_commit():
    """Test transaction commit functionality."""
    db = DBOperator()
    try:
        # Create a test schema
        test_schema = f"test_db_{uuid.uuid4().hex[:8]}"
        await db.execute_raw(f"CREATE SCHEMA IF NOT EXISTS {test_schema}")
        
        # Create a test table
        await db.execute_raw(
            f"""
            CREATE TABLE IF NOT EXISTS {test_schema}.test_items (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL,
                description TEXT,
                data JSONB,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
            """
        )
        
        try:
            # Insert directly without transaction first
            record = await db.insert(
                "test_items",
                {
                    "name": "Direct Insert",
                    "description": "Testing direct insert",
                    "created_at": datetime.now()  # Use Python datetime object
                },
                schema=test_schema
            )
            
            # Verify we can read it back
            assert "id" in record
            direct_id = record["id"]
            fetched = await db.fetch_one("test_items", {"id": direct_id}, schema=test_schema)
            assert fetched is not None
            
            # Now test transactions manually
            conn = await db._connector._pool.acquire()
            try:
                # Start a transaction 
                tx = conn.transaction()
                await tx.start()
                
                # Insert in transaction
                insert_query = f"""
                INSERT INTO {test_schema}.test_items 
                (name, description, created_at) 
                VALUES ($1, $2, $3) RETURNING *
                """
                
                tx_record = await conn.fetchrow(
                    insert_query, 
                    "Transaction Test Item", 
                    "Testing transaction commit", 
                    datetime.now()
                )
                
                # Get ID of the record
                tx_id = tx_record["id"]
                
                # Commit the transaction
                await tx.commit()
                
                # Verify the record exists after commit
                fetched = await db.fetch_one("test_items", {"id": tx_id}, schema=test_schema)
                assert fetched is not None
                assert fetched["name"] == "Transaction Test Item"
                
            finally:
                await db._connector._pool.release(conn)
                
        finally:
            # Drop schema regardless of test outcome
            await db.execute_raw(f"DROP SCHEMA IF EXISTS {test_schema} CASCADE")
    finally:
        await db.close()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_transaction_rollback():
    """Test transaction rollback functionality."""
    db = DBOperator()
    try:
        # Create a test schema
        test_schema = f"test_db_{uuid.uuid4().hex[:8]}"
        await db.execute_raw(f"CREATE SCHEMA IF NOT EXISTS {test_schema}")
        
        # Create a test table
        await db.execute_raw(
            f"""
            CREATE TABLE IF NOT EXISTS {test_schema}.test_items (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL,
                description TEXT,
                data JSONB,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
            """
        )
        
        try:
            # Testing rollbacks manually
            conn = await db._connector._pool.acquire()
            try:
                # Start a transaction 
                tx = conn.transaction()
                await tx.start()
                
                # Insert in transaction
                insert_query = f"""
                INSERT INTO {test_schema}.test_items 
                (name, description, created_at) 
                VALUES ($1, $2, $3) RETURNING *
                """
                
                tx_record = await conn.fetchrow(
                    insert_query, 
                    "Rollback Test Item", 
                    "Testing transaction rollback", 
                    datetime.now()
                )
                
                # Get ID of the record
                tx_id = tx_record["id"]
                
                # Rollback the transaction
                await tx.rollback()
                
                # Verify the record doesn't exist after rollback
                fetched = await db.fetch_one("test_items", {"id": tx_id}, schema=test_schema)
                assert fetched is None
                
            finally:
                await db._connector._pool.release(conn)
                
        finally:
            # Drop schema regardless of test outcome
            await db.execute_raw(f"DROP SCHEMA IF EXISTS {test_schema} CASCADE")
    finally:
        await db.close() 