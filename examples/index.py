"""
MODULE: services/database/examples/index.py
PURPOSE: Provides a centralized entry point to run database examples
CLASSES:
    - None
FUNCTIONS:
    - list_examples: Lists all available examples
    - run_example: Runs a selected example
    - main: Entry point for the example runner
DEPENDENCIES:
    - os: For directory operations
    - importlib: For dynamic module imports
    - sys: For system operations

This module serves as a central hub for running all the example scripts in the
database services package. It provides a simple command-line interface to list
and run examples that demonstrate various features of the database services.

Example usage:
```
# List all available examples
python services/database/examples/index.py list

# Run a specific example
python services/database/examples/index.py run mock_db_example
```
"""

import os
import sys
import importlib
from pathlib import Path
from typing import List, Dict, Optional

def list_examples() -> List[Dict[str, str]]:
    """
    List all available examples in the examples directory.
    
    Returns:
        List of dictionaries containing example information
    """
    examples = []
    current_dir = Path(__file__).parent
    
    for file_path in current_dir.glob("*.py"):
        if file_path.name in ("__init__.py", "index.py"):
            continue
            
        module_name = file_path.stem
        
        # Try to import the module to get its docstring
        try:
            module = importlib.import_module(f"services.database.examples.{module_name}")
            description = module.__doc__.split("PURPOSE:")[1].split("\n")[0].strip() if module.__doc__ else "No description"
        except Exception:
            description = "Could not load description"
        
        examples.append({
            "name": module_name,
            "description": description,
            "path": str(file_path)
        })
    
    return sorted(examples, key=lambda x: x["name"])

def run_example(example_name: str) -> int:
    """
    Run a specific example.
    
    Args:
        example_name: The name of the example to run
        
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    examples = list_examples()
    matching_examples = [ex for ex in examples if ex["name"] == example_name]
    
    if not matching_examples:
        print(f"Error: Example '{example_name}' not found.")
        print("Use 'python services/database/examples/index.py list' to see available examples.")
        return 1
    
    example = matching_examples[0]
    
    print(f"\n=== Running Example: {example['name']} ===")
    print(f"Description: {example['description']}")
    print("=" * 60)
    
    try:
        module = importlib.import_module(f"services.database.examples.{example_name}")
        if hasattr(module, "main"):
            module.main()
        else:
            print(f"Error: The example '{example_name}' does not have a main() function.")
            return 1
        return 0
    except Exception as e:
        print(f"\nError running example '{example_name}':")
        print(f"  {type(e).__name__}: {e}")
        return 1

def print_usage() -> None:
    """
    Print usage information.
    """
    print("Usage:")
    print("  python services/database/examples/index.py list")
    print("  python services/database/examples/index.py run <example_name>")
    print("\nCommands:")
    print("  list               List all available examples")
    print("  run <example_name> Run a specific example")

def main() -> int:
    """
    Entry point for the example runner.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    if len(sys.argv) < 2:
        print_usage()
        return 1
    
    command = sys.argv[1].lower()
    
    if command == "list":
        examples = list_examples()
        print("\nAvailable Examples:")
        print("-" * 80)
        for i, example in enumerate(examples):
            print(f"{i+1}. {example['name']}")
            print(f"   {example['description']}")
            print()
        
        print(f"\nFound {len(examples)} examples.")
        print("\nTo run an example:")
        print("  python services/database/examples/index.py run <example_name>")
        return 0
    
    elif command == "run":
        if len(sys.argv) < 3:
            print("Error: Missing example name.")
            print_usage()
            return 1
        
        example_name = sys.argv[2]
        return run_example(example_name)
    
    else:
        print(f"Error: Unknown command '{command}'.")
        print_usage()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 