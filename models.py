"""
Database models for the Library Locator MVP.

Two tables:
- Book: sample catalog records (title, author, call_number, category)
- ShelfRange: maps a call-number range to a physical shelf location

In the real version, `Book` data would come from the library's own
catalog/API instead of living in your own database.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    call_number = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)


class ShelfRange(Base):
    __tablename__ = "shelf_ranges"

    id = Column(Integer, primary_key=True, index=True)
    # Call numbers are compared as strings using simple alphabetical
    # ordering, which works fine for a demo. A production version would
    # want a proper call-number parser (Dewey or LC).
    call_number_start = Column(String, nullable=False)
    call_number_end = Column(String, nullable=False)
    floor = Column(String, nullable=False)
    aisle = Column(String, nullable=False)
    shelf = Column(String, nullable=False)
    directions_text = Column(String, nullable=False)
