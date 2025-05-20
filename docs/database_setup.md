# Database Setup and Management

This document describes the database setup and management processes for the Content Generator project.

## Database Architecture

The Content Generator project uses a PostgreSQL database with the following configuration:

- **Production Database**: Stores actual content, templates, and project data.
- **Test Database**: Used for development and testing purposes.

Each database has two types of schemas:

1. **Public Schema**: Contains global tables like `projects`, `object_models`, and `prompts`.
2. **Project-Specific Schemas**: Each project has its own schema that contains tables for project-specific data.

## Database Tables

### Public Schema Tables

- **object_models**: Defines the structure of content objects.
- **prompts**: Stores prompt templates for generating content.

### Project Schema Tables (per project)

- **contents**: Stores the actual content generated for a project.
- **prompts**: Project-specific prompt adaptations.
- **vocabulary**: Project-specific vocabulary terms and their values.

## Database Setup

### Production Database Setup

The production database should be set up by a database administrator. The database admin should:

1. Create a PostgreSQL database with appropriate name and credentials.
2. Create and configure a database user with appropriate permissions.
3. Run the initial setup scripts to create necessary tables.

### Test Database Setup

For the test database, we have provided several scripts to help with setup and maintenance:

1. **Connection Check**: Use `scripts/check_db_config.py` to verify database connections and permissions.
2. **Database Cleanup**: Use `scripts/clean_test_db.py` to clean up the test database.
3. **Table Creation**: Use `scripts/init_test_db.py` to create essential tables.
4. **SQL Script Generation**: Use `scripts/generate_test_db_sql.py` to generate SQL commands for database administrators.

If you encounter permission issues, generate the SQL commands and have a database administrator execute them:

```bash
python scripts/generate_test_db_sql.py
# Then have an admin run:
# psql -U postgres -f scripts/sql/init_test_db_TIMESTAMP.sql
```

### Synchronizing Production and Test Databases

### Mirroring Tables

The system supports different mirroring types for tables:

- **Full mirroring (structure + data)** - For tables like `object_models` and `prompts`
- **Structure-only mirroring** - For tables like `projects`, where only the schema is needed without copying data

To synchronize the tables from production to test, use:

```bash
python scripts/mirror_prod_tables.py
```

After mirroring table structures, you can populate the test database with seed data:

```bash
python scripts/populate_seed_projects.py
```

This script reads predefined projects from `tests/seed_data/seed_projects.json` and inserts them into the test database.

### Data Synchronization

For more specific data synchronization needs:

```bash
python scripts/sync_test_db.py
```

### Compatible Fields Sync

To ensure field compatibility between databases:

```bash
python scripts/sync_compatible_fields.py
```

### Verification

Always verify that the tables have been correctly synchronized:

```bash
python scripts/verify_tables.py
```

### Fixing Public Schema Permissions

If you encounter "permission denied for schema public" errors, this indicates an issue with the PostgreSQL default permissions. To resolve this:

1. Connect to the database as the postgres superuser:
   ```bash
   # If using peer authentication (common on Linux systems)
   sudo -u postgres psql -d contentgen_test_db
   ```

2. Drop and recreate the public schema with appropriate permissions:
   ```sql
   -- Drop and recreate public schema
   DROP SCHEMA IF EXISTS public CASCADE;
   CREATE SCHEMA public;

   -- Set permissions for test user
   GRANT USAGE ON SCHEMA public TO test_runner_user;
   GRANT CREATE ON SCHEMA public TO test_runner_user;
   GRANT ALL ON SCHEMA public TO test_runner_user;

   -- Set default privileges for future objects
   ALTER DEFAULT PRIVILEGES IN SCHEMA public
   GRANT ALL ON TABLES TO test_runner_user;

   ALTER DEFAULT PRIVILEGES IN SCHEMA public
   GRANT ALL ON SEQUENCES TO test_runner_user;
   ```

3. Alternatively, you can use the provided script that handles this process:
   ```bash
   python scripts/regenerate_public_schema.py --admin-user postgres
   ```

After fixing the permissions, the test user should be able to create and modify tables in the public schema.

## Project Schema Management

When a new project is created:

1. A new schema is created with the project's name or ID.
2. Core tables (`contents`, `prompts`, `vocabulary`) are created in this schema.
3. The project's metadata is stored in the `public.projects` table.

## Database Maintenance

Regular maintenance tasks include:

1. **Backup**: Regular backups of both production and test databases.
2. **Cleanup**: Removing unused schemas and tables from the test database.
3. **Optimization**: Regular database optimization through vacuuming and indexing.
4. **Monitoring**: Monitoring database performance and storage usage.

## Common Issues and Solutions

### Permission Denied Errors

If you encounter permission denied errors, check that your database user has appropriate permissions:

```sql
-- Grant schema permissions
GRANT USAGE ON SCHEMA public TO <user>;
GRANT CREATE ON SCHEMA public TO <user>;

-- Grant table permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO <user>;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO <user>;
```

### Connection Issues

If you're having trouble connecting to the database:

1. Verify that the database server is running.
2. Check your database credentials in `config/settings.py`.
3. Ensure that the database server allows connections from your IP address.

## Database Migration

When making schema changes, follow these guidelines:

1. Document the changes in the appropriate project documentation.
2. Create migration scripts to apply changes to both production and test databases.
3. Test migrations thoroughly in the test database before applying to production.
4. Schedule production migrations during low-traffic periods.

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Database Scripts README](../scripts/README.md)
- [Project Management Module Documentation](../docs/project_management.md) 