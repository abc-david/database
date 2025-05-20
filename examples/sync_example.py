"""
MODULE: services/database/examples/sync_example.py
PURPOSE: Demonstrates how to use the database synchronization tools
CLASSES:
    - None
FUNCTIONS:
    - main: Entry point for the example
DEPENDENCIES:
    - services.database.sync: For database synchronization
    - pathlib: For path manipulation
    - os: For environment variables

This module provides a practical example of using the database synchronization
tools to export and import database schemas, tables, and data. It demonstrates
how to use the DatabaseSyncManager to create dumps, restore from dumps, and
synchronize databases across environments.

Example usage:
```
python services/database/examples/sync_example.py
```
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Import sync components
from services.database.sync import DatabaseSyncManager

def main() -> None:
    """
    Entry point for the database synchronization example.
    
    This function demonstrates how to use the DatabaseSyncManager
    to perform various database synchronization operations.
    """
    print("\n=== Database Synchronization Example ===\n")
    
    # Create a sync manager for the test database
    print("1. Creating DatabaseSyncManager...")
    sync_manager = DatabaseSyncManager(
        db_name="contentgen_test_db",
        db_user="test_runner_user",
        db_password="test123",
        db_host="localhost",
        db_port=5432
    )
    print("   DatabaseSyncManager created successfully!")
    
    # Define the dump directory
    dump_dir = Path.home() / "python/projects/content_generator/db_dumps"
    os.makedirs(dump_dir, exist_ok=True)
    
    # Example 1: Create a full database dump
    print("\n2. Example 1: Creating a full database dump...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dump_file = dump_dir / f"full_dump_{timestamp}.sql"
    
    success = sync_manager.create_dump(
        output_file=str(dump_file),
        include_schemas=True,
        include_data=True
    )
    
    if success:
        print(f"   Full dump created successfully at: {dump_file}")
        dump_size = dump_file.stat().st_size / 1024  # Size in KB
        print(f"   Dump size: {dump_size:.2f} KB")
    else:
        print("   Failed to create full dump")
        return
    
    # Example 2: Create a schema-only dump
    print("\n3. Example 2: Creating a schema-only dump...")
    schema_dump_file = dump_dir / f"schema_only_{timestamp}.sql"
    
    success = sync_manager.create_dump(
        output_file=str(schema_dump_file),
        include_schemas=True,
        include_data=False
    )
    
    if success:
        print(f"   Schema-only dump created successfully at: {schema_dump_file}")
    else:
        print("   Failed to create schema-only dump")
    
    # Example 3: Create a filtered dump (specific schemas)
    print("\n4. Example 3: Creating a filtered dump (specific schemas)...")
    filtered_dump_file = dump_dir / f"filtered_dump_{timestamp}.sql"
    
    success = sync_manager.create_dump(
        output_file=str(filtered_dump_file),
        schemas=["prj_b2b_saas", "prj_rel_iques_t"],
        include_schemas=True,
        include_data=True
    )
    
    if success:
        print(f"   Filtered dump created successfully at: {filtered_dump_file}")
    else:
        print("   Failed to create filtered dump")
    
    # Example 4: List available dumps
    print("\n5. Example 4: Listing available dumps...")
    dumps = list(dump_dir.glob("*.sql"))
    print(f"   Found {len(dumps)} dumps:")
    for i, dump in enumerate(sorted(dumps, key=lambda f: f.stat().st_mtime, reverse=True)):
        size_kb = dump.stat().st_size / 1024
        modified = datetime.fromtimestamp(dump.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        print(f"   {i+1}. {dump.name} ({size_kb:.2f} KB, modified: {modified})")
    
    # Example 5: Explain how to restore from a dump
    print("\n6. Example 5: How to restore from a dump...")
    print("   To restore from a dump, you would use:")
    print(f"   sync_manager.restore_dump('{filtered_dump_file}')\n")
    print("   Note: This example doesn't actually restore the dump to avoid overwriting your database.")
    
    # Example 6: Explain database synchronization between environments
    print("\n7. Example 6: Database synchronization between environments...")
    print("   To synchronize from another environment:")
    print("   1. SSH into the remote environment")
    print("   2. Create a dump file")
    print("   3. Transfer the dump file to the local machine")
    print("   4. Restore from the dump file")
    print("\n   Example command sequence:")
    print("   $ ssh production_server")
    print("   $ python -m services.database.sync.cli dump --output=/tmp/prod_dump.sql")
    print("   $ exit")
    print("   $ scp production_server:/tmp/prod_dump.sql ./local_prod_dump.sql")
    print("   $ python -m services.database.sync.cli restore --input=./local_prod_dump.sql")
    
    print("\n=== Example Complete ===\n")
    
    # Clean up example dumps (optional)
    print("Would you like to clean up the example dumps? (y/n)")
    response = input().strip().lower()
    if response == 'y':
        for dump in dumps:
            if dump.name.startswith(("full_dump_", "schema_only_", "filtered_dump_")) and timestamp in dump.name:
                dump.unlink()
                print(f"Deleted: {dump.name}")
        print("Cleanup complete!")

if __name__ == "__main__":
    main() 