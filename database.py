"""
Database connection setup.

Uses SQLite by default so the demo runs with zero setup. To point this
at Postgres later (e.g. on Railway), just set the DATABASE_URL
environment variable, e.g.:

    postgresql://user:password@host:port/dbname

No other code needs to change.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./library.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
