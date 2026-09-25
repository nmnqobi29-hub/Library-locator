

from database import SessionLocal, init_db
from models import Book, ShelfRange

SAMPLE_BOOKS = [
    ("Introduction to Algorithms", "Cormen, Cheney, Leiserson", "005.1 COR", "Computer Science"),
    ("Clean Code", "Robert C. Martin", "005.1 MAR", "Computer Science"),
    ("Design Patterns", "Gamma, Helm, Johnson, Vlissides", "005.1 GAM", "Computer Science"),
    ("Database System Concepts", "Silberschatz, Korth", "005.74 SIL", "Computer Science"),
    ("Operating System Concepts", "Silberschatz, Galvin", "005.43 SIL", "Computer Science"),
    ("Principles of Marketing", "Kotler, Armstrong", "658.8 KOT", "Business"),
    ("Financial Accounting", "Weygandt, Kimmel", "657 WEY", "Business"),
    ("Organizational Behavior", "Robbins, Judge", "658.3 ROB", "Business"),
    ("Managerial Economics", "Png, Lehman", "658.155 PNG", "Business"),
    ("Principles of Corporate Finance", "Brealey, Myers", "658.15 BRE", "Business"),
    ("A History of Western Architecture", "David Watkin", "720.9 WAT", "Architecture"),
    ("The Image of the City", "Kevin Lynch", "711.4 LYN", "Architecture"),
    ("Architecture: Form, Space, and Order", "Francis D.K. Ching", "729 CHI", "Architecture"),
    ("Modern Architecture Since 1900", "William J.R. Curtis", "724.6 CUR", "Architecture"),
    ("A Global History of Architecture", "Ching, Jarzombek, Prakash", "720.9 CHJ", "Architecture"),
    ("Made in Africa", "Various", "960 VAR", "Africana & Archives"),
    ("A History of South Africa", "Leonard Thompson", "968 THO", "Africana & Archives"),
    ("The Land Question in South Africa", "Ruth Hall", "968.06 HAL", "Africana & Archives"),
]

SAMPLE_RANGES = [
    # (start, end, floor, aisle, shelf, directions)
    ("000", "099.99", "Level 2", "Aisle C", "Shelf 3",
     "Computer Science (000s) — take the stairs to Level 2, turn right, "
     "it's the 3rd shelving unit down Aisle C."),
    ("600", "699.99", "Level 2", "Aisle F", "Shelf 1",
     "Business & Management (650s) — on Level 2, walk past the seminar "
     "rooms, Aisle F is on your left."),
    ("700", "799.99", "Level 1", "Aisle A", "Shelf 4",
     "Architecture & Arts (700s) — on Level 1, near the entrance, Aisle A, "
     "4th shelving unit."),
    ("900", "999.99", "Level 1", "Aisle B", "Shelf 1",
     "History & Africana (900s) — on Level 1, past Aisle A, look for the "
     "Africana & Archives sign, Aisle B."),
]


def run():
    init_db()
    db = SessionLocal()
    try:
        if db.query(Book).count() == 0:
            for title, author, call_number, category in SAMPLE_BOOKS:
                db.add(Book(title=title, author=author, call_number=call_number, category=category))
        if db.query(ShelfRange).count() == 0:
            for start, end, floor, aisle, shelf, directions in SAMPLE_RANGES:
                db.add(ShelfRange(
                    call_number_start=start, call_number_end=end,
                    floor=floor, aisle=aisle, shelf=shelf, directions_text=directions,
                ))
        db.commit()
        print(f"Seeded {db.query(Book).count()} books and {db.query(ShelfRange).count()} shelf ranges.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
