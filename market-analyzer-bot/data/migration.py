from alembic import command
from alembic.config import Config

def run_migrations():
    # Set up the Alembic configuration
    alembic_cfg = Config("alembic.ini")
    # Autogenerate and apply migrations
    command.upgrade(alembic_cfg, "head")