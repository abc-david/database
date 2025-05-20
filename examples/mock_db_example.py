"""
MODULE: services/database/examples/mock_db_example.py
PURPOSE: Demonstrates how to use the mock database system with DBOperator
CLASSES:
    - None
FUNCTIONS:
    - main: Entry point for the example
DEPENDENCIES:
    - services.database: For database operations
    - services.database.mock: For mock data generation
    - json: For pretty printing

This module provides a practical example of using the schema-aware mock database
system in conjunction with the DBOperator class. It shows how to configure the
DBOperator to use the mock system for testing, and how to generate realistic
mock data that respects the database schema.

Example usage:
Run this script to see how the mock database system works with DBOperator.
The script will demonstrate:
1. Creating a DBOperator in mock mode
2. Performing various database operations with mock data
3. Validating mock data against the schema
"""

import json
from typing import Dict, Any, List, Optional

# Import database components
from services.database import DBOperator, SchemaRegistry, MockDataGenerator

def pretty_print(data: Any) -> None:
    """
    Pretty print data as JSON.
    
    Args:
        data: Data to print
    """
    print(json.dumps(data, indent=2, default=str))

def main() -> None:
    """
    Entry point for the mock database example.
    """
    print("\n=== Mock Database Example ===\n")
    
    # Create a schema registry and initialize it
    print("1. Creating schema registry...")
    registry = SchemaRegistry()
    registry.initialize()
    print("   Schema registry initialized successfully!")
    
    # Create a mock data generator
    print("\n2. Creating mock data generator...")
    generator = MockDataGenerator(registry)
    print("   Mock data generator created successfully!")
    
    # Create a DBOperator in mock mode
    print("\n3. Creating DBOperator in mock mode...")
    db = DBOperator(test_mode="mock")
    db.schema_registry = registry  # Provide our schema registry
    print("   DBOperator created in mock mode!")
    
    # Example 1: Fetch a single row
    print("\n4. Example 1: Fetching a single row from 'users' table...")
    user = db.fetch_one("SELECT * FROM public.users WHERE id = %s", (1,))
    print("   Fetched mock user:")
    pretty_print(user)
    
    # Example 2: Fetch multiple rows
    print("\n5. Example 2: Fetching multiple rows from 'posts' table...")
    posts = db.fetch_all("SELECT * FROM public.posts WHERE user_id = %s", (user.get('id'),))
    print(f"   Fetched {len(posts)} mock posts:")
    pretty_print(posts)
    
    # Example 3: Insert data
    print("\n6. Example 3: Inserting data into 'users' table...")
    new_user_data = {
        "name": "Example User",
        "email": "example@example.com",
        "status": "active"
    }
    
    # Validate the data against the schema
    is_valid, error = registry.validate_insert_data("public", "users", new_user_data)
    if is_valid:
        print("   Validation passed!")
        user_id = db.insert("public", "users", new_user_data)
        print(f"   Inserted mock user with ID: {user_id}")
    else:
        print(f"   Validation failed: {error}")
    
    # Example 4: Generate related data
    print("\n7. Example 4: Generating related data...")
    related_data = generator.generate_related_rows(
        "public", "users",
        {
            "posts": {"count": 3, "fk_column": "user_id"},
            "comments": {"count": 5, "fk_column": "user_id"}
        },
        count=2  # Generate 2 users with related data
    )
    
    print("   Generated related data:")
    print(f"   - {len(related_data['users'])} users")
    print(f"   - {len(related_data['posts'])} posts")
    print(f"   - {len(related_data['comments'])} comments")
    
    # Example 5: Mock query result
    print("\n8. Example 5: Generating mock query result...")
    query = """
        SELECT u.*, COUNT(p.id) as post_count
        FROM public.users u
        LEFT JOIN public.posts p ON u.id = p.user_id
        GROUP BY u.id
        ORDER BY post_count DESC
        LIMIT 5
    """
    
    result = generator.generate_mock_query_result(query, row_count=5)
    print("   Generated mock query result:")
    pretty_print(result)
    
    print("\n=== Example Complete ===\n")

if __name__ == "__main__":
    main() 