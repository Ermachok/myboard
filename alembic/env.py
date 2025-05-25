import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import create_engine, pool

from alembic import context

load_dotenv()

from app.db.database import Base
from app.models.board import Board
from app.models.task import Task
from app.models.user import User

config = context.config

fileConfig(config.config_file_name)

target_metadata = Base.metadata

SYNC_DB_URL = os.getenv("SYNC_DATABASE_URL")

print(SYNC_DB_URL, target_metadata)


def run_migrations_offline():
    context.configure(
        url=SYNC_DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(
        SYNC_DB_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
