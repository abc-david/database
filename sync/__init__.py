"""
MODULE: services/database/sync/__init__.py
PURPOSE: Export classes and functions from the sync package
CLASSES:
    - DatabaseSyncManager: For managing database synchronization
FUNCTIONS:
    - create_cli: Creates the argument parser for the CLI
    - main: Entry point for the CLI
DEPENDENCIES:
    - db_sync_manager: Provides database synchronization functionality
    - db_sync_cli: Provides command-line interface for sync operations

This module exports the main classes and functions from the sync package,
making them available for importing directly from the package. The package
provides functionality for database synchronization between different 
environments or devices.

The exported components help ensure consistent database state across different
development environments, making it easier for teams to work with shared data.

Example usage:
from services.database.sync import DatabaseSyncManager

# Create a sync manager
sync_manager = DatabaseSyncManager()

# Dump both databases
prod_path, test_path = sync_manager.dump_all()

# Commit dumps to git
sync_manager.commit_dumps_to_git("Update database dumps")
"""

from .db_sync_manager import DatabaseSyncManager
from .db_sync_cli import create_cli, main

__all__ = [
    "DatabaseSyncManager",
    "create_cli",
    "main"
] 