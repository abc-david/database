"""
MODULE: services/database/sync/db_sync_manager.py
PURPOSE: Manages database dumping, restoring, and synchronization between environments
CLASSES:
    - DatabaseSyncManager: Manages database dumping and synchronization
FUNCTIONS:
    - None
DEPENDENCIES:
    - logging: For operational logging
    - datetime: For timestamp generation
    - subprocess: For executing database commands
    - os: For file operations
    - typing: For type annotations
    - shutil: For file copying
    - pathlib: For path manipulation

This module provides functionality for synchronizing database content between
different environments or devices. It supports creating SQL dumps of database
schemas and tables, restoring from those dumps, and transferring dumps between
devices.

This functionality is particularly useful for development teams working across
multiple machines or for syncing between development, testing, and production
environments. The module ensures consistent database state across different
contexts.

Example usage:
When a developer needs to work on a new feature on a different machine, the
DatabaseSyncManager can create dumps of the relevant database schemas and tables
from the original machine, transfer them to the new machine, and restore them,
ensuring a consistent development environment regardless of the physical device.
"""

import os
import logging
import datetime
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Union

class DatabaseSyncManager:
    """
    Manages database dumping, restoring, and synchronization between environments.
    
    This class provides functionality for creating SQL dumps of database schemas and
    tables, restoring from those dumps, and transferring dumps between devices. It
    supports both production and test databases, making it easy to maintain consistent
    database state across different environments.
    """
    
    def __init__(self, repo_root: Optional[str] = None):
        """
        Initialize the database sync manager.
        
        Args:
            repo_root: Root directory of the repository (default: current working directory)
        """
        # Configure logging
        self.logger = logging.getLogger("db_sync_manager")
        
        # Determine repository root
        self.repo_root = repo_root or os.getcwd()
        
        # Set up dumps directory
        self.dumps_dir = os.path.join(self.repo_root, "db_dumps")
        os.makedirs(self.dumps_dir, exist_ok=True)
        
        # Ensure gitignore is set up correctly
        self._setup_gitignore()
    
    def _setup_gitignore(self) -> None:
        """
        Set up .gitignore to properly track database dumps.
        
        This ensures that database dumps are tracked in git, while
        temporary files are ignored.
        """
        gitignore_path = os.path.join(self.dumps_dir, ".gitignore")
        
        if not os.path.exists(gitignore_path):
            self.logger.debug("Creating .gitignore for db_dumps directory")
            with open(gitignore_path, 'w') as f:
                f.write("# Only ignore temporary files\n")
                f.write("*.tmp\n")
                f.write("temp_*\n")
                f.write("*.log\n")
    
    def _get_db_params(self, is_test_db: bool = False) -> Dict[str, str]:
        """
        Get database connection parameters.
        
        Args:
            is_test_db: Whether to get parameters for the test database
            
        Returns:
            Dictionary with database connection parameters
        """
        try:
            # First try to import from settings
            if is_test_db:
                from config.settings import TEST_DB_USER, TEST_DB_PASS, TEST_DB_HOST, TEST_DB_PORT, TEST_DB_NAME
                return {
                    "user": TEST_DB_USER,
                    "password": TEST_DB_PASS,
                    "host": TEST_DB_HOST,
                    "port": TEST_DB_PORT,
                    "dbname": TEST_DB_NAME
                }
            else:
                from config.settings import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
                return {
                    "user": DB_USER,
                    "password": DB_PASS,
                    "host": DB_HOST,
                    "port": DB_PORT,
                    "dbname": DB_NAME
                }
        except ImportError:
            # Fallback to environment variables
            import os
            from dotenv import load_dotenv
            
            # Load environment variables
            load_dotenv()
            
            # Get parameters with appropriate prefix
            prefix = "TEST_" if is_test_db else ""
            return {
                "user": os.getenv(f"{prefix}DB_USER", "postgres"),
                "password": os.getenv(f"{prefix}DB_PASS", ""),
                "host": os.getenv(f"{prefix}DB_HOST", "localhost"),
                "port": os.getenv(f"{prefix}DB_PORT", "5432"),
                "dbname": os.getenv(f"{prefix}DB_NAME", 
                                    "contentgen_test_db" if is_test_db else "contentgen_db")
            }
    
    def dump_database(self, is_test_db: bool = False, include_timestamp: bool = True, 
                     schemas: Optional[List[str]] = None) -> str:
        """
        Create a full SQL dump of the database.
        
        Args:
            is_test_db: Whether to dump the test database
            include_timestamp: Whether to include a timestamp in the filename
            schemas: List of schemas to dump (dumps all if None)
            
        Returns:
            Path to the created dump file
        """
        db_params = self._get_db_params(is_test_db)
        db_type = "test" if is_test_db else "prod"
        
        # Create filename with optional timestamp
        timestamp = f"_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}" if include_timestamp else ""
        filename = f"{db_type}_db{timestamp}.sql"
        dump_path = os.path.join(self.dumps_dir, filename)
        
        # Create the dump command
        cmd = [
            "pg_dump",
            "-h", db_params["host"],
            "-p", db_params["port"],
            "-U", db_params["user"],
            "-d", db_params["dbname"],
            "--clean",          # Include DROP commands before CREATE
            "--if-exists",      # Use IF EXISTS in DROP commands
            "--no-owner",       # Don't include ownership commands
            "--no-privileges",  # Don't include privilege commands
        ]
        
        # Add schema restrictions if specified
        if schemas:
            for schema in schemas:
                cmd.extend(["-n", schema])
        
        # Add output file
        cmd.extend(["-f", dump_path])
        
        # Set up environment with password
        env = os.environ.copy()
        env["PGPASSWORD"] = db_params["password"]
        
        try:
            self.logger.info(f"Creating database dump: {dump_path}")
            
            # Execute the dump command
            subprocess.run(cmd, env=env, check=True, capture_output=True)
            
            # Create a "latest" copy for easy reference
            latest_path = os.path.join(self.dumps_dir, f"{db_type}_db_latest.sql")
            shutil.copy2(dump_path, latest_path)
            
            self.logger.info(f"Database dump created successfully: {dump_path}")
            self.logger.info(f"Latest reference copy created: {latest_path}")
            
            return dump_path
            
        except subprocess.CalledProcessError as e:
            error_output = e.stderr.decode() if e.stderr else str(e)
            error_msg = f"Failed to create database dump: {error_output}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def restore_database(self, dump_path: str, is_test_db: bool = False) -> bool:
        """
        Restore a database from a SQL dump.
        
        Args:
            dump_path: Path to the SQL dump file
            is_test_db: Whether to restore to the test database
            
        Returns:
            True if successful, raises exception otherwise
        """
        # Check if the dump file exists or is a reference
        if not os.path.exists(dump_path):
            # Check if it's a reference to a dump in our directory
            potential_path = os.path.join(self.dumps_dir, dump_path)
            if os.path.exists(potential_path):
                dump_path = potential_path
            else:
                error_msg = f"Database dump not found: {dump_path}"
                self.logger.error(error_msg)
                raise FileNotFoundError(error_msg)
        
        # Get database connection parameters
        db_params = self._get_db_params(is_test_db)
        
        # Create the restore command
        cmd = [
            "psql",
            "-h", db_params["host"],
            "-p", db_params["port"],
            "-U", db_params["user"],
            "-d", db_params["dbname"],
            "-f", dump_path
        ]
        
        # Set up environment with password
        env = os.environ.copy()
        env["PGPASSWORD"] = db_params["password"]
        
        try:
            self.logger.info(f"Restoring database from dump: {dump_path}")
            
            # Execute the restore command
            result = subprocess.run(cmd, env=env, check=True, capture_output=True)
            
            self.logger.info("Database restored successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            error_output = e.stderr.decode() if e.stderr else str(e)
            error_msg = f"Failed to restore database: {error_output}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def dump_all(self, include_timestamp: bool = True, 
                schemas: Optional[Dict[str, List[str]]] = None) -> Tuple[str, str]:
        """
        Create dumps of both production and test databases.
        
        Args:
            include_timestamp: Whether to include a timestamp in the filenames
            schemas: Dictionary mapping 'prod' and 'test' to lists of schemas to dump
            
        Returns:
            Tuple of (prod_dump_path, test_dump_path)
        """
        self.logger.info("Creating dumps of production and test databases")
        
        # Extract schema lists or use None for full dumps
        prod_schemas = schemas.get('prod') if schemas else None
        test_schemas = schemas.get('test') if schemas else None
        
        # Create the dumps
        prod_path = self.dump_database(
            is_test_db=False, 
            include_timestamp=include_timestamp,
            schemas=prod_schemas
        )
        
        test_path = self.dump_database(
            is_test_db=True, 
            include_timestamp=include_timestamp,
            schemas=test_schemas
        )
        
        return prod_path, test_path
    
    def restore_all(self, prod_dump: str, test_dump: str) -> bool:
        """
        Restore both production and test databases from dumps.
        
        Args:
            prod_dump: Path to production database dump
            test_dump: Path to test database dump
            
        Returns:
            True if successful, raises exception otherwise
        """
        self.logger.info("Restoring production and test databases")
        
        # Restore production database
        self.restore_database(prod_dump, is_test_db=False)
        
        # Restore test database
        self.restore_database(test_dump, is_test_db=True)
        
        return True
    
    def restore_from_latest(self) -> bool:
        """
        Restore both databases from the latest dumps.
        
        Returns:
            True if successful, raises exception otherwise
        """
        # Check for latest dumps
        prod_latest = os.path.join(self.dumps_dir, "prod_db_latest.sql")
        test_latest = os.path.join(self.dumps_dir, "test_db_latest.sql")
        
        if not os.path.exists(prod_latest) or not os.path.exists(test_latest):
            error_msg = "Latest dumps not found. Create dumps first."
            self.logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        # Restore from latest dumps
        return self.restore_all(prod_latest, test_latest)
    
    def sync_from_dumps(self, target_device: Optional[str] = None) -> bool:
        """
        Sync databases from dumps, optionally pulling from a remote device first.
        
        Args:
            target_device: SSH target for remote sync (user@host)
            
        Returns:
            True if successful
        """
        if target_device:
            # Pull dumps from remote device first
            self.logger.info(f"Pulling database dumps from {target_device}")
            
            # Create path for remote dumps directory
            remote_dumps_dir = f"{target_device}:{Path(self.dumps_dir).as_posix()}"
            
            try:
                # Use rsync to pull latest dumps
                subprocess.run(
                    ["rsync", "-avz", f"{remote_dumps_dir}/*_latest.sql", self.dumps_dir],
                    check=True, capture_output=True
                )
                
                self.logger.info(f"Successfully pulled latest dumps from {target_device}")
                
            except subprocess.CalledProcessError as e:
                error_output = e.stderr.decode() if e.stderr else str(e)
                error_msg = f"Failed to pull dumps from remote: {error_output}"
                self.logger.error(error_msg)
                raise RuntimeError(error_msg)
        
        # Now restore from the latest dumps
        return self.restore_from_latest()
    
    def get_available_dumps(self) -> Dict[str, List[str]]:
        """
        Get list of available database dumps.
        
        Returns:
            Dictionary with 'prod' and 'test' keys containing lists of available dumps
        """
        result = {"prod": [], "test": []}
        
        # List all dump files
        for filename in os.listdir(self.dumps_dir):
            if filename.endswith(".sql"):
                if filename.startswith("prod_db"):
                    result["prod"].append(filename)
                elif filename.startswith("test_db"):
                    result["test"].append(filename)
        
        # Sort by timestamp (newest first)
        for db_type in result:
            result[db_type].sort(reverse=True)
        
        return result
    
    def commit_dumps_to_git(self, message: Optional[str] = None) -> bool:
        """
        Commit database dumps to git repository.
        
        Args:
            message: Commit message (default: "Update database dumps")
            
        Returns:
            True if successful
        """
        # Generate commit message if not provided
        if not message:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"Update database dumps - {timestamp}"
        
        try:
            self.logger.info("Committing database dumps to git repository")
            
            # Stage database dumps
            subprocess.run(
                ["git", "add", os.path.join(self.dumps_dir, "*.sql")],
                cwd=self.repo_root, check=True, capture_output=True
            )
            
            # Commit changes
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.repo_root, check=True, capture_output=True
            )
            
            self.logger.info("Database dumps committed to git repository")
            return True
            
        except subprocess.CalledProcessError as e:
            error_output = e.stderr.decode() if e.stderr else str(e)
            error_msg = f"Failed to commit dumps to git: {error_output}"
            self.logger.error(error_msg)
            return False
    
    def push_to_remote(self, remote: str = "origin", branch: Optional[str] = None) -> bool:
        """
        Push committed dumps to a git remote.
        
        Args:
            remote: Git remote name (default: "origin")
            branch: Branch to push (default: current branch)
            
        Returns:
            True if successful
        """
        try:
            self.logger.info(f"Pushing database dumps to remote: {remote}")
            
            # Determine current branch if none specified
            if branch is None:
                branch_cmd = subprocess.run(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    cwd=self.repo_root, check=True, capture_output=True, text=True
                )
                branch = branch_cmd.stdout.strip()
            
            # Push to remote
            subprocess.run(
                ["git", "push", remote, branch],
                cwd=self.repo_root, check=True, capture_output=True
            )
            
            self.logger.info(f"Successfully pushed dumps to {remote}/{branch}")
            return True
            
        except subprocess.CalledProcessError as e:
            error_output = e.stderr.decode() if e.stderr else str(e)
            error_msg = f"Failed to push dumps to remote: {error_output}"
            self.logger.error(error_msg)
            return False 