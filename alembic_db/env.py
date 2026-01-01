# These imports are required at runtime but may not be available in the linter environment
# They are installed via requirements.txt (alembic, SQLAlchemy)
try:
    from sqlalchemy import engine_from_config  # type: ignore
    from sqlalchemy import pool  # type: ignore
    from alembic import context  # type: ignore
except ImportError as exc:
    # This file is only used when alembic is installed
    # The import error here is expected in linter environments
    raise ImportError(
        "alembic and sqlalchemy are required. Install with: pip install alembic SQLAlchemy"
    ) from exc

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


from app.database.models import Base
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    This configures the context with a connection to the database.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
