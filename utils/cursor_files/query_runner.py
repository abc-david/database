"""
MODULE: services/database/utils/cursor_files/query_runner.py
PURPOSE: Utility script for direct database access without psql
FUNCTIONS:
    - run_query: Execute SQL queries against the database
    - main: Parse arguments and run queries
DEPENDENCIES:
    - services.database: For database operations
    - argparse: For command line argument parsing
    - asyncio: For async runtime
    - json: For parameter parsing and result formatting

This script provides a command-line interface for executing arbitrary SQL
queries against the database for debugging and testing purposes.
"""

import asyncio
import json
import sys
import argparse
from typing import Dict, List, Any, Optional, Union

from services.database import DBConnector

async def run_query(
    query: str,
    params: Optional[List[Any]] = None,
    fetch: str = "all",
    schema: Optional[str] = None
) -> Union[Dict, List[Dict], Any]:
    """
    Execute a SQL query and return the results.
    
    Args:
        query: SQL query to execute
        params: Query parameters (optional)
        fetch: Fetch mode - 'val' (single value), 'row' (single row), 'all' (all rows)
        schema: Database schema name (optional)
        
    Returns:
        Query results based on the fetch mode
    """
    conn = DBConnector()
    try:
        fetch_val = fetch == "val"
        fetch_row = fetch == "row"
        fetch_all = fetch == "all"
        
        result = await conn.execute(
            query,
            params,
            fetch_val=fetch_val,
            fetch_row=fetch_row,
            fetch_all=fetch_all,
            schema=schema
        )
        
        # Convert to JSON-serializable format
        if isinstance(result, list):
            # Handle list of records
            for i, record in enumerate(result):
                if hasattr(record, 'items'):  # Dict-like object
                    result[i] = {k: v for k, v in record.items()}
        elif result and hasattr(result, 'items'):
            # Handle single dict-like record
            result = {k: v for k, v in result.items()}
            
        # Print the results
        print(json.dumps(result, indent=2, default=str))
        return result
    finally:
        await conn.close()

async def inspect_database(schema_filter: Optional[str] = None) -> None:
    """
    Inspect the database structure and list schemas and tables.
    
    Args:
        schema_filter: Optional schema name to filter results
    """
    conn = DBConnector()
    try:
        # Get all schemas
        schemas = await conn.execute(
            "SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN ('pg_catalog', 'information_schema')",
            fetch_all=True
        )
        
        print("Available schemas:")
        for schema in schemas:
            schema_name = schema['schema_name']
            if schema_filter and schema_filter != schema_name:
                continue
                
            print(f"- {schema_name}")
            
            # Get tables for this schema
            tables = await conn.execute(
                """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = $1
                ORDER BY table_name
                """,
                [schema_name],
                fetch_all=True
            )
            
            if tables:
                print(f"  Tables:")
                for table in tables:
                    table_name = table['table_name']
                    print(f"  - {table_name}")
                    
                    # Get column information
                    columns = await conn.execute(
                        """
                        SELECT column_name, data_type 
                        FROM information_schema.columns 
                        WHERE table_schema = $1 AND table_name = $2
                        ORDER BY ordinal_position
                        """,
                        [schema_name, table_name],
                        fetch_all=True
                    )
                    
                    if columns:
                        for column in columns:
                            print(f"    • {column['column_name']} ({column['data_type']})")
            print()
    finally:
        await conn.close()

def main():
    """Parse command line arguments and run the appropriate function."""
    parser = argparse.ArgumentParser(description="Database query utility for testing and debugging.")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Execute a SQL query")
    query_parser.add_argument("--query", "-q", required=True, help="SQL query to execute")
    query_parser.add_argument("--params", "-p", help="Parameters as JSON string")
    query_parser.add_argument("--fetch", choices=["val", "row", "all"], default="all", help="Fetch mode")
    query_parser.add_argument("--schema", "-s", help="Database schema")
    
    # Inspect command
    inspect_parser = subparsers.add_parser("inspect", help="Inspect database structure")
    inspect_parser.add_argument("--schema", "-s", help="Filter by schema name")
    
    args = parser.parse_args()
    
    if args.command == "query":
        params = json.loads(args.params) if args.params else None
        asyncio.run(run_query(args.query, params, args.fetch, args.schema))
    elif args.command == "inspect":
        asyncio.run(inspect_database(args.schema))
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 