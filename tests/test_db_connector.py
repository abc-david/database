"""
MODULE: services/database/tests/test_db_connector.py
PURPOSE: Tests for the database connector module
DEPENDENCIES:
    - pytest: For testing and async support
    - asyncio: For async/await support

This module contains tests for the database connector functionality,
including connection pooling, query execution, and transaction management.
"""

import pytest
import asyncio
import logging
from unittest.mock import patch, MagicMock, call

# Import the module under test
from services.database.db_connector import DBConnector

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_db_connector_init():
    """Test that DBConnector initializes correctly."""
    # Create instance
    db = DBConnector()
    try:
        # Initialize the pool
        pool = await db.get_pool()
        assert pool is not None
    finally:
        # Clean up
        await db.close()

@pytest.mark.asyncio
async def test_db_connector_execute_query():
    """Test that DBConnector can execute a simple query."""
    # Create instance
    db = DBConnector()
    try:
        # Execute a simple query
        result = await db.execute("SELECT 1 as test", fetch_val=True)
        assert result == 1
    finally:
        # Clean up
        await db.close()

@pytest.mark.asyncio
async def test_db_connector_simple_operations():
    """Test basic DB operations without using the transaction manager."""
    # Create instance
    db = DBConnector()
    try:
        # Create a temporary table for testing
        await db.execute(
            """
            CREATE TEMPORARY TABLE test_ops (
                id SERIAL PRIMARY KEY,
                name TEXT
            )
            """
        )
        
        # Insert record
        await db.execute(
            "INSERT INTO test_ops (name) VALUES ($1)",
            ("test_record",)
        )
        
        # Query the record
        name = await db.execute(
            "SELECT name FROM test_ops WHERE id = 1",
            fetch_val=True
        )
        
        # Verify record
        assert name == "test_record"
        
        # Get count
        count = await db.execute(
            "SELECT COUNT(*) FROM test_ops",
            fetch_val=True
        )
        
        # Verify count
        assert count == 1
        
    finally:
        # Clean up
        await db.close() 