"""
MODULE: services/database/sync/db_sync_cli.py
PURPOSE: Command-line interface for database synchronization utilities
CLASSES:
    - None
FUNCTIONS:
    - create_cli: Creates the argument parser for the CLI
    - main: Entry point for the CLI
DEPENDENCIES:
    - argparse: For parsing command-line arguments
    - sys: For system operations
    - db_sync_manager: For database synchronization functionality

This module provides a command-line interface for the database synchronization
utilities. It allows users to create dumps, restore databases, list available
dumps, and synchronize databases between devices through simple commands.

The CLI is designed to be user-friendly and to support common database
synchronization workflows, making it easy for developers to manage database
state across different environments or devices.

Example usage:
$ python -m services.database.sync.db_sync_cli dump --all
$ python -m services.database.sync.db_sync_cli restore --latest
$ python -m services.database.sync.db_sync_cli sync --from user@otherdevice
"""

import argparse
import sys
from .db_sync_manager import DatabaseSyncManager

def create_cli():
    """
    Create command-line interface for database sync operations.
    
    Returns:
        ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(description="Database Synchronization Utilities")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Dump command
    dump_parser = subparsers.add_parser("dump", help="Create database dumps")
    dump_parser.add_argument("--prod", action="store_true", help="Dump production database")
    dump_parser.add_argument("--test", action="store_true", help="Dump test database")
    dump_parser.add_argument("--all", action="store_true", help="Dump both databases")
    dump_parser.add_argument("--no-timestamp", action="store_true", help="Exclude timestamp from filenames")
    dump_parser.add_argument("--schemas", nargs="+", help="Only dump specific schemas (space-separated list)")
    
    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore databases from dumps")
    restore_parser.add_argument("--prod", help="Production database dump to restore from")
    restore_parser.add_argument("--test", help="Test database dump to restore from")
    restore_parser.add_argument("--latest", action="store_true", help="Restore from latest dumps")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available dumps")
    
    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Sync databases between devices")
    sync_parser.add_argument("--from", dest="remote_host", help="Remote host to sync from (user@host)")
    
    # Git command
    git_parser = subparsers.add_parser("git", help="Manage dumps in git")
    git_parser.add_argument("--commit", action="store_true", help="Commit dumps to git")
    git_parser.add_argument("--message", help="Commit message")
    git_parser.add_argument("--push", action="store_true", help="Push dumps to git remote")
    git_parser.add_argument("--remote", default="origin", help="Git remote name (default: origin)")
    git_parser.add_argument("--branch", help="Git branch name (default: current branch)")
    
    # Workflow command
    workflow_parser = subparsers.add_parser("workflow", help="Execute common workflows")
    workflow_parser.add_argument("--dump-and-commit", action="store_true", help="Dump all databases and commit to git")
    workflow_parser.add_argument("--sync-from-remote", help="Pull from remote and restore (user@host)")
    workflow_parser.add_argument("--push-after-commit", action="store_true", help="Push to remote after commit")
    
    return parser

def main():
    """
    Entry point for the database sync CLI.
    
    Parses command-line arguments and executes the requested operation.
    """
    parser = create_cli()
    args = parser.parse_args()
    
    # Create sync manager
    db_sync = DatabaseSyncManager()
    
    # Execute command
    if args.command == "dump":
        # Determine whether to include timestamp
        include_timestamp = not args.no_timestamp
        
        # Prepare schemas parameter if provided
        schemas = None
        if args.schemas:
            schemas = {"prod": args.schemas, "test": args.schemas}
            
        # Dump databases based on flags
        if args.all or (not args.prod and not args.test):
            # Dump both databases
            prod_path, test_path = db_sync.dump_all(
                include_timestamp=include_timestamp,
                schemas=schemas
            )
            print(f"Production database dumped to: {prod_path}")
            print(f"Test database dumped to: {test_path}")
        else:
            # Dump individual databases
            if args.prod:
                prod_schemas = schemas["prod"] if schemas else None
                path = db_sync.dump_database(
                    is_test_db=False, 
                    include_timestamp=include_timestamp,
                    schemas=prod_schemas
                )
                print(f"Production database dumped to: {path}")
                
            if args.test:
                test_schemas = schemas["test"] if schemas else None
                path = db_sync.dump_database(
                    is_test_db=True, 
                    include_timestamp=include_timestamp,
                    schemas=test_schemas
                )
                print(f"Test database dumped to: {path}")
    
    elif args.command == "restore":
        # Restore databases based on flags
        if args.latest:
            # Restore from latest dumps
            db_sync.restore_from_latest()
            print("Both databases restored from latest dumps")
        else:
            # Restore individual databases
            if args.prod:
                db_sync.restore_database(args.prod, is_test_db=False)
                print(f"Production database restored from: {args.prod}")
                
            if args.test:
                db_sync.restore_database(args.test, is_test_db=True)
                print(f"Test database restored from: {args.test}")
    
    elif args.command == "list":
        # List available dumps
        dumps = db_sync.get_available_dumps()
        
        print("Available database dumps:")
        print("\nProduction database dumps:")
        for dump in dumps["prod"]:
            print(f"  - {dump}")
        
        print("\nTest database dumps:")
        for dump in dumps["test"]:
            print(f"  - {dump}")
    
    elif args.command == "sync":
        # Sync databases
        if args.remote_host:
            # Sync from remote host
            db_sync.sync_from_dumps(args.remote_host)
            print(f"Databases synced from {args.remote_host}")
        else:
            # Restore from latest local dumps
            db_sync.restore_from_latest()
            print("Databases restored from latest local dumps")
    
    elif args.command == "git":
        # Git operations
        if args.commit:
            # Commit dumps to git
            db_sync.commit_dumps_to_git(args.message)
            print("Database dumps committed to git")
            
            # Push if requested
            if args.push:
                db_sync.push_to_remote(args.remote, args.branch)
                print(f"Database dumps pushed to {args.remote}")
    
    elif args.command == "workflow":
        # Common workflows
        if args.dump_and_commit:
            # Dump databases
            prod_path, test_path = db_sync.dump_all()
            print(f"Production database dumped to: {prod_path}")
            print(f"Test database dumped to: {test_path}")
            
            # Commit to git
            db_sync.commit_dumps_to_git()
            print("Database dumps committed to git")
            
            # Push if requested
            if args.push_after_commit:
                db_sync.push_to_remote()
                print("Database dumps pushed to remote")
        
        if args.sync_from_remote:
            # Sync from remote host
            db_sync.sync_from_dumps(args.sync_from_remote)
            print(f"Databases synced from {args.sync_from_remote}")
    
    else:
        # No command or unrecognized command
        parser.print_help()

if __name__ == "__main__":
    main() 