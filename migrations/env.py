from __future__ import with_statement
from flask import current_app
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import logging
from app.app import create_app
from app.db import db

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

try:
    app = current_app._get_current_object()
except RuntimeError:
    app = create_app()
config.set_main_option('sqlalchemy.url',
                       app.config.get('SQLALCHEMY_DATABASE_URI'))
target_metadata = db.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def compare_type(context, inspected_column, metadata_column, inspected_type,
                 metadata_type):
    if type(metadata_type) == db.Boolean:
        if type(inspected_type) == mysql.base.TINYINT:
            return False


def compare_server_default(context, inspected_column, metadata_column,
                           inspected_default, metadata_default,
                           rendered_metadata_default):
    if type(metadata_column.type) == db.Boolean:
        if type(inspected_column['type']) == mysql.base.TINYINT:
            if inspected_default == "'1'":
                return metadata_default == true
            elif inspected_default == "'0'":
                return metadata_default == false


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    engine = engine_from_config(config.get_section(config.config_ini_section),
                                prefix='sqlalchemy.',
                                poolclass=pool.NullPool)

    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=compare_type,
        compare_server_default=compare_server_default,
        # process_revision_directives=process_revision_directives,
        # **app.extensions['migrate'].configure_args
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
