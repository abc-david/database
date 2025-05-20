# Database Design

## Overview

The Content Generation Framework uses PostgreSQL with a schema-per-project approach to provide robust storage while maintaining complete isolation between projects. This document describes the database design, including schema organization, table structures, and the use of JSONB for flexible content storage.

## Schema Organization

### Project-Based Schema Isolation

Each content project in the framework gets its own PostgreSQL schema:

```
content_db
  ├── public schema (system tables)
  │    ├── projects - Project metadata
  │    └── object_models - Global object model definitions
  ├── project_1_schema
  │    ├── object_type_templates - Project-specific template customizations
  │    ├── workflows
  │    └── contents
  ├── project_2_schema
  │    ├── object_type_templates - Project-specific template customizations
  │    ├── workflows
  │    └── contents
  └── ...
```

This approach provides several benefits:
- Complete isolation between projects
- Independent backup and restore capabilities
- Simplified access control
- Ability to archive or migrate individual projects

## Core Tables

### Projects Table (Public Schema)

The projects table in the public schema tracks all content projects:

```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    schema_name VARCHAR(63) NOT NULL UNIQUE,
    description JSONB NOT NULL DEFAULT '{}',
    settings JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

Key fields:
- `id`: Unique identifier for the project
- `name`: Human-readable project name
- `schema_name`: PostgreSQL schema name (derived from project name)
- `description`: JSONB field containing project metadata, hierarchies, and vocabularies
- `settings`: JSONB field containing project settings

### Object Models Table (Public Schema)

```sql
CREATE TABLE public.object_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    version VARCHAR(20) NOT NULL DEFAULT '1.0',
    definition JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

This table stores global content type definitions which are used as the base templates for all projects. These define the standard structure, validation rules, and metadata schema for different object types.

### Project-Specific Tables

Each project schema contains the following tables:

#### Object Type Templates Table

```sql
CREATE TABLE {project.schema_name}.object_type_templates (
    id SERIAL PRIMARY KEY,
    object_type TEXT NOT NULL,
    template JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(object_type)
);
```

This table stores project-specific customizations and extensions to the global object model definitions. This allows projects to add fields or override defaults while inheriting the core structure from the global templates.

#### Workflows Table

```sql
CREATE TABLE {project.schema_name}.workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    settings JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

This table organizes content generation tasks within a project.

#### Contents Table

```sql
CREATE TABLE {project.schema_name}.contents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_type VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    content JSONB NOT NULL,
    metadata JSONB DEFAULT '{}',
    workflow_id UUID REFERENCES {project.schema_name}.workflows(id),
    published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

This table stores all generated content with flexible JSONB fields for content and metadata.

## Model Definition System

### Two-Tier Template Approach

The framework implements a two-tier approach to object templates:

1. **Global Object Models** (`public.object_models`): 
   - Define standard structure and validation rules for different content types across the entire application
   - Serve as the "master templates" for all projects
   - Ensure consistency in core object properties

2. **Project-Specific Templates** (`{schema_name}.object_type_templates`): 
   - Allow for project-level customization and extension of the global templates
   - Accommodate specific metadata needs or LLM-determined structures
   - Enable projects to experiment with new fields without affecting global definitions

This approach provides:
- **Standardization**: Global templates ensure consistency across the application
- **Flexibility**: Project templates allow for customization and specialization
- **Inheritance**: Projects inherit from global templates but can override or extend them
- **Evolution**: Projects can experiment with new metadata structures without affecting the core models

For example, a global "Product" template might define standard fields like name, price, and SKU, while a project-specific template could add fields like "sustainability_score" or "seasonal_relevance" based on that project's specific needs.

## JSONB Structure

### Project Description

The project's `description` field uses a structured JSONB format:

```json
{
  "about": "Technology blog focusing on AI and machine learning",
  "main_topic": "Artificial Intelligence",
  "target_audience": "Software developers and data scientists",
  "topic_hierarchy": {
    "id": "tech-123",
    "name": "Technology",
    "slug": "technology",
    "subtopics": [
      { 
        "id": "ai-456",
        "name": "AI", 
        "slug": "ai",
        "subtopics": []
      },
      { 
        "id": "prog-789",
        "name": "Programming", 
        "slug": "programming",
        "subtopics": []
      }
    ]
  },
  "category_hierarchy": {
    "id": "products-abc",
    "name": "Products",
    "slug": "products",
    "subcategories": [
      {
        "id": "laptops-def",
        "name": "Laptops",
        "slug": "laptops",
        "subcategories": []
      }
    ]
  },
  "vocabularies": {
    "VALID_CONTENT_TYPES": [
      "article", "tutorial", "review", "comparison"
    ],
    "VALID_DIFFICULTY_LEVELS": [
      "beginner", "intermediate", "advanced", "expert"
    ],
    "known_tags": {
      "type": "dynamic",
      "values": ["python", "javascript", "ai", "machine-learning"],
      "suggestions_only": true
    }
  }
}
```

### Object Model Definition

Object models use a structured JSONB format for flexible definitions:

```json
{
  "name": "BlogPost",
  "fields": {
    "title": {
      "type": "str",
      "args": {
        "description": "The post title"
      }
    },
    "content": {
      "type": "str",
      "args": {
        "description": "The post content"
      }
    },
    "key_takeaways": {
      "type": "List[str]",
      "args": {
        "description": "Key points for readers to remember"
      }
    }
  },
  "metadata_schema": {
    "required": [
      "content_type", "tags", "categories"
    ],
    "recommended": [
      "difficulty_level", "estimated_reading_time", "keywords"
    ],
    "controlled_vocabularies": {
      "content_type": {
        "reference_type": "project_vocabulary",
        "vocabulary_name": "VALID_CONTENT_TYPES"
      },
      "difficulty_level": {
        "reference_type": "project_vocabulary",
        "vocabulary_name": "VALID_DIFFICULTY_LEVELS"
      }
    }
  }
}
```

## Database Operations

The Content Generator uses a direct SQL approach rather than an ORM system, providing better performance and schema flexibility.

### Key Database Functions

The framework provides these main database operation classes:

1. **DBConnector**: Low-level connection management
2. **DBOperator**: High-level database operations
3. **SchemaSetup**: Schema creation and management

### Project Creation Process

When a new project is created:

1. A record is inserted in `public.projects` with a UUID
2. A new schema named `project_{uuid}` is created
3. Project-specific tables are created in the new schema
4. Default settings are populated based on project type
5. Permissions are set up for appropriate access

### Content Storage Process

When content is generated:

1. Object model definition is retrieved from `public.object_models`
2. Content is validated against the model definition
3. Content is stored in `{project_schema}.contents`
4. Metadata is stored in the content row's `metadata` JSONB field
5. Related tables are updated as needed (e.g., tags, categories)

## Query Patterns

### Across-Project Queries

To find content across all projects:

```sql
-- Find all content with a specific tag
WITH project_schemas AS (
  SELECT schema_name FROM public.projects
)
SELECT 
  p.name AS project_name,
  c.id,
  c.title,
  c.content_type
FROM 
  project_schemas ps
CROSS JOIN LATERAL (
  SELECT * FROM information_schema.tables 
  WHERE table_schema = ps.schema_name AND table_name = 'contents'
) t
CROSS JOIN LATERAL (
  SELECT * FROM (
    SELECT id, title, content_type 
    FROM "query_execution"(
      format('SELECT id, title, content_type FROM %I.contents 
              WHERE metadata::jsonb @> ''{"tags": ["ai"]}''', ps.schema_name)
    ) AS (id UUID, title TEXT, content_type TEXT)
  ) sub
) c
JOIN public.projects p ON p.schema_name = ps.schema_name;
```

### Project-Specific Queries

To find content within a project:

```sql
-- Find content in a specific project
SELECT 
  id, 
  title, 
  content->>'body' AS body,
  metadata->>'author' AS author
FROM 
  project_abc123.contents
WHERE 
  content_type = 'article'
  AND metadata->>'difficulty_level' = 'beginner';
```

### JSONB Query Examples

The system makes extensive use of PostgreSQL's JSONB capabilities:

```sql
-- Find content with specific metadata values
SELECT * FROM project_abc123.contents
WHERE metadata @> '{"tags": ["postgresql", "jsonb"]}';

-- Find content with nested JSONB properties
SELECT * FROM project_abc123.contents
WHERE content->'sections'->0->'title' ? 'Introduction';

-- Text search within JSONB fields
SELECT * FROM project_abc123.contents
WHERE content->>'body' ILIKE '%database design%';
```

## Schema Evolution

As the system evolves, schema changes are handled through:

1. **Schema Versioning**: Each schema has a version number
2. **Migration Scripts**: Automated updates for schema changes
3. **Compatibility Layer**: For handling different schema versions

## References

- [PostgreSQL JSONB Documentation](https://www.postgresql.org/docs/current/datatype-json.html)
- [Schema Design Best Practices](https://www.postgresql.org/docs/current/ddl-schemas.html) 