"""
MODULE: services/database/schema_setup.py
PURPOSE: Set up and verify database schemas
CLASSES:
    - SchemaSetup: Utility class for setting up and verifying database schemas
FUNCTIONS:
    - None
DEPENDENCIES:
    - db_connector: For database connectivity
    - sql_templates: For SQL templates
    - asyncio: For async operations

This module provides utilities for ensuring that all required database schemas
and tables are created. It can set up the public schema, create project schemas,
and verify that all required tables exist in each schema.
"""

import asyncio
import logging
from typing import List, Dict, Set, Optional
import re

from services.database.db_connector import DBConnector, QueryError, SchemaError
from services.database.sql_templates import (
    get_required_tables,
    format_project_template
)

logger = logging.getLogger(__name__)

class SchemaSetup:
    """
    Utility class for setting up and verifying database schemas.
    
    This class provides methods to:
    1. Set up the public schema with all required tables
    2. Create project schemas with the required tables
    3. Verify that all required tables exist in a schema
    4. Fix missing tables in a schema
    
    Usage:
        setup = SchemaSetup()
        await setup.ensure_public_schema()
        await setup.ensure_project_schema("b2b_saas")
    """
    
    def __init__(self):
        """Initialize the schema setup."""
        self._connector = DBConnector()
        
    async def _get_existing_tables(self, schema: str) -> Set[str]:
        """
        Get the set of existing tables in a schema.
        
        Args:
            schema: Schema name
            
        Returns:
            Set of table names
            
        Raises:
            SchemaError: If the schema does not exist
        """
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = $1
        """
        
        try:
            tables = await self._connector.execute(
                query, 
                (schema,), 
                fetch_all=True
            )
            return {table['table_name'] for table in tables}
        except Exception as e:
            logger.error(f"Error getting tables for schema {schema}: {e}")
            raise SchemaError(f"Error getting tables for schema {schema}: {e}")
            
    async def _schema_exists(self, schema: str) -> bool:
        """
        Check if a schema exists.
        
        Args:
            schema: Schema name
            
        Returns:
            True if the schema exists, False otherwise
        """
        query = """
        SELECT EXISTS (
            SELECT FROM information_schema.schemata 
            WHERE schema_name = $1
        )
        """
        
        try:
            return await self._connector.execute(
                query, 
                (schema,), 
                fetch_val=True
            )
        except Exception as e:
            logger.error(f"Error checking if schema {schema} exists: {e}")
            return False
            
    async def _create_schema(self, schema: str) -> None:
        """
        Create a schema if it doesn't exist.
        
        Args:
            schema: Schema name
            
        Raises:
            QueryError: If the schema creation fails
        """
        exists = await self._schema_exists(schema)
        
        if not exists:
            query = f"CREATE SCHEMA {schema}"
            try:
                await self._connector.execute(query)
                logger.info(f"Created schema: {schema}")
            except Exception as e:
                logger.error(f"Error creating schema {schema}: {e}")
                raise QueryError(f"Error creating schema {schema}: {e}")
        else:
            logger.info(f"Schema {schema} already exists")
            
    async def _create_table(self, schema: str, table: str, sql: str) -> None:
        """
        Create a table in a schema.
        
        Args:
            schema: Schema name
            table: Table name
            sql: SQL statement to create the table
            
        Raises:
            QueryError: If the table creation fails
        """
        try:
            # Log the SQL template for debugging
            logger.info(f"SQL template for {schema}.{table}: {sql}")
            
            # For project schemas, format the SQL template
            if schema != "public":
                sql = await format_project_template(sql, schema)
                
            await self._connector.execute(sql)
            logger.info(f"Created or verified table: {schema}.{table}")
        except Exception as e:
            logger.error(f"Error creating table {schema}.{table}: {e}")
            raise QueryError(f"Error creating table {schema}.{table}: {e}")
            
    async def ensure_public_schema(self) -> None:
        """
        Ensure the public schema exists and has all required tables.
        
        This method checks if the public schema has all the required tables for
        the application to function correctly, and creates any missing tables.
        """
        logger.info("Ensuring public schema")
        
        # Create the public schema if it doesn't exist
        if not await self._schema_exists("public"):
            await self._create_schema("public")
            
        # Get existing tables
        existing_tables = await self._get_existing_tables("public")
        
        # Get required tables for public schema
        required_tables = await get_required_tables("public")
        
        # Create missing tables
        for table_name, sql_template in required_tables.items():
            if table_name not in existing_tables:
                logger.info(f"Creating table: public.{table_name}")
                # Skip formatting for public schema tables since they already have public hardcoded
                await self._create_table("public", table_name, sql_template)
                
        logger.info("Public schema setup complete")
        
    async def ensure_project_schema(self, schema_name: str) -> None:
        """
        Ensure a project schema exists and has all required tables.
        
        This method creates a project schema if it doesn't exist, and ensures
        all required tables for project functionality are present.
        
        Args:
            schema_name: Name of the project schema
        """
        if not schema_name:
            raise ValueError("Schema name cannot be empty")
            
        # Ensure lowercase and no special characters in schema name
        schema_name = schema_name.lower()
        if not re.match(r'^[a-z0-9_]+$', schema_name):
            raise ValueError(f"Invalid schema name: {schema_name}. Use only lowercase letters, numbers, and underscores.")
        
        logger.info(f"Ensuring project schema: {schema_name}")
        
        # First ensure the public schema is setup properly
        await self.ensure_public_schema()
        
        # Create the project schema if it doesn't exist
        if not await self._schema_exists(schema_name):
            await self._create_schema(schema_name)
            
        # Get existing tables
        existing_tables = await self._get_existing_tables(schema_name)
        
        # Get required tables for project schema
        required_tables = await get_required_tables("project")
        
        # Create missing tables
        for table_name, sql_template in required_tables.items():
            if table_name not in existing_tables:
                logger.info(f"Creating table: {schema_name}.{table_name}")
                
                # Format the SQL with the schema name
                formatted_sql = await format_project_template(sql_template, schema_name)
                
                # Skip special handling of foreign keys - keep consistent data types
                # The format_project_template will handle the proper escaping of JSON object notation
                
                await self._create_table(schema_name, table_name, formatted_sql)
                
        logger.info(f"Project schema setup complete: {schema_name}")
        
    async def verify_schema(self, schema_name: str, schema_type: str = "project") -> Dict[str, bool]:
        """
        Verify that a schema has all required tables.
        
        Args:
            schema_name: Name of the schema to verify
            schema_type: Type of schema ('public' or 'project')
            
        Returns:
            Dictionary mapping table names to boolean (True if exists)
            
        Raises:
            ValueError: If the schema_type is invalid
        """
        # Get existing tables
        if not await self._schema_exists(schema_name):
            logger.warning(f"Schema {schema_name} does not exist")
            return {}
            
        existing_tables = await self._get_existing_tables(schema_name)
        
        # Get required tables
        required_tables = await get_required_tables(schema_type)
        
        # Check each required table
        verification = {}
        for table_name in required_tables.keys():
            verification[table_name] = table_name in existing_tables
            
        return verification
        
    async def fix_schema(self, schema_name: str, schema_type: str = "project") -> List[str]:
        """
        Fix a schema by creating any missing required tables.
        
        Args:
            schema_name: Name of the schema to fix
            schema_type: Type of schema ('public' or 'project')
            
        Returns:
            List of created tables
            
        Raises:
            ValueError: If the schema_type is invalid
        """
        # Verify schema first
        verification = await self.verify_schema(schema_name, schema_type)
        
        # If schema doesn't exist or verification is empty, we need to create it
        if not verification:
            if schema_type == "public":
                await self.ensure_public_schema()
                return list((await get_required_tables(schema_type)).keys())
            else:
                await self.ensure_project_schema(schema_name)
                return list((await get_required_tables(schema_type)).keys())
        
        # Get required tables
        required_tables = await get_required_tables(schema_type)
        
        # Create missing tables
        created_tables = []
        for table_name, exists in verification.items():
            if not exists:
                logger.info(f"Creating missing table: {schema_name}.{table_name}")
                sql_template = required_tables[table_name]
                
                if schema_type == "public":
                    # Skip formatting for public schema tables
                    formatted_sql = sql_template
                else:
                    # Format the SQL with the schema name
                    formatted_sql = await format_project_template(sql_template, schema_name)
                
                await self._create_table(schema_name, table_name, formatted_sql)
                created_tables.append(table_name)
                
        return created_tables
        
    async def get_all_project_schemas(self) -> List[str]:
        """
        Get all project schemas in the database.
        
        This method filters out system schemas and the public schema.
        
        Returns:
            List of project schema names
        """
        query = """
        SELECT schema_name 
        FROM information_schema.schemata 
        WHERE schema_name NOT IN ('public', 'pg_catalog', 'information_schema', 'pg_toast')
            AND schema_name NOT LIKE 'pg_%'
        """
        
        try:
            schemas = await self._connector.execute(
                query, 
                fetch_all=True
            )
            return [schema['schema_name'] for schema in schemas]
        except Exception as e:
            logger.error(f"Error getting project schemas: {e}")
            return []
            
    async def fix_all_project_schemas(self) -> Dict[str, List[str]]:
        """
        Fix all project schemas by creating any missing tables.
        
        Returns:
            Dictionary mapping schema names to lists of created tables
        """
        logger.info("Fixing all project schemas...")
        
        # Get all project schemas
        schemas = await self.get_all_project_schemas()
        logger.info(f"Found project schemas: {schemas}")
        
        # Fix each schema
        result = {}
        for schema in schemas:
            created = await self.fix_schema(schema)
            result[schema] = created
            
        return result
        
    async def close(self):
        """Close the database connection."""
        await self._connector.close()


async def main():
    """Set up all required schemas and tables."""
    setup = SchemaSetup()
    
    try:
        # Ensure public schema
        await setup.ensure_public_schema()
        
        # Fix all project schemas
        fixed = await setup.fix_all_project_schemas()
        for schema, tables in fixed.items():
            if tables:
                logger.info(f"Fixed schema {schema} by creating tables: {tables}")
                
        logger.info("Schema setup complete")
    finally:
        await setup.close()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Run the main function
    asyncio.run(main()) 