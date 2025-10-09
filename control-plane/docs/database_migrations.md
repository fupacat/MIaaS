# Database Migration Strategy

## Overview

MIaaS Control Plane uses SQLAlchemy ORM for database abstraction, designed to support both SQLite (MVP/development) and PostgreSQL (production) with minimal code changes.

## Current Design (MVP)

### SQLite Configuration

- **Database file**: `control_plane.db` (created automatically in control-plane directory)
- **Connection string**: `sqlite:///./control_plane.db`
- **Engine settings**: 
  - `check_same_thread=False` - Allow multi-threaded access
  - Auto-creates tables on startup via `Base.metadata.create_all()`

### Database Models

Located in `app/db/models.py`:

- **NodeDB**: Stores registered agent nodes with capabilities and status
- **DeploymentDB**: Tracks service deployments across nodes

Both models use:
- String primary keys for easy reference
- JSON columns for flexible data storage (capabilities, environment variables)
- Timestamp tracking (created_at, updated_at with auto-update)
- Indexed foreign keys for efficient queries

## Migration to PostgreSQL

### Step 1: Update Database URL

In `app/db/database.py`, change:

```python
# From SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./control_plane.db"

# To PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/miaas"
```

Or use environment variable:

```python
import os
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./control_plane.db"  # fallback
)
```

### Step 2: Install PostgreSQL Driver

```bash
pip install psycopg2-binary
# Update requirements.txt
```

### Step 3: Remove SQLite-specific Settings

```python
# SQLite needs check_same_thread=False, PostgreSQL doesn't
connect_args = {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
```

### Step 4: Test Compatibility

The current models are PostgreSQL-compatible:
- JSON columns work in both databases
- String primary keys work in both
- DateTime fields work in both

## Schema Versioning with Alembic (Future)

For production deployments, Alembic migration tool is recommended for:
- Versioned schema changes
- Safe rollbacks
- Team collaboration on schema updates

### Setup Alembic (when needed)

```bash
# Install Alembic
pip install alembic

# Initialize in control-plane directory
cd control-plane
alembic init alembic

# Configure alembic.ini
# Set sqlalchemy.url to your database URL

# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

### Alembic Configuration

Edit `alembic/env.py` to import models:

```python
from app.db.database import Base
from app.db.models import NodeDB, DeploymentDB

target_metadata = Base.metadata
```

### Migration Workflow

```bash
# Make model changes in app/db/models.py

# Generate migration
alembic revision --autogenerate -m "Add new field"

# Review migration in alembic/versions/

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

## Data Seeding

### For Development

Use the provided seed scripts:

**Shell script (requires running server):**
```bash
./seed_data.sh
```

**Python script (direct database access):**
```bash
python seed_data.py
python seed_data.py --clear  # Clear before seeding
```

### For Production

1. Use proper migration scripts, not seed scripts
2. Back up database before any schema changes
3. Test migrations on staging environment first

## Backup and Recovery

### SQLite

```bash
# Backup
cp control_plane.db control_plane.db.backup

# Restore
cp control_plane.db.backup control_plane.db
```

### PostgreSQL

```bash
# Backup
pg_dump -U user miaas > backup.sql

# Restore
psql -U user miaas < backup.sql
```

## Testing Strategy

### In-Memory Database for Tests

Tests use an in-memory SQLite database for speed and isolation:

```python
SQLALCHEMY_DATABASE_URL = "sqlite://"  # in-memory
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Share connection across threads
)
```

### Test Fixtures

The `conftest.py` provides:
- `setup_database`: Clears tables before each test
- `override_get_db`: Injects test database into FastAPI
- `client`: Configured TestClient

## Database Best Practices

1. **Use environment variables** for connection strings
2. **Never commit database files** to git (in .gitignore)
3. **Always use sessions properly** with try/finally to close
4. **Index foreign keys** for query performance
5. **Use transactions** for multi-step operations
6. **Validate data** with Pydantic before DB operations
7. **Handle SQLAlchemy exceptions** appropriately

## Current Limitations

1. **No automatic migrations**: Schema changes require manual `init_db()` call or db restart
2. **No version tracking**: Can't easily track schema history
3. **No rollback capability**: Can't undo schema changes without backup

These will be addressed when Alembic is integrated (roadmap item).

## Environment Variables

```bash
# Database configuration
DATABASE_URL=sqlite:///./control_plane.db  # or postgresql://...
LOG_LEVEL=INFO

# For production PostgreSQL
DATABASE_URL=postgresql://user:password@db-host:5432/miaas
```

## See Also

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [FastAPI Database Guide](https://fastapi.tiangolo.com/tutorial/sql-databases/)
