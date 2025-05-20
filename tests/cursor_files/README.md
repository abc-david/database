# Test cursor_files Directory

This directory contains test scripts that are meant to be temporary or one-off tests for development and debugging purposes. According to the project organization rules, files in this directory:

1. Are not meant to be part of the permanent test suite
2. May contain ad-hoc tests for specific issues or features
3. May be deleted or cleaned up periodically
4. Are useful for development, debugging, or quick verification

## Usage

When implementing or debugging features, you can add temporary test files here without affecting the main test suite. These tests are intended for:

- Exploring the behavior of a specific database feature
- Testing fixes for specific issues
- Verifying behavior in isolation
- Quick one-off tests during development

## Cleanup

Files in this directory may be removed during cleanup operations. If you develop a test that should be preserved, consider moving it to the main tests directory and ensuring it follows the proper test structure and naming conventions. 