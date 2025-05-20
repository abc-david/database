# Database Credentials Management

## Overview

This document explains how to manage and access database credentials securely in the content generator system. Proper credential management is crucial for database security and deployment flexibility.

## Credential Storage

The system uses a multi-layered approach to manage database credentials:

1. **Configuration Files**: Default non-sensitive configurations
2. **Environment Variables**: Sensitive credentials in production
3. **Local Overrides**: Development-specific settings

## Settings Structure

Database credentials are stored in the configuration system:

```python
# Located in /config/settings.py
DATABASE_CONFIG = {
    "prod": {
        "host": "localhost",  # Default, overridden by env vars in production
        "dbname": "content_generator_prod",
        "user": "",  # Empty by default, must be provided
        "password": "",  # Empty by default, must be provided
        "port": 5432
    },
    "test": {
        "host": "localhost",
        "dbname": "content_generator_test",
        "user": "",
        "password": "",
        "port": 5432
    }
}
```

## Environment Variables

In production environments, credentials should be provided through environment variables:

| Environment Variable | Description | Example |
|----------------------|-------------|---------|
| `DB_PROD_HOST` | Production database host | `db.example.com` |
| `DB_PROD_NAME` | Production database name | `content_generator_prod` |
| `DB_PROD_USER` | Production database username | `cg_prod_user` |
| `DB_PROD_PASSWORD` | Production database password | `StrongPassword123!` |
| `DB_PROD_PORT` | Production database port | `5432` |
| `DB_TEST_HOST` | Test database host | `localhost` |
| `DB_TEST_NAME` | Test database name | `content_generator_test` |
| `DB_TEST_USER` | Test database username | `cg_test_user` |
| `DB_TEST_PASSWORD` | Test database password | `TestPassword123!` |
| `DB_TEST_PORT` | Test database port | `5432` |

## Setting Environment Variables

### For Linux/macOS

```bash
# Add to ~/.bashrc or ~/.zshrc
export DB_PROD_USER="your_username"
export DB_PROD_PASSWORD="your_password"
export DB_TEST_USER="test_username"
export DB_TEST_PASSWORD="test_password"
```

Then run:

```bash
source ~/.bashrc  # or source ~/.zshrc
```

### For Development in a Virtual Environment

Create a `.env` file in your project root:

```
# .env file (DO NOT COMMIT THIS FILE)
DB_PROD_USER=dev_username
DB_PROD_PASSWORD=dev_password
DB_TEST_USER=test_username
DB_TEST_PASSWORD=test_password
```

Then load these variables when activating your virtual environment:

```bash
# Add to venv/bin/activate
set -a
source /path/to/project/.env
set +a
```

## Accessing Credentials in Code

The system provides a centralized way to access credentials:

```python
from config.settings import get_database_config

# Get production database config
prod_config = get_database_config("prod")
# Returns: {"host": "...", "dbname": "...", "user": "...", "password": "...", "port": ...}

# Get test database config
test_config = get_database_config("test")
```

The `get_database_config` function merges default settings with environment variables.

## Automatic Usage with DBConnector

The `DBConnector` class automatically uses the proper credentials:

```python
from services.database import DBConnector

# Create a connection to the production database
prod_db = DBConnector(env="prod")

# Create a connection to the test database
test_db = DBConnector(env="test")
```

## Local Development Setup

For local development:

1. Create a file named `local_settings.py` in the `/config` directory:

```python
# /config/local_settings.py (not version controlled)
LOCAL_DATABASE_CONFIG = {
    "prod": {
        "user": "local_dev_user",
        "password": "local_dev_password"
    },
    "test": {
        "user": "local_test_user",
        "password": "local_test_password"
    }
}
```

2. The settings system will automatically merge these local settings with the default configuration.

## CI/CD Pipeline Configuration

In CI/CD environments, set database credentials as secrets or environment variables:

### GitHub Actions Example

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    env:
      DB_TEST_USER: ${{ secrets.DB_TEST_USER }}
      DB_TEST_PASSWORD: ${{ secrets.DB_TEST_PASSWORD }}
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest
```

## Rotating Credentials

Best practices for credential rotation:

1. Generate new credentials in the database
2. Update environment variables or CI/CD secrets
3. Restart services to pick up new credentials
4. Revoke old credentials after confirming new ones work

## Credential Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment-specific credentials** (different for prod/test)
3. **Rotate credentials** periodically
4. **Use least privilege accounts** for each environment
5. **Encrypt credentials** in transit and at rest
6. **Audit credential access** regularly

## Troubleshooting

If you encounter database connection issues:

1. Check that environment variables are correctly set
2. Verify the database user has proper permissions
3. Ensure the database server allows connections from your IP
4. Check firewall rules allow connections on the database port

Common error: `psycopg2.OperationalError: FATAL: password authentication failed for user`
- Solution: Verify the correct username and password are set in environment variables

## Setting Up a New Environment

To configure credentials for a new environment:

1. Create database users with appropriate permissions
2. Add the configuration to `/config/settings.py`
3. Set up environment variables for the new environment
4. Update documentation for the team 