# Nomi Backend

FastAPI backend for the Nomi task and inspiration management application.

## Database Migrations

This project uses [Alembic](https://alembic.sqlalchemy.org/) for database migrations with async SQLAlchemy support.

### Initial Setup

The database migrations are already configured. When you start the devcontainer, PostgreSQL will be running automatically.

### Creating a New Migration

When you add or modify SQLAlchemy models, generate a migration:

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Example: Adding a new table
alembic revision --autogenerate -m "Add tasks table"

# Example: Modifying an existing table
alembic revision --autogenerate -m "Add priority field to tasks"
```

**Important:** Always review the auto-generated migration file in `alembic/versions/` before applying it. Alembic may not detect all changes correctly.

### Applying Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply one migration at a time
alembic upgrade +1

# Rollback one migration
alembic downgrade -1

# Rollback all migrations
alembic downgrade base
```

### Checking Migration Status

```bash
# Show current migration version
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic history --verbose
```

### Common Migration Scenarios

#### Adding a New Table

1. Create your SQLAlchemy model in `app/features/{feature}/model.py`
2. Import the model in `alembic/env.py` (if not using wildcard import)
3. Generate migration: `alembic revision --autogenerate -m "Add {table} table"`
4. Review the generated file in `alembic/versions/`
5. Apply: `alembic upgrade head`

#### Modifying an Existing Table

1. Update your SQLAlchemy model
2. Generate migration: `alembic revision --autogenerate -m "Update {table}"`
3. Review the migration - check for:
   - Data migrations needed
   - Index changes
   - Constraint changes
4. Apply: `alembic upgrade head`

#### Creating a Manual Migration

For complex changes that autogenerate can't handle:

```bash
# Create empty migration
alembic revision -m "Custom migration description"

# Edit the generated file in alembic/versions/
# Add your upgrade() and downgrade() logic
```

### Troubleshooting

**Migration fails with "relation already exists":**
- Check if the table was created manually
- Review migration history: `alembic current`
- Consider using `alembic stamp head` to mark current state (careful!)

**Autogenerate doesn't detect changes:**
- Ensure your model imports are correct in `alembic/env.py`
- Check that `target_metadata` is set to `Base.metadata`
- Some changes (like column type changes) may need manual migrations

**Database connection errors:**
- Verify PostgreSQL is running: `docker ps`
- Check DATABASE_URL in `.env` file
- Ensure you're in the devcontainer environment

## Development

### Running the Application

```bash
# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_database.py

# Run with coverage
pytest --cov=app
```

### Code Quality

```bash
# Format code with Black
black .

# Lint with Ruff
ruff check .

# Auto-fix linting issues
ruff check --fix .
```

## Project Structure

```
nomi-backend/
├── app/
│   ├── core/
│   │   ├── config.py         # Environment configuration
│   │   └── database.py       # Database engine and session factory
│   ├── features/
│   │   └── users/
│   │       └── model.py      # User SQLAlchemy model
│   └── main.py               # FastAPI application
├── alembic/
│   ├── versions/             # Migration scripts
│   └── env.py                # Alembic environment config
├── tests/
│   └── test_database.py      # Database integration tests
├── alembic.ini               # Alembic configuration
├── requirements.txt          # Python dependencies
└── pyproject.toml            # Tool configuration
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `ENVIRONMENT` - development/production
- `DEBUG` - Enable debug mode

## License

[Add license information]
