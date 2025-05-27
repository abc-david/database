# Database Schema Architecture

## Overview

The content generator system uses a multi-schema PostgreSQL database architecture to organize data across projects while maintaining clear boundaries and data ownership. This document explains the schema design philosophy, structure, and data flow.

The core design principle is the separation of common resources (shared across all projects) from project-specific data. This is achieved through a two-level schema organization:

1. **Public Schema**: Contains common resources and system-wide tables
2. **Project-Specific Schemas**: Contains data relevant only to a single project

## Schema Organization

### Public Schema

The public schema serves as the authoritative source of truth for shared resources across all projects. It contains:

- **Projects**: Basic information about each project
- **Object Models**: Reusable content generation models
- **Prompts**: Reusable prompt templates
- **LLM Usage**: Tracking of LLM API calls
- **Clients**: Client information for billing and organization

### Project Schemas

Each project has its own dedicated schema, named after the project (e.g., `project_123`, where 123 is the project ID). These schemas contain:

- **Contents**: Generated content specific to this project
- **Metadata**: Project-specific metadata and settings
- **Vocabulary**: Project-specific terminology and dictionaries
- **Prompt Components**: Project-adapted prompt templates

## Advantages of This Approach

- **Clear Data Ownership**: Each project's data is isolated in its own schema
- **Simplified Access Control**: Permissions can be assigned at the schema level
- **Independent Evolution**: Projects can evolve their schema without affecting others
- **Deployment Flexibility**: Ability to migrate specific projects if needed
- **Query Efficiency**: Queries can target specific schemas to reduce data scanning

## Public Schema as Source of Truth

The public schema is designed to store:

1. **Authoritative Definitions**: Core object models and prompt templates
2. **Cross-Project Resources**: Resources shared between multiple projects
3. **System Metadata**: Information about projects, clients, usage, and billing

Key tables in the public schema include:

```sql
-- Projects table to track all projects
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    client_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    settings JSONB
);

-- Object models for content generation
CREATE TABLE object_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    structure JSONB NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Prompt templates for LLM interactions
CREATE TABLE prompts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    template TEXT NOT NULL,
    parameters JSONB,
    object_model_id UUID REFERENCES object_models(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- LLM API usage tracking
CREATE TABLE llm_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    prompt_id UUID REFERENCES prompts(id),
    tokens_in INTEGER NOT NULL,
    tokens_out INTEGER NOT NULL,
    model VARCHAR(100) NOT NULL,
    cost NUMERIC(10, 6) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Client information
CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255),
    api_key VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## Project Schemas

Each project schema is created dynamically when a new project is added to the system. The schema name follows the pattern `project_{id}` where `{id}` is the project ID.

Key tables in the project-specific schemas include:

```sql
-- Generated content for this project
CREATE TABLE contents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255),
    body TEXT NOT NULL,
    object_model_id UUID NOT NULL,  -- References public.object_models
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Project-specific metadata
CREATE TABLE metadata (
    key VARCHAR(255) PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Project-specific vocabulary
CREATE TABLE vocabulary (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    term VARCHAR(255) NOT NULL,
    definition TEXT NOT NULL,
    category VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Project-adapted prompt components
CREATE TABLE prompt_components (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    base_prompt_id UUID,  -- References public.prompts
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## Data Flow Between Schemas

The system follows a defined pattern for data flow between the public schema and project schemas:

1. **Object Model Instantiation**:
   - Object models are defined in the public schema
   - When content is generated for a project, the resulting data is stored in the project schema
   - References to the original object model are maintained

2. **Prompt Adaptation**:
   - Base prompts are defined in the public schema
   - Project-specific adaptations are stored in the project schema
   - Usage tracking is recorded in the public schema

Example of cross-schema data flow:

```python
# Generate content with an object model
def generate_project_content(project_id, object_model_id, input_data):
    # Fetch object model from public schema
    object_model = db.fetch_one(
        "SELECT * FROM public.object_models WHERE id = %s",
        (object_model_id,)
    )
    
    # Generate content
    content = generate_from_model(object_model, input_data)
    
    # Store in project schema
    db.execute(
        f"INSERT INTO project_{project_id}.contents "
        "(title, body, object_model_id, metadata) "
        "VALUES (%s, %s, %s, %s)",
        (content["title"], content["body"], object_model_id, json.dumps(content["metadata"]))
    )
    
    # Record usage in public schema
    db.execute(
        "INSERT INTO public.llm_usage "
        "(project_id, prompt_id, tokens_in, tokens_out, model, cost) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (project_id, prompt_id, tokens_in, tokens_out, model_name, calculated_cost)
    )
```

## Schema Creation and Management

Project schemas are created automatically when a new project is added to the system. The `SchemaSetup` class handles this process:

```python
from services.database import DBOperator

class SchemaSetup:
    def __init__(self, db: DBOperator):
        self.db = db
    
    def create_project_schema(self, project_id: int):
        """Create a new schema for a project with all required tables."""
        schema_name = f"project_{project_id}"
        
        # Create the schema
        self.db.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
        
        # Create tables in the new schema
        self.db.execute(f"""
            CREATE TABLE IF NOT EXISTS {schema_name}.contents (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                title VARCHAR(255),
                body TEXT NOT NULL,
                object_model_id UUID NOT NULL,
                metadata JSONB,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create additional tables...
        # ...
```

## Accessing Schema Data

To access data from either the public schema or a project schema:

```python
from services.database import DBOperator

# Create a database operator
db = DBOperator()

# Access data from public schema
projects = db.fetch_all("SELECT * FROM public.projects")
object_models = db.fetch_all("SELECT * FROM public.object_models")

# Access data from project schema
project_id = 123
contents = db.fetch_all(f"SELECT * FROM project_{project_id}.contents")
vocabulary = db.fetch_all(f"SELECT * FROM project_{project_id}.vocabulary")

# Cross-schema query
joined_data = db.fetch_all(f"""
    SELECT c.*, o.name as model_name 
    FROM project_{project_id}.contents c
    JOIN public.object_models o ON c.object_model_id = o.id
""")
```

## Schema Upgrades and Migrations

When the database structure needs to be updated:

1. **Public Schema**: Updates affect all projects and require careful planning
2. **Project Schemas**: Updates can be done selectively or for all projects

The system provides migration utilities to handle schema updates:

```python
from services.database import DBOperator, SchemaSetup

def upgrade_all_project_schemas(db: DBOperator):
    """Upgrade all project schemas to the latest version."""
    # Get all projects
    projects = db.fetch_all("SELECT id FROM public.projects")
    
    # Update each project schema
    for project in projects:
        project_id = project["id"]
        schema_name = f"project_{project_id}"
        
        # Add new column to contents table
        db.execute(f"""
            ALTER TABLE {schema_name}.contents
            ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1
        """)
        
        # Other schema updates...
```

## Schema Best Practices

1. **Keep the public schema clean**: Only store truly shared resources
2. **Consistent naming**: Use consistent naming patterns across schemas
3. **Schema references**: Always use fully qualified names (schema.table) in queries
4. **Ownership clarity**: Clearly document ownership and responsibility for each schema
5. **Access control**: Set appropriate permissions on schemas and tables
6. **Cross-schema joins**: Minimize joins across schemas for better performance
7. **Schema isolation**: Design project schemas to function without tight coupling
8. **Schema documentation**: Maintain clear documentation of schema structure
9. **Version tracking**: Track schema versions to manage migrations

By following this architecture, the content generator system maintains clear separation between shared resources and project-specific data, enabling efficient data management and project isolation. 