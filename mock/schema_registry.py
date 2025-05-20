"""
MODULE: services/database/mock/schema_registry.py
PURPOSE: Maintains database schema information for validation and mock generation
CLASSES:
    - SchemaRegistry: Registry for database schema information
FUNCTIONS:
    - None
DEPENDENCIES:
    - psycopg2: For database connection and schema extraction
    - json: For JSON schema handling
    - re: For parsing SQL dump files
    - logging: For operational logging
    - os: For file operations
    - typing: For type annotations

This module provides a schema registry that extracts and stores database schema 
information for use in validation and mock data generation. It can extract schema
information directly from a database or from SQL dump files, making it versatile
for both online and offline schema analysis.

The schema information includes table structure, column types, constraints, and
relationships, which is crucial for generating realistic mock data that respects
the database structure during testing.

Example usage:
When testing database interactions without requiring a real database connection,
the SchemaRegistry provides schema information to generate mock responses that
match the expected structure, ensuring that code expecting specific database
schemas works correctly even in test environments.
"""

import os
import json
import re
import logging
import random
import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, Any, Optional, List, Tuple, Union, Set

class SchemaRegistry:
    """
    Maintains database schema information for validation and mock generation.
    
    This class is responsible for extracting, storing, and providing access to
    database schema information. It can obtain this information either by directly
    querying a database or by parsing SQL dump files. The stored schema information
    is used for validating data against schema constraints and for generating
    realistic mock data that respects the database structure.
    """
    
    def __init__(self, schema_source: str = "db", schema_file: Optional[str] = None):
        """
        Initialize the schema registry.
        
        Args:
            schema_source: Source of schema information ("db" or "file")
            schema_file: Path to SQL dump file if schema_source is "file"
        """
        # Configure logging
        self.logger = logging.getLogger("schema_registry")
        
        # Store initialization parameters
        self.schema_source = schema_source
        self.schema_file = schema_file
        
        # Storage for schema information
        # Structure: {schema_name: {table_name: {columns: {col_name: col_info}, primary_keys: []}}}
        self.table_schemas: Dict[str, Dict[str, Dict[str, Any]]] = {}
        
        # Track initialization state
        self.initialized = False
    
    def initialize(self) -> None:
        """
        Load schema information from the specified source.
        
        This method triggers the extraction of schema information based on the
        initialization parameters. It will either query the database directly
        or parse a SQL dump file.
        
        Raises:
            ValueError: If the schema source is not supported or if there are
                       issues with accessing the specified source.
        """
        # Skip if already initialized
        if self.initialized:
            self.logger.debug("Schema registry already initialized")
            return
            
        self.logger.info(f"Initializing schema registry from {self.schema_source}")
        
        # Extract schema information based on the source
        if self.schema_source == "db":
            self._load_schema_from_db()
        elif self.schema_source == "file":
            self._load_schema_from_file()
        else:
            error_msg = f"Unsupported schema source: {self.schema_source}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
            
        # Set initialization flag
        self.initialized = True
        
        self.logger.info(f"Schema registry initialized with {len(self.table_schemas)} schemas")
        for schema, tables in self.table_schemas.items():
            self.logger.debug(f"Schema '{schema}' has {len(tables)} tables")
    
    def _load_schema_from_db(self) -> None:
        """
        Query database to load schema information.
        
        This method connects to the database and extracts schema information
        by querying the information_schema tables. It extracts table structure,
        column definitions, primary keys, and other constraints.
        
        Raises:
            RuntimeError: If there are issues connecting to the database or
                         executing queries.
        """
        try:
            # Import settings for test database connection
            from config.settings import TEST_DB_USER, TEST_DB_PASS, TEST_DB_HOST, TEST_DB_PORT, TEST_DB_NAME
            
            # Create connection string and connect
            conn_string = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
            self.logger.debug(f"Connecting to database: {TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}")
            
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            try:
                # Get all schemas, excluding system schemas
                self.logger.debug("Retrieving database schemas")
                cursor.execute("""
                    SELECT schema_name 
                    FROM information_schema.schemata 
                    WHERE schema_name NOT IN ('pg_catalog', 'information_schema')
                """)
                
                schemas = [row['schema_name'] for row in cursor.fetchall()]
                self.logger.debug(f"Found {len(schemas)} schemas: {', '.join(schemas)}")
                
                # For each schema, get all tables
                for schema in schemas:
                    self.table_schemas[schema] = {}
                    
                    self.logger.debug(f"Retrieving tables for schema '{schema}'")
                    cursor.execute("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = %s
                    """, (schema,))
                    
                    tables = [row['table_name'] for row in cursor.fetchall()]
                    self.logger.debug(f"Found {len(tables)} tables in schema '{schema}'")
                    
                    # For each table, get column information
                    for table in tables:
                        self.logger.debug(f"Retrieving column information for {schema}.{table}")
                        cursor.execute("""
                            SELECT column_name, data_type, is_nullable, 
                                   column_default, character_maximum_length
                            FROM information_schema.columns
                            WHERE table_schema = %s AND table_name = %s
                            ORDER BY ordinal_position
                        """, (schema, table))
                        
                        columns = cursor.fetchall()
                        self.table_schemas[schema][table] = {
                            "columns": {
                                col['column_name']: {
                                    "type": col['data_type'],
                                    "nullable": col['is_nullable'] == 'YES',
                                    "default": col['column_default'],
                                    "max_length": col['character_maximum_length']
                                } for col in columns
                            }
                        }
                        
                        # Get primary key information
                        self.logger.debug(f"Retrieving primary key information for {schema}.{table}")
                        cursor.execute("""
                            SELECT kcu.column_name
                            FROM information_schema.table_constraints tc
                            JOIN information_schema.key_column_usage kcu
                              ON tc.constraint_name = kcu.constraint_name
                             AND tc.table_schema = kcu.table_schema
                            WHERE tc.constraint_type = 'PRIMARY KEY'
                              AND tc.table_schema = %s
                              AND tc.table_name = %s
                        """, (schema, table))
                        
                        pk_columns = [row['column_name'] for row in cursor.fetchall()]
                        self.table_schemas[schema][table]["primary_keys"] = pk_columns
                        
                        # Get foreign key information
                        self.logger.debug(f"Retrieving foreign key information for {schema}.{table}")
                        cursor.execute("""
                            SELECT
                                kcu.column_name,
                                ccu.table_schema AS foreign_table_schema,
                                ccu.table_name AS foreign_table_name,
                                ccu.column_name AS foreign_column_name
                            FROM information_schema.table_constraints AS tc
                            JOIN information_schema.key_column_usage AS kcu
                              ON tc.constraint_name = kcu.constraint_name
                              AND tc.table_schema = kcu.table_schema
                            JOIN information_schema.constraint_column_usage AS ccu
                              ON ccu.constraint_name = tc.constraint_name
                              AND ccu.table_schema = tc.table_schema
                            WHERE tc.constraint_type = 'FOREIGN KEY'
                              AND tc.table_schema = %s
                              AND tc.table_name = %s
                        """, (schema, table))
                        
                        fk_relations = cursor.fetchall()
                        self.table_schemas[schema][table]["foreign_keys"] = {
                            rel['column_name']: {
                                "schema": rel['foreign_table_schema'],
                                "table": rel['foreign_table_name'],
                                "column": rel['foreign_column_name']
                            } for rel in fk_relations
                        }
                        
                        # Get indexes information
                        self.logger.debug(f"Retrieving index information for {schema}.{table}")
                        cursor.execute("""
                            SELECT
                                i.relname AS index_name,
                                a.attname AS column_name,
                                ix.indisunique AS is_unique
                            FROM pg_index ix
                            JOIN pg_class i ON i.oid = ix.indexrelid
                            JOIN pg_class t ON t.oid = ix.indrelid
                            JOIN pg_namespace n ON n.oid = t.relnamespace
                            JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(ix.indkey)
                            WHERE n.nspname = %s
                              AND t.relname = %s
                        """, (schema, table))
                        
                        indexes = cursor.fetchall()
                        self.table_schemas[schema][table]["indexes"] = {}
                        
                        # Group columns by index name
                        for idx in indexes:
                            idx_name = idx['index_name']
                            if idx_name not in self.table_schemas[schema][table]["indexes"]:
                                self.table_schemas[schema][table]["indexes"][idx_name] = {
                                    "columns": [],
                                    "unique": idx['is_unique']
                                }
                            self.table_schemas[schema][table]["indexes"][idx_name]["columns"].append(idx['column_name'])
            finally:
                # Always close the database connection
                cursor.close()
                conn.close()
                
        except (psycopg2.Error, ImportError, Exception) as e:
            error_msg = f"Failed to load schema from database: {str(e)}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def _load_schema_from_file(self) -> None:
        """
        Parse SQL dump file to extract schema information.
        
        This method parses a SQL dump file to extract schema information such as
        table definitions, column types, and constraints. This is useful when
        working without a direct database connection.
        
        Raises:
            ValueError: If the schema file is not found or cannot be parsed.
        """
        # Validate file existence
        if not self.schema_file or not os.path.exists(self.schema_file):
            error_msg = f"Schema file not found: {self.schema_file}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
            
        self.logger.info(f"Loading schema from file: {self.schema_file}")
        
        try:
            # Read the SQL dump file
            with open(self.schema_file, 'r') as file:
                sql_content = file.read()
                
            # Parse CREATE TABLE statements
            # This is a simplified parser - a real implementation would be more robust
            self.logger.debug("Parsing CREATE TABLE statements")
            table_matches = re.finditer(r'CREATE TABLE (?:IF NOT EXISTS )?([a-zA-Z0-9_\.]+)\s*\(([\s\S]*?)\);', sql_content)
            
            # Process each CREATE TABLE statement
            for match in table_matches:
                full_table_name = match.group(1)
                columns_definition = match.group(2)
                
                # Extract schema and table name
                if '.' in full_table_name:
                    schema, table = full_table_name.split('.')
                else:
                    schema = 'public'
                    table = full_table_name
                    
                self.logger.debug(f"Processing table definition: {schema}.{table}")
                
                if schema not in self.table_schemas:
                    self.table_schemas[schema] = {}
                    
                # Parse column definitions
                columns = {}
                primary_keys = []
                foreign_keys = {}
                
                for line in columns_definition.split('\n'):
                    line = line.strip()
                    if not line or line.startswith('--'):
                        continue
                        
                    # Check for primary key constraint
                    pk_match = re.search(r'PRIMARY KEY\s*\(([^)]+)\)', line)
                    if pk_match:
                        pk_cols = [col.strip() for col in pk_match.group(1).split(',')]
                        primary_keys.extend(pk_cols)
                        continue
                        
                    # Check for foreign key constraint
                    fk_match = re.search(r'FOREIGN KEY\s*\(([^)]+)\)\s*REFERENCES\s*([a-zA-Z0-9_\.]+)\s*\(([^)]+)\)', line)
                    if fk_match:
                        fk_col = fk_match.group(1).strip()
                        ref_table = fk_match.group(2).strip()
                        ref_col = fk_match.group(3).strip()
                        
                        # Extract schema and table name
                        if '.' in ref_table:
                            ref_schema, ref_table_name = ref_table.split('.')
                        else:
                            ref_schema = 'public'
                            ref_table_name = ref_table
                            
                        foreign_keys[fk_col] = {
                            "schema": ref_schema,
                            "table": ref_table_name,
                            "column": ref_col
                        }
                        continue
                        
                    # Parse column definition
                    col_match = re.search(r'([a-zA-Z0-9_]+)\s+([A-Za-z0-9\(\)]+)(?:\s+([A-Z ]+))?', line)
                    if col_match:
                        col_name = col_match.group(1)
                        col_type = col_match.group(2)
                        constraints = col_match.group(3) or ""
                        
                        # Extract max length for character types
                        max_length = None
                        if "character" in col_type.lower() or "varchar" in col_type.lower():
                            length_match = re.search(r'\((\d+)\)', col_type)
                            if length_match:
                                max_length = int(length_match.group(1))
                        
                        columns[col_name] = {
                            "type": col_type.split('(')[0].lower(),  # Extract base type without length
                            "nullable": "NOT NULL" not in constraints,
                            "default": self._extract_default(constraints),
                            "max_length": max_length
                        }
                
                self.table_schemas[schema][table] = {
                    "columns": columns,
                    "primary_keys": primary_keys,
                    "foreign_keys": foreign_keys,
                    "indexes": {}  # Simplified - would need more parsing for indexes
                }
                
            self.logger.info(f"Successfully loaded schema information from file")
        
        except Exception as e:
            error_msg = f"Failed to parse schema file: {str(e)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
    
    def _extract_default(self, constraints: str) -> Optional[str]:
        """
        Extract DEFAULT value from column constraints.
        
        Args:
            constraints: Column constraints string

        Returns:
            Default value or None if not found
        """
        if not constraints:
            return None
            
        default_match = re.search(r'DEFAULT\s+([^,\s]+)', constraints)
        if default_match:
            return default_match.group(1)
            
        return None
    
    def get_table_schema(self, schema: str, table: str) -> Dict[str, Any]:
        """
        Get schema information for a specific table.
        
        This method returns the complete schema information for a specified table,
        including column definitions, primary keys, foreign keys, and indexes.
        
        Args:
            schema: Database schema name
            table: Table name
            
        Returns:
            Dictionary with table schema information
            
        Raises:
            ValueError: If the specified table is not found in the registry.
        """
        # Initialize if not already done
        if not self.initialized:
            self.initialize()
            
        # Validate schema and table existence
        if schema not in self.table_schemas:
            raise ValueError(f"Schema '{schema}' not found in schema registry")
            
        if table not in self.table_schemas[schema]:
            raise ValueError(f"Table '{table}' not found in schema '{schema}'")
            
        return self.table_schemas[schema][table]
    
    def validate_insert_data(self, schema: str, table: str, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate that insert data matches the table schema.
        
        This method checks if the provided data conforms to the table schema,
        ensuring that required columns are present, that column types match,
        and that constraints are respected.
        
        Args:
            schema: Database schema name
            table: Table name
            data: Data to insert
            
        Returns:
            Tuple with (is_valid, error_message)
        """
        try:
            # Get table schema
            table_schema = self.get_table_schema(schema, table)
            columns = table_schema["columns"]
            
            # Check for missing required columns
            for col_name, col_info in columns.items():
                # A column is required if it's not nullable, has no default value, and is not auto-generated
                is_auto_generated = col_info.get("default") and (
                    "nextval" in str(col_info["default"]) or 
                    "gen_random_uuid" in str(col_info["default"])
                )
                
                if not col_info["nullable"] and not col_info["default"] and not is_auto_generated and col_name not in data:
                    return False, f"Missing required column: {col_name}"
            
            # Check data types for provided columns
            for col_name, value in data.items():
                # Skip columns not in the schema (shouldn't happen with proper validation)
                if col_name not in columns:
                    return False, f"Unknown column: {col_name}"
                    
                col_info = columns[col_name]
                
                # Skip null check if column is nullable
                if value is None:
                    if not col_info["nullable"]:
                        return False, f"Column {col_name} cannot be null"
                    continue
                    
                # Check data type compatibility
                type_valid, error = self._validate_data_type(value, col_info["type"], col_info.get("max_length"))
                if not type_valid:
                    return False, f"Invalid value for column {col_name}: {error}"
            
            # All validation passed
            return True, None
            
        except ValueError as e:
            # Handle schema registry errors
            return False, str(e)
    
    def _validate_data_type(self, value: Any, data_type: str, max_length: Optional[int]) -> Tuple[bool, Optional[str]]:
        """
        Validate that a value matches the expected PostgreSQL data type.
        
        Args:
            value: The value to validate
            data_type: PostgreSQL data type
            max_length: Maximum length for string types
            
        Returns:
            Tuple with (is_valid, error_message)
        """
        # Handle different PostgreSQL data types
        try:
            # Integer types
            if data_type in ('integer', 'smallint', 'bigint', 'int'):
                if not isinstance(value, int):
                    return False, f"Expected integer, got {type(value).__name__}"
                
            # String/character types
            elif data_type.startswith('character') or data_type.startswith('varchar') or data_type == 'text':
                if not isinstance(value, str):
                    return False, f"Expected string, got {type(value).__name__}"
                if max_length and len(value) > max_length:
                    return False, f"String exceeds maximum length of {max_length}"
                    
            # Numeric types
            elif data_type in ('numeric', 'decimal', 'real', 'double precision', 'float'):
                if not isinstance(value, (int, float)):
                    return False, f"Expected number, got {type(value).__name__}"
                    
            # Boolean type
            elif data_type == 'boolean':
                if not isinstance(value, bool):
                    return False, f"Expected boolean, got {type(value).__name__}"
                    
            # Date/time types
            elif data_type in ('timestamp', 'date', 'time'):
                # For simplicity, we accept strings for timestamp types
                # In a real implementation, we would parse and validate the format
                if not isinstance(value, (str, datetime.datetime, datetime.date, datetime.time)):
                    return False, f"Expected timestamp/date/time, got {type(value).__name__}"
                    
            # JSON types
            elif data_type == 'jsonb' or data_type == 'json':
                # For JSON types, we just need to ensure it can be serialized
                json.dumps(value)
                
            # UUID type
            elif data_type == 'uuid':
                if not isinstance(value, str):
                    return False, f"Expected string for UUID, got {type(value).__name__}"
                # Simple UUID format check
                if not re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', value, re.I):
                    return False, f"Invalid UUID format: {value}"
                
            # Array types
            elif data_type.endswith('[]'):
                if not isinstance(value, (list, tuple)):
                    return False, f"Expected array, got {type(value).__name__}"
                # Check element types if array is not empty
                if value:
                    base_type = data_type[:-2]  # Remove '[]' suffix
                    for item in value:
                        item_valid, item_error = self._validate_data_type(item, base_type, None)
                        if not item_valid:
                            return False, f"Array element invalid: {item_error}"
            
            # Handle other types or unknown types
            else:
                # For unknown types, we accept any value but log a warning
                self.logger.warning(f"Unknown data type '{data_type}' - accepting value without validation")
                
            # If we get here, validation passed
            return True, None
            
        except Exception as e:
            # Handle any validation errors
            return False, str(e)
    
    def generate_mock_data(self, schema: str, table: str, override_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate realistic mock data based on table schema.
        
        This method creates realistic mock data for a specified table, respecting
        the table's schema, column types, and constraints. It can incorporate
        override values for specific columns.
        
        Args:
            schema: Database schema name
            table: Table name
            override_values: Dictionary of values to use instead of generating
            
        Returns:
            Dictionary with mock data for the table
        """
        # Get table schema
        table_schema = self.get_table_schema(schema, table)
        columns = table_schema["columns"]
        mock_data = {}
        
        # Initialize with override values if provided
        if override_values:
            mock_data.update(override_values)
        
        # Generate values for each column
        for col_name, col_info in columns.items():
            # Skip columns already set in override_values
            if col_name in mock_data:
                continue
                
            # Skip columns with defaults for auto-generation (serial, uuid, etc.)
            if col_info.get("default") and (
                "nextval" in str(col_info["default"]) or 
                "gen_random_uuid" in str(col_info["default"])
            ):
                continue
                
            # Generate mock value based on column name and type
            mock_data[col_name] = self._generate_mock_value(col_name, col_info, table_schema)
            
        return mock_data
    
    def _generate_mock_value(self, col_name: str, col_info: Dict[str, Any], table_schema: Dict[str, Any]) -> Any:
        """
        Generate appropriate mock value based on column name and type.
        
        Args:
            col_name: Column name
            col_info: Column information dictionary
            table_schema: Full table schema information
            
        Returns:
            Generated mock value appropriate for the column
        """
        data_type = col_info["type"]
        
        # Use column name hints for realistic values
        name_lower = col_name.lower()
        
        # Foreign key references
        if "foreign_keys" in table_schema and col_name in table_schema["foreign_keys"]:
            # For foreign keys, generate a value that looks like a reference
            fk_info = table_schema["foreign_keys"][col_name]
            return f"mock-{fk_info['table']}-ref-{random.randint(1000, 9999)}"
        
        # ID fields
        if name_lower == 'id' or name_lower.endswith('_id'):
            if data_type == 'uuid':
                import uuid
                return str(uuid.uuid4())
            else:
                return random.randint(1000, 9999)
        
        # Name fields
        elif 'name' in name_lower:
            prefixes = ["Test", "Mock", "Sample", "Demo", "Example"]
            return f"{random.choice(prefixes)} {col_name.title()}"
        
        # Date/time fields
        elif any(term in name_lower for term in ['date', 'time', 'created', 'updated']):
            now = datetime.datetime.now()
            if data_type == 'date':
                return now.date().isoformat()
            elif data_type == 'time':
                return now.time().isoformat()
            else:  # timestamp
                return now.isoformat()
        
        # Status fields
        elif 'status' in name_lower:
            return random.choice(["active", "inactive", "pending", "completed"])
        
        # Email fields
        elif 'email' in name_lower:
            domains = ["example.com", "test.org", "mock.net", "sample.io"]
            return f"mock.user.{random.randint(1000, 9999)}@{random.choice(domains)}"
        
        # URL fields
        elif any(term in name_lower for term in ['url', 'link', 'website']):
            domains = ["example.com", "test.org", "mock.net", "sample.io"]
            paths = ["home", "about", "contact", "product", "service"]
            return f"https://{random.choice(domains)}/{random.choice(paths)}"
        
        # Type-based generation for other fields
        if data_type in ('integer', 'smallint', 'bigint', 'int'):
            return random.randint(1, 1000)
            
        elif data_type.startswith('character') or data_type.startswith('varchar') or data_type == 'text':
            length = min(col_info.get("max_length") or 50, 50)  # Default to 50 if no max or too large
            return f"mock-{col_name}-{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length-len(col_name)-6))}"
            
        elif data_type in ('numeric', 'decimal', 'real', 'double precision', 'float'):
            return round(random.uniform(1, 1000), 2)
            
        elif data_type == 'boolean':
            return random.choice([True, False])
            
        elif data_type == 'jsonb' or data_type == 'json':
            # For JSON, create a mock object with some relevant fields
            return {
                "mock": True,
                "field": f"mock-{col_name}",
                "value": random.randint(1, 100),
                "active": random.choice([True, False])
            }
            
        elif data_type == 'uuid':
            import uuid
            return str(uuid.uuid4())
            
        elif data_type.endswith('[]'):
            # For array types, generate 1-3 mock elements
            base_type = data_type[:-2]  # Remove '[]' suffix
            count = random.randint(1, 3)
            return [
                self._generate_mock_scalar_value(base_type, None)
                for _ in range(count)
            ]
            
        # Default fallback for unknown types
        return f"mock-{col_name}"
    
    def _generate_mock_scalar_value(self, data_type: str, max_length: Optional[int]) -> Any:
        """
        Generate a mock value for a scalar data type.
        
        Args:
            data_type: Base data type
            max_length: Maximum length for string types
            
        Returns:
            Generated mock value for the type
        """
        if data_type in ('integer', 'smallint', 'bigint', 'int'):
            return random.randint(1, 1000)
            
        elif data_type.startswith('character') or data_type.startswith('varchar') or data_type == 'text':
            length = min(max_length or 10, 10)  # Use smaller default for array elements
            return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))
            
        elif data_type in ('numeric', 'decimal', 'real', 'double precision', 'float'):
            return round(random.uniform(1, 100), 2)
            
        elif data_type == 'boolean':
            return random.choice([True, False])
            
        elif data_type == 'uuid':
            import uuid
            return str(uuid.uuid4())
            
        else:
            # For other types, return a simple string
            return f"mock-{data_type}-value"

    def compare_with_db(self) -> Dict[str, Any]:
        """
        Compare this schema registry with the current database schema.
        
        This method is useful for detecting schema drift between the registry
        and the actual database.
        
        Returns:
            Dictionary with difference information
        """
        # Create a temporary registry from the current database
        db_registry = SchemaRegistry(schema_source="db")
        db_registry.initialize()
        
        # Compare the schemas
        return self._compare_schemas(db_registry)
    
    def _compare_schemas(self, other_registry: 'SchemaRegistry') -> Dict[str, Any]:
        """
        Compare this schema registry with another one.
        
        Args:
            other_registry: Another SchemaRegistry instance
            
        Returns:
            Dictionary with difference information
        """
        differences = {
            "missing_schemas": [],
            "missing_tables": {},
            "missing_columns": {},
            "type_differences": {},
            "constraint_differences": {}
        }
        
        # Check for missing schemas
        for schema in self.table_schemas:
            if schema not in other_registry.table_schemas:
                differences["missing_schemas"].append(schema)
                continue
                
            # Check for missing tables
            for table in self.table_schemas[schema]:
                if table not in other_registry.table_schemas[schema]:
                    if schema not in differences["missing_tables"]:
                        differences["missing_tables"][schema] = []
                    differences["missing_tables"][schema].append(table)
                    continue
                    
                # Check for column differences
                self_columns = self.table_schemas[schema][table]["columns"]
                other_columns = other_registry.table_schemas[schema][table]["columns"]
                
                for col_name in self_columns:
                    if col_name not in other_columns:
                        key = f"{schema}.{table}"
                        if key not in differences["missing_columns"]:
                            differences["missing_columns"][key] = []
                        differences["missing_columns"][key].append(col_name)
                        continue
                        
                    # Check for type differences
                    if self_columns[col_name]["type"] != other_columns[col_name]["type"]:
                        key = f"{schema}.{table}"
                        if key not in differences["type_differences"]:
                            differences["type_differences"][key] = {}
                        differences["type_differences"][key][col_name] = {
                            "self": self_columns[col_name]["type"],
                            "other": other_columns[col_name]["type"]
                        }
                        
                    # Check for constraint differences (nullable)
                    if self_columns[col_name]["nullable"] != other_columns[col_name]["nullable"]:
                        key = f"{schema}.{table}"
                        if key not in differences["constraint_differences"]:
                            differences["constraint_differences"][key] = {}
                        differences["constraint_differences"][key][col_name] = {
                            "constraint": "nullable",
                            "self": self_columns[col_name]["nullable"],
                            "other": other_columns[col_name]["nullable"]
                        }
        
        return differences
    
    def to_json(self, output_file: Optional[str] = None) -> Optional[str]:
        """
        Export schema registry to JSON format.
        
        Args:
            output_file: If provided, write to this file
            
        Returns:
            JSON string if output_file is None, otherwise None
        """
        if not self.initialized:
            self.initialize()
            
        # Convert to JSON-compatible format
        json_data = json.dumps(self.table_schemas, indent=2, default=str)
        
        # Write to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(json_data)
            return None
            
        return json_data
    
    @classmethod
    def from_json(cls, json_data: Union[str, Dict], is_file: bool = False) -> 'SchemaRegistry':
        """
        Create schema registry from JSON data.
        
        Args:
            json_data: JSON string, dictionary, or file path
            is_file: Whether json_data is a file path
            
        Returns:
            SchemaRegistry instance
        """
        registry = cls(schema_source="json")
        
        if is_file:
            with open(json_data, 'r') as f:
                registry.table_schemas = json.load(f)
        elif isinstance(json_data, str):
            registry.table_schemas = json.loads(json_data)
        else:
            registry.table_schemas = json_data
            
        registry.initialized = True
        return registry 