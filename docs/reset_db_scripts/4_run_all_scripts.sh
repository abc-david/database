#!/bin/bash
# Script to run all SQL scripts in sequence to recreate the database tables

echo "Starting database recreation process..."

# Database connection parameters
DB_USER="david"
DB_HOST="localhost"
DB_NAME="content_gen"

# Run the scripts in order
echo "1. Creating tables and constraints..."
psql -U $DB_USER -h $DB_HOST -d $DB_NAME -f services/database/docs/1_create_tables.sql

echo "2. Inserting projects and prompts data..."
psql -U $DB_USER -h $DB_HOST -d $DB_NAME -f services/database/docs/2_insert_projects_prompts.sql

echo "3. Inserting object_models data (top 15 records)..."
psql -U $DB_USER -h $DB_HOST -d $DB_NAME -f services/database/docs/3_insert_object_models.sql

echo "Database recreation completed."

# Verify tables were created
echo "Verifying tables in the public schema..."
psql -U $DB_USER -h $DB_HOST -d $DB_NAME -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE' ORDER BY table_name;"

# Count the number of records in each table
echo "Counting records in each table..."
psql -U $DB_USER -h $DB_HOST -d $DB_NAME -c "SELECT 'object_models' as table_name, COUNT(*) FROM public.object_models UNION ALL SELECT 'projects', COUNT(*) FROM public.projects UNION ALL SELECT 'prompts', COUNT(*) FROM public.prompts ORDER BY table_name;"

echo "Database setup complete." 