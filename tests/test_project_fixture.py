"""
MODULE: services/database/tests/test_project_fixture.py
PURPOSE: Provide a local test_project fixture for database tests
"""

import pytest
import uuid

@pytest.fixture
async def test_project():
    """
    Provide a test project schema name for isolated database testing.
    
    This is a simplified version of the global test_project fixture,
    allowing database tests to run independently.
    """
    # Create a unique schema name for this test session
    schema_name = f"test_db_{uuid.uuid4().hex[:8]}"
    
    # Return the schema name
    return schema_name 