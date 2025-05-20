"""
MODULE: services/database/examples/transaction_test_example.py
PURPOSE: Demonstrates how to use transaction isolation in database tests
CLASSES:
    - ProjectTests: Example test class for project-related functionality
FUNCTIONS:
    - None
DEPENDENCIES:
    - services.database: For database operations
    - services.database.testing: For transaction isolation
    - pytest: For test framework

This module provides practical examples of using the transaction isolation system
for database tests. It demonstrates how to use the `with_transaction` decorator
to ensure tests run in isolated transactions that are automatically rolled back,
preventing test side effects from affecting other tests.

Example usage:
Run this script with pytest:
```
pytest -xvs services/database/examples/transaction_test_example.py
```
"""

import pytest
from typing import Dict, Any, List

# Import database components
from services.database import DBOperator
from services.database.testing import with_transaction, TestTransactionManager

# Import service to test
from services.projects import ProjectService

class TestProjects:
    """
    Example test class for project-related functionality.
    
    This class demonstrates how to use the transaction isolation system
    to test database operations without side effects.
    """
    
    def setup_method(self):
        """Set up test environment before each test."""
        # Use e2e mode to connect to the test database
        self.db = DBOperator(test_mode="e2e")
        self.project_service = ProjectService(db=self.db)
        
    @with_transaction
    def test_create_project(self):
        """
        Test creating a project using transaction isolation.
        
        This test will create a project in the database, but the
        transaction will be rolled back after the test completes.
        """
        # Arrange: Prepare test data
        project_data = {
            "name": "Test Project",
            "slug": "test-project",
            "description": "A test project created in an isolated transaction",
            "status": "active"
        }
        
        # Act: Create the project
        project_id = self.project_service.create_project(project_data)
        
        # Assert: Project was created successfully
        assert project_id is not None, "Project ID should not be None"
        
        # Fetch the created project
        project = self.project_service.get_project_by_id(project_id)
        
        # Verify project data
        assert project is not None, "Project should exist"
        assert project["name"] == project_data["name"]
        assert project["slug"] == project_data["slug"]
        assert project["description"] == project_data["description"]
        
        # Even though we created a project, the transaction will be
        # rolled back automatically after the test completes
        
    @with_transaction
    def test_delete_project(self):
        """
        Test deleting a project using transaction isolation.
        
        This test will create a project, delete it, and then verify
        it was deleted, all within an isolated transaction.
        """
        # Arrange: Create a test project
        project_data = {
            "name": "Project to Delete",
            "slug": "project-to-delete",
            "description": "This project will be deleted",
            "status": "active"
        }
        project_id = self.project_service.create_project(project_data)
        
        # Act: Delete the project
        deleted = self.project_service.delete_project(project_id)
        
        # Assert: Project was deleted
        assert deleted is True, "Project deletion should return True"
        
        # Verify the project no longer exists
        project = self.project_service.get_project_by_id(project_id)
        assert project is None, "Project should not exist after deletion"
        
    @with_transaction
    def test_update_project(self):
        """
        Test updating a project using transaction isolation.
        
        This test will create a project, update it, and then verify
        the updates, all within an isolated transaction.
        """
        # Arrange: Create a test project
        project_data = {
            "name": "Original Project Name",
            "slug": "original-project",
            "description": "Original description",
            "status": "draft"
        }
        project_id = self.project_service.create_project(project_data)
        
        # Act: Update the project
        update_data = {
            "name": "Updated Project Name",
            "description": "Updated description",
            "status": "active"
        }
        updated = self.project_service.update_project(project_id, update_data)
        
        # Assert: Project was updated
        assert updated is True, "Project update should return True"
        
        # Verify the updates
        project = self.project_service.get_project_by_id(project_id)
        assert project is not None, "Project should exist"
        assert project["name"] == update_data["name"]
        assert project["description"] == update_data["description"]
        assert project["status"] == update_data["status"]
        # slug should not have changed
        assert project["slug"] == project_data["slug"]
        
if __name__ == "__main__":
    print("This module is intended to be run with pytest.")
    print("Run: pytest -xvs services/database/examples/transaction_test_example.py") 