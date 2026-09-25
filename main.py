

import difflib

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, init_db
from models import Book, ShelfRange

app = FastAPI(title="Library Locator MVP")


@app.on_event("startup")
def on_startup():
    init_db()


def get_session() -> Session:
    return SessionLocal()


def find_matching_books(db: Session, query: str):
    query = query.strip()
    if not query:
        return []

    like = f"%{query}%"
    exact_matches = (
        db.query(Book)
        .filter((Book.title.ilike(like)) | (Book.author.ilike(like)))
        .all()
    )
    if exact_matches:
        return exact_matches

    # Fuzzy fallback: suggest close title matches so a typo or partial
    # memory of the title still finds something.
    all_books = db.query(Book).all()
    titles = [b.title for b in all_books]
    close = difflib.get_close_matches(query, titles, n=3, cutoff=0.5)
    return [b for b in all_books if b.title in close]


def locate_call_number(db: Session, call_number: str):
    call_number = call_number.strip().upper()
    ranges = db.query(ShelfRange).all()
    for r in ranges:
        if r.call_number_start.upper() <= call_number <= r.call_number_end.upper():
            return r
    return None


@app.get("/search")
def search(q: str):
    db = get_session()
    try:
        books = find_matching_books(db, q)
        return [
            {"id": b.id, "title": b.title, "author": b.author,
             "call_number": b.call_number, "category": b.category}
            for b in books
        ]
    finally:
        db.close()


@app.get("/locate")
def locate(call_number: str):
    db = get_session()
    try:
        r = locate_call_number(db, call_number)
        if not r:
            raise HTTPException(status_code=404, detail="No shelf range found for that call number.")
        return {
            "floor": r.floor, "aisle": r.aisle, "shelf": r.shelf,
            "directions": r.directions_text,
        }
    finally:
        db.close()


@app.get("/find")
def find(q: str):
    db = get_session()
    try:
        books = find_matching_books(db, q)
        if not books:
            raise HTTPException(status_code=404, detail="No books matched your search.")

        results = []
        for b in books:
            r = locate_call_number(db, b.call_number)
            results.append({
                "title": b.title,
                "author": b.author,
                "call_number": b.call_number,
                "category": b.category,
                "location": {
                    "floor": r.floor, "aisle": r.aisle, "shelf": r.shelf,
                    "directions": r.directions_text,
                } if r else None,
            })
        return results
    finally:
        db.close()
