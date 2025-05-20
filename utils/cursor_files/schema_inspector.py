"""
MODULE: services/database/utils/cursor_files/schema_inspector.py
PURPOSE: Utility for inspecting and verifying database schemas
FUNCTIONS:
    - inspect_schema: Check schema structure and table definitions
    - compare_schemas: Compare tables between two schemas
    - diagnose_schema_issues: Identify and report schema problems
DEPENDENCIES:
    - services.database: For database operations
    - asyncio: For async runtime

This utility helps diagnose schema-related issues by inspecting schema structures,
comparing schemas, and identifying missing or mismatched tables and columns.
It also provides support for test schema validation against model schemas.
"""

import asyncio
import json
import sys
import argparse
from typing import Dict, List, Any, Optional, Set, Tuple

from services.database import SchemaSetup, DBConnector, SQL_TEMPLATES, get_required_tables

class SchemaInspector:
    """
    Utility class for inspecting database schemas and tables.
    
    This class provides methods to:
    1. Inspect schema structures
    2. Compare tables between schemas
    3. Identify missing tables and columns
    4. Diagnose common schema issues
    5. Support test environment validation
    """
    
    def __init__(self):
        """Initialize the schema inspector."""
        self.db = DBConnector()
        self.setup = SchemaSetup()
    
    async def close(self):
        """Close database connections."""
        await self.db.close()
        await self.setup.close()
        
    async def inspect_schema(self, schema_name: str) -> Dict[str, Any]:
        """
        Inspect a database schema and its tables.
        
        Args:
            schema_name: The schema to inspect
            
        Returns:
            Dict containing schema information and table structures
        """
        # Check if schema exists
        schema_exists = await self.setup._schema_exists(schema_name)
        if not schema_exists:
            print(f"Schema '{schema_name}' does not exist")
            return {"exists": False}
            
        # Get tables in schema
        tables = await self.setup._get_existing_tables(schema_name)
        
        # Collect detailed information for each table
        tables_info = {}
        for table in tables:
            # Get column information
            columns = await self.db.execute(
                """
                SELECT 
                    column_name, 
                    data_type, 
                    is_nullable, 
                    column_default
                FROM 
                    information_schema.columns 
                WHERE 
                    table_schema = $1 
                    AND table_name = $2
                ORDER BY 
                    ordinal_position
                """,
                [schema_name, table],
                fetch_all=True
            )
            
            # Get primary key information
            primary_keys = await self.db.execute(
                """
                SELECT 
                    kcu.column_name
                FROM 
                    information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                      ON tc.constraint_name = kcu.constraint_name
                      AND tc.table_schema = kcu.table_schema
                WHERE 
                    tc.constraint_type = 'PRIMARY KEY'
                    AND tc.table_schema = $1
                    AND tc.table_name = $2
                """,
                [schema_name, table],
                fetch_all=True
            )
            
            # Get indexes
            indexes = await self.db.execute(
                """
                SELECT
                    indexname,
                    indexdef
                FROM
                    pg_indexes
                WHERE
                    schemaname = $1
                    AND tablename = $2
                """,
                [schema_name, table],
                fetch_all=True
            )
            
            # Store table information
            tables_info[table] = {
                "columns": columns,
                "primary_keys": [pk["column_name"] for pk in primary_keys],
                "indexes": indexes
            }
        
        # Check for required tables
        schema_type = "public" if schema_name == "public" else "project"
        required_tables = get_required_tables(schema_type)
        missing_tables = [table for table in required_tables if table not in tables]
        
        return {
            "exists": True,
            "name": schema_name,
            "tables": tables,
            "tables_info": tables_info,
            "required_tables": required_tables,
            "missing_tables": missing_tables
        }
    
    async def compare_schemas(self, source_schema: str, target_schema: str) -> Dict[str, Any]:
        """
        Compare two schemas and identify differences.
        
        Args:
            source_schema: The source schema to compare from
            target_schema: The target schema to compare to
            
        Returns:
            Dict containing comparison results
        """
        # Get schema information
        source_info = await self.inspect_schema(source_schema)
        target_info = await self.inspect_schema(target_schema)
        
        if not source_info["exists"]:
            return {"error": f"Source schema '{source_schema}' does not exist"}
            
        if not target_info["exists"]:
            return {"error": f"Target schema '{target_schema}' does not exist"}
        
        # Compare tables
        source_tables = set(source_info["tables"])
        target_tables = set(target_info["tables"])
        
        tables_only_in_source = source_tables - target_tables
        tables_only_in_target = target_tables - source_tables
        common_tables = source_tables & target_tables
        
        # Compare columns in common tables
        column_differences = {}
        for table in common_tables:
            source_columns = {col["column_name"]: col for col in source_info["tables_info"][table]["columns"]}
            target_columns = {col["column_name"]: col for col in target_info["tables_info"][table]["columns"]}
            
            source_col_names = set(source_columns.keys())
            target_col_names = set(target_columns.keys())
            
            # Find differences
            cols_only_in_source = source_col_names - target_col_names
            cols_only_in_target = target_col_names - source_col_names
            
            # Check for type differences in common columns
            type_diffs = []
            for col in source_col_names & target_col_names:
                source_type = source_columns[col]["data_type"]
                target_type = target_columns[col]["data_type"]
                
                if source_type != target_type:
                    type_diffs.append({
                        "column": col,
                        "source_type": source_type,
                        "target_type": target_type
                    })
            
            if cols_only_in_source or cols_only_in_target or type_diffs:
                column_differences[table] = {
                    "only_in_source": list(cols_only_in_source),
                    "only_in_target": list(cols_only_in_target),
                    "type_differences": type_diffs
                }
        
        return {
            "tables_only_in_source": list(tables_only_in_source),
            "tables_only_in_target": list(tables_only_in_target),
            "common_tables": list(common_tables),
            "column_differences": column_differences
        }
    
    async def diagnose_schema_issues(self, schema_name: str) -> Dict[str, Any]:
        """
        Diagnose common schema issues and suggest fixes.
        
        Args:
            schema_name: The schema to diagnose
            
        Returns:
            Dict containing diagnostic results and suggested fixes
        """
        # Get schema information
        schema_info = await self.inspect_schema(schema_name)
        
        if not schema_info["exists"]:
            return {"error": f"Schema '{schema_name}' does not exist"}
        
        issues = []
        
        # Check for missing required tables
        if schema_info["missing_tables"]:
            issues.append({
                "type": "missing_tables",
                "message": f"Missing required tables: {schema_info['missing_tables']}",
                "suggested_fix": "Run schema_setup.py to create missing tables"
            })
        
        # Check for missing primary keys
        for table, info in schema_info["tables_info"].items():
            if not info["primary_keys"]:
                issues.append({
                    "type": "missing_primary_key",
                    "message": f"Table '{table}' has no primary key",
                    "suggested_fix": f"Add a primary key to table '{schema_name}.{table}'"
                })
        
        # Check for indexes on commonly queried columns
        common_indexed_columns = {
            "content": ["content_type", "created_at"],
            "prompts": ["prompt_type"],
            "object_models": ["name"]
        }
        
        for table, indexed_columns in common_indexed_columns.items():
            if table in schema_info["tables_info"]:
                for col in indexed_columns:
                    has_index = False
                    for idx in schema_info["tables_info"][table]["indexes"]:
                        if col in idx["indexdef"]:
                            has_index = True
                            break
                    
                    if not has_index:
                        issues.append({
                            "type": "missing_index",
                            "message": f"Column '{schema_name}.{table}.{col}' should have an index",
                            "suggested_fix": f"CREATE INDEX {table}_{col}_idx ON {schema_name}.{table} ({col})"
                        })
        
        # Return diagnostic results
        return {
            "schema_name": schema_name,
            "issues": issues,
            "issue_count": len(issues),
            "has_issues": len(issues) > 0
        }
        
    async def has_protected_column(self, schema_name: str, table_name: str) -> bool:
        """
        Check if a table has an is_protected column.
        
        Args:
            schema_name: The schema name
            table_name: The table name
            
        Returns:
            True if the table has an is_protected column, False otherwise
        """
        columns = await self.db.execute(
            """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = $1 
            AND table_name = $2
            AND column_name = 'is_protected'
            """,
            [schema_name, table_name],
            fetch_all=True
        )
        
        return len(columns) > 0
        
    async def add_protection_column(self, schema_name: str, table_name: str) -> bool:
        """
        Add an is_protected column to a table if it doesn't exist.
        
        Args:
            schema_name: The schema name
            table_name: The table name
            
        Returns:
            True if the column was added, False if it already existed
        """
        if await self.has_protected_column(schema_name, table_name):
            return False
            
        # Add the is_protected column
        await self.db.execute(
            f"ALTER TABLE {schema_name}.{table_name} ADD COLUMN is_protected BOOLEAN DEFAULT false",
        )
        
        return True
        
    async def setup_test_protection(self, schema_name: str) -> Dict[str, Any]:
        """
        Set up test data protection for all tables in a schema.
        
        This adds the is_protected column to all tables in the schema,
        which is used to prevent accidental modification of seed data.
        
        Args:
            schema_name: The schema to set up protection for
            
        Returns:
            Dict with results of the protection setup
        """
        # Get schema info
        schema_info = await self.inspect_schema(schema_name)
        
        if not schema_info["exists"]:
            return {"error": f"Schema '{schema_name}' does not exist"}
            
        # Add protection column to all tables
        results = {}
        for table in schema_info["tables"]:
            added = await self.add_protection_column(schema_name, table)
            results[table] = "added is_protected column" if added else "already protected"
            
        return {
            "schema_name": schema_name,
            "protection_setup": results
        }
    
    async def verify_model_schema(self, db_schema: str, model_name: str) -> Dict[str, Any]:
        """
        Verify that a database schema matches a model schema.
        
        Args:
            db_schema: The database schema to verify
            model_name: The model name to verify against
            
        Returns:
            Dict with verification results
        """
        try:
            # Import the model registry
            from services.models.core.model_registry import ModelRegistry
            
            # Get the model schema
            model_schema = await ModelRegistry.get_schema(model_name)
            
            if not model_schema:
                return {"error": f"Model '{model_name}' not found in registry"}
                
            # Get database schema info
            db_info = await self.inspect_schema(db_schema)
            
            if not db_info["exists"]:
                return {"error": f"Database schema '{db_schema}' does not exist"}
                
            # Determine which table to check
            table_name = model_schema.get("table_name", model_name.lower())
            
            if table_name not in db_info["tables"]:
                return {
                    "error": f"Table '{table_name}' not found in schema '{db_schema}'",
                    "available_tables": db_info["tables"]
                }
                
            # Get table columns
            columns = {}
            for col in db_info["tables_info"][table_name]["columns"]:
                columns[col["column_name"]] = col
                
            # Check if all required fields have corresponding columns
            missing_columns = []
            type_mismatches = []
            
            for field_name, field_def in model_schema.get("fields", {}).items():
                # Skip fields that don't map directly to columns
                if field_def.get("type") == "Dict" or field_def.get("type") == "List":
                    continue
                    
                # Map model types to PostgreSQL types
                type_mapping = {
                    "str": "character varying",
                    "int": "integer",
                    "float": "double precision",
                    "bool": "boolean",
                    "datetime": "timestamp without time zone",
                    "date": "date",
                    "UUID": "uuid"
                }
                
                expected_type = type_mapping.get(field_def.get("type"), "character varying")
                
                # Check if column exists
                if field_name not in columns:
                    missing_columns.append(field_name)
                    continue
                    
                # Check column type
                actual_type = columns[field_name]["data_type"]
                if actual_type != expected_type and field_def.get("required", True):
                    type_mismatches.append({
                        "field": field_name,
                        "expected_type": expected_type,
                        "actual_type": actual_type
                    })
            
            return {
                "model_name": model_name,
                "db_schema": db_schema,
                "table_name": table_name,
                "is_valid": not missing_columns and not type_mismatches,
                "missing_columns": missing_columns,
                "type_mismatches": type_mismatches
            }
        except ImportError:
            return {"error": "Could not import ModelRegistry, make sure the models service is installed"}


async def main():
    """Parse command line arguments and run the appropriate function."""
    parser = argparse.ArgumentParser(description="Database schema inspection utility.")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Inspect command
    inspect_parser = subparsers.add_parser("inspect", help="Inspect a schema")
    inspect_parser.add_argument("--schema", "-s", required=True, help="Schema to inspect")
    
    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare two schemas")
    compare_parser.add_argument("--source", required=True, help="Source schema")
    compare_parser.add_argument("--target", required=True, help="Target schema")
    
    # Diagnose command
    diagnose_parser = subparsers.add_parser("diagnose", help="Diagnose schema issues")
    diagnose_parser.add_argument("--schema", "-s", required=True, help="Schema to diagnose")
    
    # Setup protection command
    protect_parser = subparsers.add_parser("protect", help="Set up test data protection")
    protect_parser.add_argument("--schema", "-s", required=True, help="Schema to set up protection for")
    
    # Verify model schema command
    verify_parser = subparsers.add_parser("verify-model", help="Verify a model schema against a database schema")
    verify_parser.add_argument("--schema", "-s", required=True, help="Database schema to verify")
    verify_parser.add_argument("--model", "-m", required=True, help="Model name to verify against")
    
    args = parser.parse_args()
    inspector = SchemaInspector()
    
    try:
        if args.command == "inspect":
            result = await inspector.inspect_schema(args.schema)
            print(json.dumps(result, indent=2, default=str))
        elif args.command == "compare":
            result = await inspector.compare_schemas(args.source, args.target)
            print(json.dumps(result, indent=2, default=str))
        elif args.command == "diagnose":
            result = await inspector.diagnose_schema_issues(args.schema)
            print(json.dumps(result, indent=2, default=str))
        elif args.command == "protect":
            result = await inspector.setup_test_protection(args.schema)
            print(json.dumps(result, indent=2, default=str))
        elif args.command == "verify-model":
            result = await inspector.verify_model_schema(args.schema, args.model)
            print(json.dumps(result, indent=2, default=str))
        else:
            parser.print_help()
    finally:
        await inspector.close()

if __name__ == "__main__":
    asyncio.run(main()) 