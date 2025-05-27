#!/usr/bin/env python3
"""
Script to extract all object_models from SQL dump file and create INSERT statements with IDs
with properly formatted SQL string literals in arrays
"""

import re
import os
import json

# Define paths
DUMP_FILE = "services/database/docs/contentgen_test_db_localhost-2025_05_21_18_02_45-dump.sql"
OUTPUT_FILE = "services/database/docs/object_models_inserts_fixed.sql"

def extract_object_models():
    """Extract all object_models records from the SQL dump file with proper SQL formatting"""
    
    # Check if dump file exists
    if not os.path.exists(DUMP_FILE):
        print(f"Error: Dump file {DUMP_FILE} not found")
        return False
    
    # Read the entire dump file
    with open(DUMP_FILE, 'r') as f:
        content = f.read()
    
    # Find the object_models COPY section
    model_pattern = r"COPY public\.object_models.*?FROM stdin;\n(.*?)\\\.[\n\r]"
    model_match = re.search(model_pattern, content, re.DOTALL)
    
    if not model_match:
        print("Error: Could not find object_models data section")
        return False
    
    # Extract the data rows
    data_section = model_match.group(1).strip()
    rows = data_section.split('\n')
    
    print(f"Found {len(rows)} object_models records")
    
    # Generate INSERT statements
    with open(OUTPUT_FILE, 'w') as f:
        f.write("-- Generated INSERT statements for object_models\n\n")
        
        for row in rows:
            # Split the row by tabs
            fields = row.split('\t')
            if len(fields) < 10:
                print(f"Warning: Invalid row format, skipping")
                continue
            
            # Process use_cases array safely
            use_cases = fields[6]
            if use_cases.startswith('{') and use_cases.endswith('}'):
                use_cases = use_cases[1:-1]  # Remove braces
                
                if not use_cases.strip():
                    # Empty array - cast it properly
                    use_cases_sql = "ARRAY[]::text[]"
                else:
                    # Split by commas, but handle quoted values with commas inside
                    use_cases_items = []
                    in_quotes = False
                    current_item = ""
                    
                    for char in use_cases:
                        if char == '"' and (len(current_item) == 0 or current_item[-1] != '\\'):
                            in_quotes = not in_quotes
                            current_item += char
                        elif char == ',' and not in_quotes:
                            if current_item:
                                use_cases_items.append(current_item)
                            current_item = ""
                        else:
                            current_item += char
                    
                    if current_item:
                        use_cases_items.append(current_item)
                    
                    # Properly format each item as a SQL string literal with single quotes
                    # Handle both quoted and unquoted values correctly
                    formatted_items = []
                    for item in use_cases_items:
                        if item.startswith('"') and item.endswith('"'):
                            # Item was already quoted, replace double quotes with single quotes
                            item_text = item[1:-1]  # Remove the original double quotes
                            # Escape single quotes in the content if any
                            item_text = item_text.replace("'", "''")
                            formatted_items.append(f"'{item_text}'")
                        else:
                            # Item was not quoted
                            # Escape single quotes in the content if any
                            item = item.replace("'", "''")
                            formatted_items.append(f"'{item}'")
                    
                    use_cases_sql = "ARRAY[" + ", ".join(formatted_items) + "]"
            else:
                # Empty array - cast it properly
                use_cases_sql = "ARRAY[]::text[]"
            
            # Process related_templates safely
            related_templates = fields[7]
            if related_templates == '{}':
                # Empty array - cast it properly
                related_templates_sql = "ARRAY[]::text[]"
            else:
                # Keep as is but ensure it's quoted properly
                related_templates_sql = f"'{related_templates}'"
            
            # Create INSERT statement with ID
            insert = f"""INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '{fields[0]}',
  '{fields[1].replace("'", "''")}',
  '{fields[2]}',
  '{fields[3]}',
  '{fields[4].replace("'", "''")}',
  '{fields[5].replace("'", "''")}',
  {use_cases_sql},
  {related_templates_sql},
  '{fields[8]}',
  '{fields[9]}'
);
"""
            f.write(insert + "\n")
    
    print(f"Successfully wrote INSERT statements to {OUTPUT_FILE}")
    return True

if __name__ == "__main__":
    extract_object_models() 