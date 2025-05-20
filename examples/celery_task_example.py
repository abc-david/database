"""
MODULE: services/database/examples/celery_task_example.py
PURPOSE: Example of using database decorators with Celery tasks
CLASSES:
    - None
FUNCTIONS:
    - process_user_data: Example Celery task using the with_db_connection decorator
    - update_multiple_records: Example showing transaction handling
DEPENDENCIES:
    - services.database: For database operations
    - celery: For task definitions

This module demonstrates how to use the with_db_connection decorator in Celery tasks,
showing proper database connection handling in an async environment.
"""

import logging
import uuid
from typing import Dict, Any, List

from celery import shared_task
from celery.utils.log import get_task_logger

from services.database import with_db_connection

logger = get_task_logger(__name__)

@shared_task
@with_db_connection
async def process_user_data(conn, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Example Celery task that processes user data.
    
    This task demonstrates:
    1. Automatic connection injection via the decorator
    2. Transaction handling (automatic commit/rollback)
    3. Connection cleanup
    
    Args:
        conn: Database connection (injected by decorator)
        user_id: UUID of the user
        data: User data to process
        
    Returns:
        Processed user data with status
    """
    # Check if user exists
    user = await conn.fetch_dict(
        "SELECT * FROM public.users WHERE id = $1",
        user_id
    )
    
    if not user:
        logger.error(f"User {user_id} not found")
        return {"status": "error", "message": "User not found"}
    
    # Update user data
    updated_user = await conn.execute(
        """
        UPDATE public.users 
        SET 
            name = $1,
            email = $2,
            updated_at = NOW()
        WHERE id = $3
        RETURNING *
        """,
        data.get("name"),
        data.get("email"),
        user_id
    )
    
    # Create user preferences
    if "preferences" in data:
        for pref_key, pref_value in data["preferences"].items():
            await conn.execute(
                """
                INSERT INTO public.user_preferences (user_id, key, value)
                VALUES ($1, $2, $3)
                ON CONFLICT (user_id, key) DO UPDATE SET value = $3
                """,
                user_id,
                pref_key,
                pref_value
            )
    
    # Log the update
    await conn.execute(
        """
        INSERT INTO public.audit_logs (entity_type, entity_id, action, data)
        VALUES ($1, $2, $3, $4)
        """,
        "user",
        user_id,
        "update",
        {"updated_fields": list(data.keys())}
    )
    
    return {
        "status": "success",
        "user_id": user_id,
        "updated_fields": list(data.keys())
    }

@shared_task
@with_db_connection
async def update_multiple_records(conn, record_ids: List[str], update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Example Celery task that updates multiple records in a transaction.
    
    This task demonstrates:
    1. Transaction handling with multiple operations
    2. Error handling and automatic rollback
    
    Args:
        conn: Database connection (injected by decorator)
        record_ids: List of record IDs to update
        update_data: Data to apply to each record
        
    Returns:
        Status of the update operation
    """
    updated_count = 0
    failed_ids = []
    
    # Transaction is handled by the decorator
    # If any operation fails, all updates will be rolled back
    
    for record_id in record_ids:
        try:
            # Update the record
            result = await conn.execute(
                """
                UPDATE public.records
                SET 
                    status = $1,
                    metadata = metadata || $2::jsonb,
                    updated_at = NOW()
                WHERE id = $3
                RETURNING id
                """,
                update_data.get("status"),
                update_data.get("metadata", {}),
                record_id
            )
            
            if result:
                updated_count += 1
            else:
                failed_ids.append(record_id)
                
        except Exception as e:
            # This exception will be caught by the decorator
            # The transaction will be rolled back automatically
            logger.error(f"Error updating record {record_id}: {str(e)}")
            # Re-raise to trigger rollback
            raise
    
    # If we get here, all updates succeeded and the transaction will be committed
    
    return {
        "status": "success",
        "updated_count": updated_count,
        "total_records": len(record_ids),
        "failed_ids": failed_ids
    } 