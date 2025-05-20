"""
MODULE: services/database/utils/cursor_files/sample_operations.py
PURPOSE: Example of common database operations using the database service
FUNCTIONS:
    - insert_sample_data: Insert sample records into a table
    - export_table_data: Export table contents to JSON or CSV
    - run_sample_operations: Run all sample operations
DEPENDENCIES:
    - services.database: For database operations
    - asyncio: For async runtime
    
This file demonstrates how to perform common database operations using the
services/database package. You can use this as a template for your own
database interaction scripts.
"""

import asyncio
import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

from services.database import DBOperator, with_db_connection

async def insert_sample_data(schema: str, table: str) -> None:
    """
    Insert sample data into a table.
    
    Args:
        schema: Database schema name
        table: Table name
    """
    db = DBOperator()
    try:
        # Create sample data
        current_time = datetime.now().isoformat()
        sample_records = [
            {
                "name": f"Sample {i}",
                "description": f"This is sample record {i}",
                "created_at": current_time,
                "status": "active" if i % 2 == 0 else "inactive"
            }
            for i in range(1, 4)
        ]
        
        # Insert each record
        inserted = []
        for record in sample_records:
            try:
                result = await db.insert(table, record, schema=schema)
                inserted.append(result)
                print(f"Inserted record: {json.dumps(result, default=str)}")
            except Exception as e:
                print(f"Error inserting record: {str(e)}")
        
        print(f"Successfully inserted {len(inserted)} records")
        
    finally:
        await db.close()

@with_db_connection
async def get_data_with_decorator(conn, schema: str, table: str) -> List[Dict[str, Any]]:
    """
    Example showing how to use the with_db_connection decorator.
    
    Args:
        conn: Database connection (injected by decorator)
        schema: Database schema name
        table: Table name
        
    Returns:
        List of records from the table
    """
    # The conn object has all DBConnector methods available
    records = await conn.execute(
        f"SELECT * FROM {schema}.{table} LIMIT 10",
        fetch_all=True
    )
    
    return records

async def export_table_data(schema: str, table: str, format: str = "json") -> str:
    """
    Export table data to a file.
    
    Args:
        schema: Database schema name
        table: Table name
        format: Export format ("json" or "csv")
        
    Returns:
        Path to the exported file
    """
    db = DBOperator()
    try:
        # Fetch all records from the table
        records = await db.fetch(table, schema=schema)
        
        if not records:
            print(f"No records found in {schema}.{table}")
            return ""
            
        # Create output directory if it doesn't exist
        os.makedirs("data_exports", exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data_exports/{schema}_{table}_{timestamp}"
        
        if format == "json":
            # Export as JSON
            output_file = f"{filename}.json"
            with open(output_file, "w") as f:
                json.dump(records, f, indent=2, default=str)
                
        elif format == "csv":
            # Export as CSV
            output_file = f"{filename}.csv"
            with open(output_file, "w", newline="") as f:
                # Get fieldnames from first record
                fieldnames = records[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                # Write header and data
                writer.writeheader()
                writer.writerows(records)
        else:
            raise ValueError(f"Unsupported format: {format}")
            
        print(f"Exported {len(records)} records to {output_file}")
        return output_file
        
    finally:
        await db.close()

async def run_transaction_example(schema: str, table: str) -> None:
    """
    Example showing how to use transactions.
    
    Args:
        schema: Database schema name
        table: Table name
    """
    db = DBOperator()
    try:
        print("Starting transaction example...")
        
        async with db.transaction() as conn:
            # All operations in this block are part of the same transaction
            
            # Check if table exists
            if not await conn.table_exists(table, schema):
                print(f"Table {schema}.{table} does not exist")
                return
                
            # Get count of records before changes
            count_before = await conn.execute(
                f"SELECT COUNT(*) AS count FROM {schema}.{table}",
                fetch_val=True
            )
            print(f"Records before: {count_before}")
            
            # Insert new record
            new_record = {
                "name": "Transaction Test",
                "description": "Record added during transaction",
                "created_at": datetime.now().isoformat(),
                "status": "active"
            }
            
            await conn.execute(
                f"INSERT INTO {schema}.{table} (name, description, created_at, status) VALUES ($1, $2, $3, $4)",
                [new_record["name"], new_record["description"], new_record["created_at"], new_record["status"]]
            )
            
            # Update a record (this would fail if no records exist with status='active')
            updated = await conn.execute(
                f"UPDATE {schema}.{table} SET status = 'updated' WHERE status = 'active' RETURNING id",
                fetch_all=True
            )
            print(f"Updated {len(updated)} records")
            
            # If this point is reached without exceptions, the transaction will be committed
            
            # Get count after changes (still in transaction)
            count_after = await conn.execute(
                f"SELECT COUNT(*) AS count FROM {schema}.{table}",
                fetch_val=True
            )
            print(f"Records after: {count_after}")
            
        print("Transaction completed successfully")
        
    except Exception as e:
        print(f"Transaction failed: {str(e)}")
        # The transaction will be automatically rolled back
    finally:
        await db.close()

async def run_sample_operations() -> None:
    """
    Run all sample database operations.
    
    Usage:
    - Modify the schema and table variables to match your database
    - Call this function to execute all operations
    """
    # Set these to match your target schema and table
    schema = "public"  # Use a project schema name or "public"
    table = "products"  # Use a table that exists in your schema
    
    print(f"\n=== Sample Operations for {schema}.{table} ===\n")
    
    tasks = [
        # Comment out any operations you don't want to run
        # insert_sample_data(schema, table),
        # export_table_data(schema, table, "json"),
        # export_table_data(schema, table, "csv"),
        # run_transaction_example(schema, table)
    ]
    
    # Also demonstrate the decorator usage
    # records = await get_data_with_decorator(schema, table)
    # print(f"Records fetched with decorator: {len(records)}")
    
    # Run the enabled tasks
    for task in tasks:
        await task
        print("\n---\n")
    
    print("All operations completed")

if __name__ == "__main__":
    asyncio.run(run_sample_operations()) 