"""
MODULE: services/database/mock/__init__.py
PURPOSE: Export classes from the mock package
CLASSES:
    - SchemaRegistry: Exported from schema_registry
    - MockDataGenerator: Exported from mock_data_generator
FUNCTIONS:
    - None
DEPENDENCIES:
    - schema_registry: Provides schema information
    - mock_data_generator: Generates mock data based on schema information

This module exports the main classes from the mock package, making them
available for importing directly from the package. The package provides
functionality for schema-aware mock data generation and validation.

The exported classes collaborate to provide a comprehensive solution for
testing with realistic mock data that adheres to the database schema.

Example usage:
from services.database.mock import SchemaRegistry, MockDataGenerator

# Initialize schema registry
registry = SchemaRegistry()

# Create mock data generator
generator = MockDataGenerator(registry)

# Generate mock data for a table
mock_data = generator.generate_row("public", "users")
"""

from .schema_registry import SchemaRegistry
from .mock_data_generator import MockDataGenerator

__all__ = [
    "SchemaRegistry",
    "MockDataGenerator"
] 