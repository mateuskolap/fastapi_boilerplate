from sqlalchemy.orm import registry
from sqlalchemy_declarative_extensions import declarative_database

table_registry = declarative_database(registry())
