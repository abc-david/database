"""
MODULE: services/database/mock/mock_data_generator.py
PURPOSE: Generates realistic mock data based on database schema information
CLASSES:
    - MockDataGenerator: Generator for schema-aware mock data
FUNCTIONS:
    - None
DEPENDENCIES:
    - schema_registry: For accessing database schema information
    - random: For generating random values
    - datetime: For generating date/time values
    - uuid: For generating UUID values
    - typing: For type annotations
    - logging: For operational logging

This module provides functionality for generating realistic mock data that adheres
to database schema constraints. It works in conjunction with the SchemaRegistry
to ensure that generated data respects column types, constraints, and relationships
defined in the database schema.

The mock data is particularly useful for testing database interactions without
requiring real data or when creating fixtures for automated tests. The generated
data is schema-aware, meaning it will match the expected structure and constraints
of the database tables.

Example usage:
When testing a service that requires database records with specific structure,
the MockDataGenerator can provide realistic test data that adheres to the schema
without requiring manual creation of test fixtures or database setup. This makes
tests more robust against schema changes and reduces the maintenance burden.
"""

import random
import datetime
import uuid
import logging
from typing import Dict, Any, Optional, List, Union, Tuple

from .schema_registry import SchemaRegistry

class MockDataGenerator:
    """
    Generator for schema-aware mock data.
    
    This class generates realistic mock data that adheres to database schema
    constraints. It uses the SchemaRegistry to obtain schema information and
    ensures that the generated data matches the expected types, respects
    constraints, and maintains relationships.
    """
    
    def __init__(self, schema_registry: Optional[SchemaRegistry] = None):
        """
        Initialize the mock data generator.
        
        Args:
            schema_registry: Existing schema registry instance, or None to create new
        """
        # Configure logging
        self.logger = logging.getLogger("mock_data_generator")
        
        # Use provided schema registry or create a new one
        self.schema_registry = schema_registry or SchemaRegistry()
        
        # Ensure schema registry is initialized
        if not self.schema_registry.initialized:
            self.schema_registry.initialize()
    
    def generate_row(self, schema: str, table: str, override_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate a single row of mock data for a table.
        
        Args:
            schema: Database schema name
            table: Table name
            override_values: Dictionary of values to use instead of generating
            
        Returns:
            Dictionary with mock data for the table
        """
        try:
            self.logger.debug(f"Generating mock row for {schema}.{table}")
            
            # Generate mock data using the schema registry
            mock_data = self.schema_registry.generate_mock_data(schema, table, override_values)
            
            # Validate the generated data
            is_valid, error = self.schema_registry.validate_insert_data(schema, table, mock_data)
            if not is_valid:
                self.logger.warning(f"Generated mock data is invalid: {error}")
                
            return mock_data
            
        except Exception as e:
            self.logger.error(f"Error generating mock row: {str(e)}")
            # Return a minimal mock object in case of error
            return {"mock_error": str(e)}
    
    def generate_rows(self, schema: str, table: str, count: int = 5, 
                     base_values: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Generate multiple rows of mock data for a table.
        
        Args:
            schema: Database schema name
            table: Table name
            count: Number of rows to generate
            base_values: Base values to include in all rows
            
        Returns:
            List of dictionaries with mock data for the table
        """
        self.logger.debug(f"Generating {count} mock rows for {schema}.{table}")
        
        # Generate the specified number of rows
        rows = []
        for i in range(count):
            # Clone base values if provided
            override_values = base_values.copy() if base_values else None
            
            # Generate row and add to result
            row = self.generate_row(schema, table, override_values)
            rows.append(row)
            
        return rows
    
    def generate_related_rows(self, main_schema: str, main_table: str, 
                             related_tables: Dict[str, Dict[str, Any]], 
                             count: int = 1) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate mock data for a main table and its related tables.
        
        This method generates a realistic set of related data across multiple
        tables, maintaining referential integrity.
        
        Args:
            main_schema: Main table schema name
            main_table: Main table name
            related_tables: Dictionary mapping table names to options:
                            {
                                "table_name": {
                                    "schema": "schema_name",  # Optional, defaults to main_schema
                                    "count": 3,               # Optional, number of related rows
                                    "fk_column": "main_id"    # Optional, foreign key column name
                                }
                            }
            count: Number of main table rows to generate
            
        Returns:
            Dictionary mapping table names to lists of generated rows
        """
        self.logger.debug(f"Generating mock data for {main_schema}.{main_table} and related tables")
        
        result = {}
        
        # Generate main table rows
        main_rows = self.generate_rows(main_schema, main_table, count)
        result[main_table] = main_rows
        
        # For each main row, generate related rows
        for main_row in main_rows:
            # Get the main row ID (typically 'id' column)
            main_id = main_row.get("id")
            if main_id is None:
                # Try to find a primary key column
                try:
                    table_schema = self.schema_registry.get_table_schema(main_schema, main_table)
                    primary_keys = table_schema.get("primary_keys", [])
                    if primary_keys:
                        main_id = main_row.get(primary_keys[0])
                except Exception as e:
                    self.logger.warning(f"Could not determine main row ID: {str(e)}")
            
            if main_id is None:
                self.logger.warning("Main row ID not found, using a generated value")
                main_id = f"mock-id-{random.randint(1000, 9999)}"
            
            # Generate related rows for each related table
            for related_table, options in related_tables.items():
                # Get options with defaults
                related_schema = options.get("schema", main_schema)
                related_count = options.get("count", 1)
                fk_column = options.get("fk_column")
                
                # Determine the foreign key column if not specified
                if fk_column is None:
                    # Default to main_table_id or just id
                    fk_column = f"{main_table}_id"
                
                # Generate related rows with the foreign key reference
                related_rows = self.generate_rows(
                    related_schema, 
                    related_table, 
                    related_count,
                    {fk_column: main_id}
                )
                
                # Add to result
                if related_table not in result:
                    result[related_table] = []
                result[related_table].extend(related_rows)
        
        return result
    
    def generate_mock_query_result(self, query: str, params: Optional[Union[List, Tuple, Dict]] = None, 
                                  row_count: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Generate a mock result for a SQL query.
        
        This method parses the query to determine the schema and table,
        then generates appropriate mock data for the query result.
        
        Args:
            query: SQL query string
            params: Query parameters (not used for parsing, just for API compatibility)
            row_count: Number of rows to generate (random 1-5 if None)
            
        Returns:
            List of dictionaries with mock data
        """
        self.logger.debug(f"Generating mock query result for: {query}")
        
        # Extract schema and table from query
        try:
            schema, table = self._extract_table_from_query(query)
            
            # Generate a random row count if not specified
            if row_count is None:
                row_count = random.randint(1, 5)
                
            # Generate the mock rows
            return self.generate_rows(schema, table, row_count)
            
        except Exception as e:
            self.logger.warning(f"Could not extract table information from query: {str(e)}")
            
            # Return a minimal mock result with warning
            return [{
                "mock_warning": "Could not extract schema information from query",
                "query": query,
                "mock_data": True
            }]
    
    def _extract_table_from_query(self, query: str) -> Tuple[str, str]:
        """
        Extract schema and table name from a SQL query.
        
        Args:
            query: SQL query string
            
        Returns:
            Tuple of (schema, table)
            
        Raises:
            ValueError: If the schema and table cannot be extracted
        """
        import re
        
        # Normalize query (remove extra whitespace, make lowercase)
        query = " ".join(query.split()).lower()
        
        # Extract from SELECT queries
        select_match = re.search(r'from\s+([a-zA-Z0-9_\.]+)', query)
        if select_match:
            table_ref = select_match.group(1)
            return self._parse_table_reference(table_ref)
            
        # Extract from INSERT queries
        insert_match = re.search(r'insert\s+into\s+([a-zA-Z0-9_\.]+)', query)
        if insert_match:
            table_ref = insert_match.group(1)
            return self._parse_table_reference(table_ref)
            
        # Extract from UPDATE queries
        update_match = re.search(r'update\s+([a-zA-Z0-9_\.]+)', query)
        if update_match:
            table_ref = update_match.group(1)
            return self._parse_table_reference(table_ref)
            
        # Extract from DELETE queries
        delete_match = re.search(r'delete\s+from\s+([a-zA-Z0-9_\.]+)', query)
        if delete_match:
            table_ref = delete_match.group(1)
            return self._parse_table_reference(table_ref)
            
        # If we can't extract, raise an error
        raise ValueError(f"Could not extract table from query: {query}")
    
    def _parse_table_reference(self, table_ref: str) -> Tuple[str, str]:
        """
        Parse a table reference into schema and table name.
        
        Args:
            table_ref: Table reference (schema.table or just table)
            
        Returns:
            Tuple of (schema, table)
        """
        if '.' in table_ref:
            schema, table = table_ref.split('.')
        else:
            schema = 'public'
            table = table_ref
            
        return schema, table 