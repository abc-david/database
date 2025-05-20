"""
MODULE: services/database/scripts/example_usage.py
PURPOSE: Demonstrate usage of the database services
DEPENDENCIES:
    - services.database: For database operations
    - config.settings: For database configuration

This script demonstrates how to use the database services for common operations.
It includes examples of using DBConnector, DBOperator, and the with_db_connection
decorator.
"""

import logging
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import database modules
from services.database.db_connector import DBConnector, with_db_connection
from services.database.db_operator import DBOperator
from services.database.validation import ObjectValidator
from services.database.utils.connection_helpers import format_db_error

def main():
    """Main function demonstrating database service usage."""
    logger.info("Demonstrating database service usage")
    
    try:
        # Using DBConnector directly
        demonstrate_db_connector()
        
        # Using DBOperator for higher-level operations
        demonstrate_db_operator()
        
        # Using with_db_connection decorator
        demonstrate_with_db_connection()
        
        # Using validation
        demonstrate_validation()
        
        logger.info("Database service demonstration completed successfully")
        
    except Exception as e:
        error_info = format_db_error(e)
        logger.error(f"Error in database demonstration: {error_info['message']}")
        return 1
        
    return 0

def demonstrate_db_connector():
    """Demonstrate use of DBConnector."""
    logger.info("=== DBConnector Examples ===")
    
    # Create a connector instance
    db = DBConnector()
    
    # Use as a context manager for transaction safety
    with db:
        # Fetch multiple records
        users = db.fetch_all(
            "SELECT * FROM prompts WHERE name = %s LIMIT 5",
            ("active",)
        )
        logger.info(f"Found {len(users)} active users")
        
        # Fetch a single record
        user = db.fetch_one(
            "SELECT * FROM prompts WHERE id = %s",
            ("user-123",)
        )
        logger.info(f"User details: {user}")
        
        # Execute a simple query
        status = db.execute(
            "UPDATE users SET last_login = %s WHERE id = %s",
            (datetime.now(), "user-123")
        )
        logger.info(f"Update status: {status}")
        
        # Insert a record
        new_user = db.insert(
            table="users",
            data={
                "name": "Test User",
                "email": "test@example.com",
                "status": "active",
                "created_at": datetime.now()
            },
            returning=["id", "name", "email"]
        )
        logger.info(f"Inserted new user: {new_user}")

def demonstrate_db_operator():
    """Demonstrate use of DBOperator."""
    logger.info("=== DBOperator Examples ===")
    
    # Create an operator instance
    db_op = DBOperator()
    
    # Use transaction context manager
    with db_op.transaction():
        # Get a record by ID
        site = db_op.get_by_id(
            table="sites",
            record_id="site-123"
        )
        logger.info(f"Site details: {site}")
        
        # Get multiple records with condition
        templates = db_op.get_all(
            table="templates",
            condition={"site_id": "site-123", "status": "active"},
            order_by="created_at DESC",
            limit=5
        )
        logger.info(f"Found {len(templates)} active templates")
        
        # Insert a record
        new_template = db_op.create(
            table="templates",
            data={
                "site_id": "site-123",
                "name": "New Template",
                "content": {"blocks": []},
                "status": "draft",
                "created_at": datetime.now()
            },
            returning=["id", "name", "status"]
        )
        logger.info(f"Created new template: {new_template}")
        
        # Update a record by ID
        updated = db_op.update_by_id(
            table="templates",
            record_id=new_template["id"],
            data={"status": "active", "updated_at": datetime.now()},
            returning=["id", "name", "status"]
        )
        logger.info(f"Updated template: {updated}")
        
        # Execute custom query
        result = db_op.execute_raw(
            "UPDATE templates SET last_used = %s WHERE id = %s",
            (datetime.now(), new_template["id"])
        )
        logger.info(f"Custom update result: {result}")
        
        # Check if a record exists
        exists = db_op.exists(
            table="templates",
            condition={"id": new_template["id"]}
        )
        logger.info(f"Template exists: {exists}")
        
        # Count records
        count = db_op.count(
            table="templates",
            condition={"site_id": "site-123"}
        )
        logger.info(f"Template count: {count}")

@with_db_connection
def demonstrate_with_db_connection(conn):
    """Demonstrate use of with_db_connection decorator."""
    logger.info("=== with_db_connection Examples ===")
    
    # Use the connection directly
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        logger.info(f"Total user count: {count}")
        
        cursor.execute("SELECT COUNT(*) FROM templates")
        count = cursor.fetchone()[0]
        logger.info(f"Total template count: {count}")
        
    # Connection is automatically committed and returned to pool

def demonstrate_validation():
    """Demonstrate use of ObjectValidator."""
    logger.info("=== ObjectValidator Examples ===")
    
    from pydantic import BaseModel, Field
    from typing import Optional
    
    # Define a Pydantic model
    class User(BaseModel):
        id: Optional[str] = None
        name: str
        email: str
        status: str = "active"
        login_count: int = 0
        
    # Create validator
    validator = ObjectValidator()
    
    # Validate valid data
    valid_data = {
        "name": "Test User",
        "email": "test@example.com"
    }
    
    result = validator.validate_with_model(valid_data, User)
    logger.info(f"Valid data result: {result.is_valid}")
    logger.info(f"Validated data: {result.validated_data}")
    
    # Validate invalid data
    invalid_data = {
        "name": "Test User",
        "email": 12345,  # Should be a string
        "status": "unknown"  # Valid but not default
    }
    
    result = validator.validate_with_model(invalid_data, User)
    logger.info(f"Invalid data result: {result.is_valid}")
    if not result.is_valid:
        logger.info(f"Validation errors: {result.errors}")

if __name__ == "__main__":
    sys.exit(main()) 