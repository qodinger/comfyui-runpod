# Alembic Database Migrations

This directory contains Alembic configuration and migration scripts for managing database schema changes in ComfyUI.

## What is Alembic?

Alembic is a database migration tool for SQLAlchemy. It allows you to version control your database schema and apply incremental changes (migrations) to keep your database in sync with your application code.

## Directory Structure

- `env.py` - Alembic environment configuration
- `script.py.mako` - Template for generating migration scripts
- `versions/` - Directory containing migration revision files (created automatically)

## Quick Start

### 1. Create a New Migration

After updating models in `app/database/models.py`:

```bash
# Generate a new migration automatically
alembic revision --autogenerate -m "Description of changes"

# Or create an empty migration to write manually
alembic revision -m "Description of changes"
```

### 2. Apply Migrations

```bash
# Upgrade to the latest version
alembic upgrade head

# Upgrade to a specific revision
alembic upgrade <revision_id>

# Upgrade one step at a time
alembic upgrade +1
```

### 3. Rollback Migrations

```bash
# Downgrade one step
alembic downgrade -1

# Downgrade to a specific revision
alembic downgrade <revision_id>

# Downgrade to base (removes all migrations)
alembic downgrade base
```

## Common Commands

### Check Current Database Version

```bash
alembic current
```

### View Migration History

```bash
# Show all revisions
alembic history

# Show detailed history
alembic history --verbose
```

### Show Pending Migrations

```bash
alembic heads
```

## Configuration

- **Database URL**: Configured via `--database-url` CLI argument (default: `sqlite:///user/comfyui.db`)
- **Script Location**: Set in `alembic.ini` (default: `alembic_db`)
- **Models Location**: `app/database/models.py`

## Workflow

1. **Define Models**: Add or modify SQLAlchemy models in `app/database/models.py`
2. **Generate Migration**: Run `alembic revision --autogenerate -m "message"`
3. **Review Migration**: Check the generated migration file in `versions/`
4. **Test Migration**: Apply with `alembic upgrade head` and verify
5. **Commit**: Add migration files to version control

## Troubleshooting

### No Target Revision Found

This usually means no migrations exist yet. Create an initial migration:

```bash
alembic revision --autogenerate -m "Initial migration"
```

### Migration Conflicts

If you have multiple heads (branched migrations), merge them:

```bash
alembic merge heads -m "Merge migrations"
```

### Database Out of Sync

If your database schema doesn't match your models:

1. Check current revision: `alembic current`
2. Check target revision: `alembic heads`
3. Apply pending migrations: `alembic upgrade head`

### Import Errors

Ensure you're running Alembic from the project root directory where `alembic.ini` is located.

## Best Practices

- Always review auto-generated migrations before applying
- Use descriptive migration messages
- Test migrations on a development database first
- Keep migrations small and focused
- Never edit existing migration files (create new ones instead)
- Commit migration files to version control

## Related Files

- `alembic.ini` - Alembic configuration file (project root)
- `app/database/models.py` - SQLAlchemy model definitions
- `app/database/db.py` - Database initialization and session management
