"""Database configuration for the Trading Order Management System.

This module handles the database connection setup and session management.
It provides the database engine configuration, session factory, and a
dependency function for FastAPI to manage database sessions.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

# Get database URL from environment variable or use SQLite as default
DATABASE_URL = getenv("DATABASE_URL", "sqlite:///./orders.db")

# Create SQLAlchemy engine with the configured database URL
engine = create_engine(DATABASE_URL)

# Create sessionmaker factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for SQLAlchemy models
Base = declarative_base()

def get_db():
    """FastAPI dependency for database session management.

    Creates a new database session for each request and ensures
    proper cleanup after the request is completed.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()