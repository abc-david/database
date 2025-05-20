"""
MODULE: services/database/tests/test_simple.py
PURPOSE: Simple test for debugging database connection
"""

import pytest
import asyncio
from datetime import datetime

from services.database import DBOperator


@pytest.mark.asyncio
async def test_simple_query():
    """Test a simple database query without using fixtures."""
    # Create DB operator directly in the test
    db = DBOperator()
    
    try:
        print("TEST RUNNING")
        print(f"DB TYPE IN TEST: {type(db)}")
        
        # Create a test table
        await db.execute_raw(
            """
            CREATE TABLE IF NOT EXISTS public.test_simple (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
            """
        )
        
        try:
            # Insert using a datetime object
            now = datetime.now()
            data = {
                "name": "Test Item",
                "created_at": now  # Use Python datetime object
            }
            
            # Insert a record
            record = await db.insert("test_simple", data, schema="public")
            print(f"INSERTED: {record}")
            
            # Check that it got an ID
            assert "id" in record
            
            # Fetch it back
            fetched = await db.fetch_one("test_simple", {"id": record["id"]}, schema="public")
            print(f"FETCHED: {fetched}")
            
            # Clean up
            await db.delete("test_simple", {"id": record["id"]}, schema="public")
            
        finally:
            # Drop the test table
            await db.execute_raw("DROP TABLE IF EXISTS public.test_simple")
            
    finally:
        # Close the connection
        await db.close() 