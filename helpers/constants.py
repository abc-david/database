"""
Constants used across the database service.

This module defines constants that are used in database operations, 
such as table column names, to avoid hardcoding strings throughout
the codebase.
"""


class ModelTableColumns:
    """Column names for the models table."""
    ID = "id"
    NAME = "name"
    DEFINITION = "definition"
    DESCRIPTION = "description"
    OBJECT_TYPE = "object_type"
    VERSION = "version"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at" 