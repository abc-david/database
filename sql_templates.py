"""
MODULE: services/database/sql_templates.py
PURPOSE: SQL templates for creating database tables and schemas
CLASSES:
    - None
FUNCTIONS:
    - None
CONSTANTS:
    - SQL_TEMPLATES: Dictionary of SQL templates for creating database tables

This module contains SQL templates for creating the required database tables
for both the public schema and project schemas. These templates are used by
the database service to ensure all required tables are created.
"""

# Define table categories
PUBLIC_ONLY_TABLES = ["projects", "prompts", "templates", "template_vocabularies"]
PROJECT_ONLY_TABLES = ["content", "metadata", "site_content", "related_content", "content_blocks"]

# Public schema tables
PUBLIC_SCHEMA_TABLES = {
    # Projects table
    "projects": """
    CREATE TABLE IF NOT EXISTS public.projects (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        status TEXT DEFAULT 'active',
        metadata JSONB DEFAULT '{}'::jsonb
    );
    """,
    
    # Prompts table
    "prompts": """
    CREATE TABLE IF NOT EXISTS public.prompts (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name TEXT NOT NULL,
        content TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        version INTEGER DEFAULT 1,
        metadata JSONB DEFAULT '{}'::jsonb,
        project_id UUID REFERENCES public.projects(id) ON DELETE CASCADE,
        UNIQUE(name, project_id)
    );
    """,
    
    # Object models table
    "object_models": """
    CREATE TABLE IF NOT EXISTS public.object_models (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        definition JSONB NOT NULL,
        version INTEGER DEFAULT 1,
        metadata JSONB DEFAULT '{}'::jsonb
    );
    """,
    
    # LLM Usage table
    "llm_usage": """
    CREATE TABLE IF NOT EXISTS public.llm_usage (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        model TEXT NOT NULL,
        prompt_tokens INTEGER NOT NULL,
        completion_tokens INTEGER NOT NULL,
        total_tokens INTEGER NOT NULL,
        cost NUMERIC(10, 6) NOT NULL,
        project_id UUID REFERENCES public.projects(id) ON DELETE SET NULL,
        prompt_id UUID REFERENCES public.prompts(id) ON DELETE SET NULL,
        request_id TEXT,
        metadata JSONB DEFAULT '{}'::jsonb
    );
    """
}

# Project schema tables (created for each project schema)
PROJECT_SCHEMA_TABLES = {
    # Content table (main table for generated content)
    "content": """
    CREATE TABLE IF NOT EXISTS {schema}.content (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        title TEXT,
        content TEXT NOT NULL,
        content_type TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        status TEXT DEFAULT 'draft',
        metadata JSONB DEFAULT '{}'::jsonb,
        content_data JSONB DEFAULT '{}'::jsonb,
        source_id UUID,
        prompt_id UUID REFERENCES public.prompts(id) ON DELETE SET NULL
    );
    """,
    
    # Metadata table for additional content metadata
    "metadata": """
    CREATE TABLE IF NOT EXISTS {schema}.metadata (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        content_id UUID NOT NULL REFERENCES {schema}.content(id) ON DELETE CASCADE,
        metadata_type TEXT NOT NULL,
        metadata_value JSONB NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        UNIQUE(content_id, metadata_type)
    );
    """,
    
    # Vocabulary table for project-specific terminology
    "vocabulary": """
    CREATE TABLE IF NOT EXISTS {schema}.vocabulary (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        term TEXT NOT NULL,
        definition TEXT NOT NULL,
        category TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        metadata JSONB DEFAULT '{}'::jsonb,
        UNIQUE(term, category)
    );
    """,
    
    # Templates table for content generation templates
    "templates": """
    CREATE TABLE IF NOT EXISTS {schema}.templates (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name TEXT NOT NULL,
        description TEXT,
        content TEXT NOT NULL,
        type TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        metadata JSONB DEFAULT '{}'::jsonb
    );
    """,
    
    # Topics table for content topics
    "topics": """
    CREATE TABLE IF NOT EXISTS {schema}.topics (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name TEXT NOT NULL,
        description TEXT,
        keywords JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        metadata JSONB DEFAULT '{}'::jsonb
    );
    """
}

# Combined dictionary of all SQL templates
SQL_TEMPLATES = {
    "public": PUBLIC_SCHEMA_TABLES,
    "project": PROJECT_SCHEMA_TABLES
}

# Function to get all required tables for a schema type
async def get_required_tables(schema_type="public"):
    """
    Get the required tables for a given schema type.
    
    Args:
        schema_type: The schema type ('public' or 'project')
        
    Returns:
        Dict of table names to SQL templates
    """
    if schema_type == "public":
        return PUBLIC_SCHEMA_TABLES
    elif schema_type == "project":
        return PROJECT_SCHEMA_TABLES
    else:
        raise ValueError(f"Invalid schema type: {schema_type}")

# Function to format a project schema template with the actual schema name
async def format_project_template(template, schema_name):
    """
    Format a SQL template with the schema name.
    
    Args:
        template: The SQL template (string or dict of strings)
        schema_name: The schema name
        
    Returns:
        Formatted SQL template
    """
    if isinstance(template, dict):
        # Handle dictionary of templates
        formatted = {}
        for key, value in template.items():
            if isinstance(value, str):
                if "{schema}" in value:
                    # Escape existing curly braces by doubling them
                    # This is particularly important for JSON default values like '{}'::jsonb
                    value_escaped = value.replace("'{}'::", "'{{}}'::").replace("'{}'", "'{{}}'")
                    formatted[key] = value_escaped.format(schema=schema_name)
                else:
                    # No formatting needed if there's no schema placeholder
                    formatted[key] = value
            else:
                formatted[key] = value
        return formatted
    elif isinstance(template, str):
        # Handle string template
        if "{schema}" in template:
            # Escape existing curly braces by doubling them
            template_escaped = template.replace("'{}'::", "'{{}}'::").replace("'{}'", "'{{}}'")
            return template_escaped.format(schema=schema_name)
        else:
            return template
    else:
        # Return as is for other types
        return template
