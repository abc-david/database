# cursor_files Directory

This directory contains utility scripts that are meant to be temporary or one-off tools for development and debugging purposes. According to the project organization rules, files in this directory:

1. Are not meant to be permanent parts of the codebase
2. Should not be imported by core functionality
3. May be deleted or cleaned up periodically
4. Are useful for development, debugging, or one-time tasks

## Current Utilities

- `schema_inspector.py`: Utility for inspecting database schemas
- `sample_operations.py`: Examples of common database operations
- `query_runner.py`: Tool for running ad-hoc database queries

## Usage

These utilities are primarily for development use. If you find yourself frequently using functionality from these files, consider:

1. Refactoring the code into a proper utility in the parent directory
2. Adding tests for the functionality
3. Documenting the API

## Cleanup

Files in this directory may be removed during cleanup operations if they appear to be outdated or unused. If you want to preserve a utility, consider moving it to the main utils directory and adding proper documentation. 