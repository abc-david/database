"""
MODULE: services/database/utils/migrate_prompts_id_to_uuid.py
PURPOSE: Migrate the prompts table ID column from integer to UUID
DEPENDENCIES:
    - asyncio: For async/await support
    - asyncpg: For database access
    - uuid: For UUID generation

This script performs a one-time migration to convert the prompts table's
primary key from integer to UUID for consistency with other tables.
"""

import asyncio
import uuid
from services.database.db_connector import DBConnector


async def migrate_prompts_table():
    """
    Migrate the prompts table primary key from integer to UUID.
    
    This function:
    1. Creates a new temporary table with UUID primary key
    2. Copies data from old table to new, generating UUIDs
    3. Drops the old table and renames the new one
    """
    print("Starting migration of prompts table from integer ID to UUID...")
    db = DBConnector()
    
    try:
        # First check if the table has integer IDs
        column_type = await db.execute(
            """
            SELECT data_type FROM information_schema.columns 
            WHERE table_name = 'prompts' AND column_name = 'id' AND table_schema = 'public'
            """,
            fetch_val=True
        )
        
        if column_type != 'integer':
            print(f"Prompts table already has ID type: {column_type}. Migration not needed.")
            return
        
        print(f"Current prompts table ID type: {column_type}. Starting migration...")
        
        # Check for and clean up any leftover tables from previous migration attempts
        await cleanup_previous_migration(db)
        
        # Begin transaction manually
        await db.execute("BEGIN")
        
        try:
            # 1. Create new table with UUID primary key
            await db.execute("""
                CREATE TABLE public.prompts_new (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    engine_type VARCHAR(50),
                    template_type VARCHAR(50),
                    template JSONB DEFAULT '{}'::jsonb,
                    version VARCHAR(20),
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    use_cases TEXT[]
                )
            """)
            
            print("Created new prompts table with UUID primary key")
            
            # 2. Get existing data
            old_prompts = await db.execute(
                "SELECT * FROM public.prompts",
                fetch_all=True
            )
            
            print(f"Found {len(old_prompts)} existing prompts to migrate")
            
            # Create a mapping of old IDs to new UUIDs for reference tables
            id_mapping = {}
            
            # 3. Copy data to new table
            for prompt in old_prompts:
                new_id = uuid.uuid4()
                id_mapping[prompt['id']] = new_id
                
                # Insert into new table
                await db.execute(
                    """
                    INSERT INTO public.prompts_new
                    (id, name, description, engine_type, template_type, template, 
                     version, is_active, created_at, updated_at, use_cases)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                    """, 
                    (new_id, 
                     prompt['name'], 
                     prompt['description'],
                     prompt.get('engine_type'),
                     prompt.get('template_type'),
                     prompt.get('template', '{}'),
                     prompt.get('version'),
                     prompt.get('is_active', True),
                     prompt.get('created_at'),
                     prompt.get('updated_at'),
                     prompt.get('use_cases', []))
                )
            
            print("Data copied to new table")
            
            # 4. Update any foreign key references in other tables
            # Check if llm_usage table exists and has prompt_id references
            llm_usage_exists = await db.execute(
                """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name = 'llm_usage'
                )
                """,
                fetch_val=True
            )
            
            if llm_usage_exists:
                print("Updating references in llm_usage table...")
                # Create a new llm_usage table with updated references
                await db.execute("""
                    CREATE TABLE public.llm_usage_new (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        model TEXT NOT NULL,
                        prompt_tokens INTEGER NOT NULL,
                        completion_tokens INTEGER NOT NULL,
                        total_tokens INTEGER NOT NULL,
                        cost NUMERIC(10, 6) NOT NULL,
                        project_id UUID REFERENCES public.projects(id) ON DELETE SET NULL,
                        prompt_id UUID REFERENCES public.prompts_new(id) ON DELETE SET NULL,
                        request_id TEXT,
                        metadata JSONB DEFAULT '{}'::jsonb
                    )
                """)
                
                # Copy data, updating references
                llm_usage_records = await db.execute(
                    "SELECT * FROM public.llm_usage",
                    fetch_all=True
                )
                
                for record in llm_usage_records:
                    old_prompt_id = record.get('prompt_id')
                    new_prompt_id = id_mapping.get(old_prompt_id) if old_prompt_id else None
                    
                    await db.execute(
                        """
                        INSERT INTO public.llm_usage_new
                        (id, timestamp, model, prompt_tokens, completion_tokens, total_tokens, cost, 
                         project_id, prompt_id, request_id, metadata)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                        """,
                        (record['id'],
                        record['timestamp'],
                        record['model'],
                        record['prompt_tokens'],
                        record['completion_tokens'],
                        record['total_tokens'],
                        record['cost'],
                        record.get('project_id'),
                        new_prompt_id,
                        record.get('request_id'),
                        record.get('metadata', '{}'))
                    )
            
            # Check for project schemas that might reference prompts
            project_schemas = await db.execute(
                """
                SELECT schema_name FROM information_schema.schemata
                WHERE schema_name NOT IN ('public', 'information_schema', 'pg_catalog', 'pg_temp_1', 'pg_toast', 'pg_toast_temp_1')
                """,
                fetch_all=True
            )
            
            for schema in project_schemas:
                schema_name = schema['schema_name']
                # Check if content table exists in this schema and has prompt_id reference
                content_exists = await db.execute(
                    f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = '{schema_name}' AND table_name = 'content'
                    )
                    """,
                    fetch_val=True
                )
                
                if content_exists:
                    print(f"Updating prompt references in {schema_name}.content table...")
                    # Check if the content table actually has a prompt_id column
                    has_prompt_id = await db.execute(
                        f"""
                        SELECT EXISTS (
                            SELECT FROM information_schema.columns
                            WHERE table_schema = '{schema_name}' AND table_name = 'content'
                            AND column_name = 'prompt_id'
                        )
                        """,
                        fetch_val=True
                    )
                    
                    if not has_prompt_id:
                        print(f"Table {schema_name}.content does not have a prompt_id column, skipping...")
                        continue
                        
                    # Create new content table with updated references
                    content_columns = await db.execute(
                        f"""
                        SELECT column_name, data_type, character_maximum_length, is_nullable
                        FROM information_schema.columns
                        WHERE table_schema = '{schema_name}' AND table_name = 'content'
                        ORDER BY ordinal_position
                        """,
                        fetch_all=True
                    )
                    
                    # Generate column definitions for the new table
                    column_defs = []
                    for col in content_columns:
                        col_name = col['column_name']
                        col_type = col['data_type']
                        if col['character_maximum_length']:
                            col_type = f"{col_type}({col['character_maximum_length']})"
                        nullable = "NULL" if col['is_nullable'] == "YES" else "NOT NULL"
                        
                        if col_name == 'id':
                            column_defs.append(f"id UUID PRIMARY KEY DEFAULT gen_random_uuid()")
                        elif col_name == 'prompt_id':
                            column_defs.append(f"prompt_id UUID REFERENCES public.prompts_new(id) ON DELETE SET NULL")
                        else:
                            column_defs.append(f"{col_name} {col_type} {nullable}")
                    
                    # Create the new table
                    create_table_sql = f"""
                        CREATE TABLE {schema_name}.content_new (
                            {', '.join(column_defs)}
                        )
                    """
                    await db.execute(create_table_sql)
                    
                    # Copy data, updating references
                    content_records = await db.execute(
                        f"SELECT * FROM {schema_name}.content",
                        fetch_all=True
                    )
                    
                    for record in content_records:
                        # Prepare column names and values for insert
                        cols = []
                        placeholders = []
                        values = []
                        param_index = 1
                        
                        for key, val in record.items():
                            if key == 'prompt_id' and val is not None:
                                # Map old prompt ID to new UUID
                                new_val = id_mapping.get(val)
                                if new_val:
                                    cols.append(key)
                                    placeholders.append(f"${param_index}")
                                    values.append(new_val)
                                    param_index += 1
                            else:
                                cols.append(key)
                                placeholders.append(f"${param_index}")
                                values.append(val)
                                param_index += 1
                        
                        # Insert into new table
                        insert_sql = f"""
                            INSERT INTO {schema_name}.content_new
                            ({', '.join(cols)})
                            VALUES ({', '.join(placeholders)})
                        """
                        await db.execute(insert_sql, tuple(values))
            
            # 5. Drop old tables and rename new ones
            print("Dropping old tables and renaming new ones...")
            
            # Drop and rename content tables in project schemas
            for schema in project_schemas:
                schema_name = schema['schema_name']
                content_exists = await db.execute(
                    f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = '{schema_name}' AND table_name = 'content_new'
                    )
                    """,
                    fetch_val=True
                )
                
                if content_exists:
                    await db.execute(f"DROP TABLE {schema_name}.content CASCADE")
                    await db.execute(f"ALTER TABLE {schema_name}.content_new RENAME TO content")
            
            # Drop and rename llm_usage if it exists
            if llm_usage_exists:
                await db.execute("DROP TABLE public.llm_usage CASCADE")
                await db.execute("ALTER TABLE public.llm_usage_new RENAME TO llm_usage")
            
            # Finally drop and rename the prompts table
            await db.execute("DROP TABLE public.prompts CASCADE")
            await db.execute("ALTER TABLE public.prompts_new RENAME TO prompts")
            
            # Commit the transaction
            await db.execute("COMMIT")
            
            print("Migration completed successfully!")
        
        except Exception as e:
            # Rollback transaction on error
            await db.execute("ROLLBACK")
            print(f"Transaction failed, changes rolled back: {str(e)}")
            raise
    
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        raise
    finally:
        await db.close()


async def cleanup_previous_migration(db):
    """
    Clean up any temporary tables from a previous migration attempt.
    """
    print("Checking for and cleaning up tables from previous migration attempts...")
    
    # Check if prompts_new exists
    prompts_new_exists = await db.execute(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'prompts_new'
        )
        """,
        fetch_val=True
    )
    
    if prompts_new_exists:
        print("Found prompts_new table from previous migration attempt, dropping...")
        await db.execute("DROP TABLE public.prompts_new CASCADE")
    
    # Check if llm_usage_new exists
    llm_usage_new_exists = await db.execute(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'llm_usage_new'
        )
        """,
        fetch_val=True
    )
    
    if llm_usage_new_exists:
        print("Found llm_usage_new table from previous migration attempt, dropping...")
        await db.execute("DROP TABLE public.llm_usage_new CASCADE")
    
    # Check for content_new tables in all schemas
    project_schemas = await db.execute(
        """
        SELECT schema_name FROM information_schema.schemata
        WHERE schema_name NOT IN ('public', 'information_schema', 'pg_catalog', 'pg_temp_1', 'pg_toast', 'pg_toast_temp_1')
        """,
        fetch_all=True
    )
    
    for schema in project_schemas:
        schema_name = schema['schema_name']
        
        content_new_exists = await db.execute(
            f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = '{schema_name}' AND table_name = 'content_new'
            )
            """,
            fetch_val=True
        )
        
        if content_new_exists:
            print(f"Found {schema_name}.content_new table from previous migration attempt, dropping...")
            await db.execute(f"DROP TABLE {schema_name}.content_new CASCADE")
    
    print("Cleanup of temporary tables completed")


if __name__ == "__main__":
    asyncio.run(migrate_prompts_table()) 