#!/usr/bin/env python3
"""
Script to check the tables in the test database.
"""

import os
import sys
import asyncio
import logging

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Set TEST_MODE environment variable to enable e2e mode
os.environ["TEST_MODE"] = "true"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def check_test_db():
    """Check tables in the test database."""
    try:
        # Import DBOperator here after setting TEST_MODE
        from services.database import DBOperator
        
        # Create a DBOperator with e2e mode
        logger.info("Creating DBOperator with e2e mode...")
        db = DBOperator(test_mode="e2e")
        
        # Get current database info
        db_info = await db.execute("SELECT current_database(), current_user", fetch_row=True)
        logger.info(f"Connected to database: {db_info['current_database']} as user: {db_info['current_user']}")
        
        # Verify the tables
        logger.info("Checking tables in public schema...")
        tables = await db.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """, fetch_all=True)
        
        logger.info("Tables in public schema:")
        for table in tables:
            logger.info(f"  - {table['table_name']}")
        
        # Check data in each table
        if 'object_models' in [t['table_name'] for t in tables]:
            logger.info("\nChecking data in object_models table:")
            object_models = await db.execute("SELECT id, name, object_type, version FROM public.object_models", fetch_all=True)
            for model in object_models:
                logger.info(f"  - {model['name']} ({model['object_type']}, v{model['version']})")
        else:
            logger.warning("object_models table not found")
        
        if 'projects' in [t['table_name'] for t in tables]:
            logger.info("\nChecking data in projects table:")
            projects = await db.execute("SELECT id, name, schema_name, primary_language, status FROM public.projects", fetch_all=True)
            for project in projects:
                logger.info(f"  - {project['name']} (schema: {project['schema_name']}, status: {project['status']})")
        else:
            logger.warning("projects table not found")
        
        if 'prompts' in [t['table_name'] for t in tables]:
            logger.info("\nChecking data in prompts table:")
            prompts = await db.execute("SELECT id, name, engine_type, template_type, version, is_active FROM public.prompts", fetch_all=True)
            for prompt in prompts:
                logger.info(f"  - {prompt['name']} (engine: {prompt['engine_type']}, type: {prompt['template_type']}, active: {prompt['is_active']})")
        else:
            logger.warning("prompts table not found")
        
    except Exception as e:
        logger.error(f"Error checking test database: {e}")
        raise
    finally:
        # Clean up
        if 'db' in locals():
            await db.close()
            logger.info("Database connection closed")

if __name__ == "__main__":
    asyncio.run(check_test_db()) 