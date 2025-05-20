"""
MODULE: services/database/examples/db_operator_test_modes.py
PURPOSE: Demonstrates how to use different test modes with the DBOperator
CLASSES:
    - None
FUNCTIONS:
    - demo_production_mode: Demonstrate production mode usage
    - demo_e2e_mode: Demonstrate end-to-end test mode
    - demo_mock_mode: Demonstrate mock mode
    - main: Entry point for the example
DEPENDENCIES:
    - services.database: For database operations
    - functools: For decorator utilities

This module provides practical examples of using the DBOperator with different
test modes: production, e2e (end-to-end), and mock. It demonstrates how to
configure the DBOperator for testing in different environments.

Example usage:
```
python services/database/examples/db_operator_test_modes.py
```
"""

import json
import sys
from typing import Dict, Any, List, Optional, Callable
from functools import wraps

# Import database components
from services.database import DBOperator, SchemaRegistry

def pretty_print(data: Any) -> None:
    """Pretty print data as JSON."""
    print(json.dumps(data, indent=2, default=str))

def db_operation(mode: Optional[str] = None):
    """
    Decorator for configuring database operations with a test mode.
    
    Args:
        mode: The test mode to use ('mock', 'e2e', or None for production)
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create the appropriate DBOperator based on the mode
            db = DBOperator(test_mode=mode)
            
            # If using mock mode, set up mock data
            if mode == 'mock':
                registry = SchemaRegistry()
                registry.initialize()
                db.schema_registry = registry
                
            # Pass the DBOperator to the function
            return func(db, *args, **kwargs)
        return wrapper
    return decorator

@db_operation(mode=None)  # Production mode (no test mode)
def demo_production_mode(db: DBOperator) -> None:
    """
    Demonstrate using the DBOperator in production mode.
    
    Args:
        db: The database operator instance
    """
    print("\n=== Production Mode Example ===\n")
    print("Using production database connection:")
    print(f"  Connection URL: {db.connection_url}")
    print(f"  Test Mode: {db.test_mode}")
    
    print("\nIn production mode:")
    print("1. Connects to the real production database")
    print("2. Executes real queries against the database")
    print("3. Changes are persistent and affect the real data")
    
    print("\nExample query (not executed to protect production data):")
    print("  db.fetch_all('SELECT * FROM public.users LIMIT 5')")
    
    # Not executing real queries in this example to avoid affecting production data
    
@db_operation(mode='e2e')  # End-to-end test mode
def demo_e2e_mode(db: DBOperator) -> None:
    """
    Demonstrate using the DBOperator in end-to-end test mode.
    
    Args:
        db: The database operator instance
    """
    print("\n=== End-to-End Test Mode Example ===\n")
    print("Using test database connection:")
    print(f"  Connection URL: {db.connection_url}")
    print(f"  Test Mode: {db.test_mode}")
    
    print("\nIn e2e mode:")
    print("1. Connects to a test database instead of production")
    print("2. Executes real queries against the test database")
    print("3. Changes are persistent in the test database")
    print("4. Should be used within transaction isolation when appropriate")
    
    print("\nExample query:")
    schema_names = db.fetch_all("""
        SELECT schema_name 
        FROM information_schema.schemata 
        WHERE schema_name LIKE 'prj\_%'
    """)
    
    print("\nProject schemas in test database:")
    for schema in schema_names:
        print(f"  - {schema['schema_name']}")
    
    print("\nTables in first project schema:")
    if schema_names:
        first_schema = schema_names[0]['schema_name']
        tables = db.fetch_all(f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = '{first_schema}'
        """)
        
        for table in tables:
            print(f"  - {table['table_name']}")
    
@db_operation(mode='mock')  # Mock mode
def demo_mock_mode(db: DBOperator) -> None:
    """
    Demonstrate using the DBOperator in mock mode.
    
    Args:
        db: The database operator instance
    """
    print("\n=== Mock Mode Example ===\n")
    print("Using mock database connection:")
    print(f"  Connection URL: {db.connection_url}")
    print(f"  Test Mode: {db.test_mode}")
    
    print("\nIn mock mode:")
    print("1. No actual database connection is established")
    print("2. Queries return mock data that mimics the schema structure")
    print("3. Changes are not persisted anywhere")
    print("4. Fast and doesn't require a test database")
    
    print("\nExample fetch_one query:")
    user = db.fetch_one("SELECT * FROM public.users WHERE id = %s", (1,))
    print("\nMock user data:")
    pretty_print(user)
    
    print("\nExample fetch_all query:")
    posts = db.fetch_all("SELECT * FROM public.posts WHERE user_id = %s LIMIT 3", (user['id'],))
    print(f"\nMock posts data ({len(posts)} records):")
    pretty_print(posts)
    
    print("\nExample insert operation:")
    new_user_id = db.insert("public", "users", {
        "name": "Test User",
        "email": "test@example.com",
        "status": "active"
    })
    print(f"Inserted mock user with ID: {new_user_id}")
    
    print("\nExample update operation:")
    rows_updated = db.update("public", "users", new_user_id, {
        "name": "Updated Name",
        "status": "inactive"
    })
    print(f"Updated {rows_updated} mock rows")
    
    print("\nMock data is schema-aware and preserves referential integrity in returned data")

def main() -> None:
    """
    Entry point for the database test modes example.
    """
    print("\n=== DBOperator Test Modes Example ===")
    print("This example demonstrates the three test modes available for DBOperator:")
    print("1. Production mode (no test_mode)")
    print("2. End-to-end test mode (test_mode='e2e')")
    print("3. Mock mode (test_mode='mock')")
    
    # Decide which demos to run
    run_production = False  # Set to True if you want to see production mode (be careful!)
    run_e2e = True
    run_mock = True
    
    # Run the selected demos
    if run_production:
        demo_production_mode()
    
    if run_e2e:
        try:
            demo_e2e_mode()
        except Exception as e:
            print(f"\nError in e2e mode demo: {e}")
            print("Make sure your test database is properly configured.")
    
    if run_mock:
        demo_mock_mode()
    
    print("\n=== Example Complete ===\n")

if __name__ == "__main__":
    main() 