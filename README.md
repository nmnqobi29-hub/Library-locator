# Library Locator MVP

A working demo of the "search a book, get shelf directions" concept —
built on sample data so you can show a real, clickable tool before
asking the library for actual catalog access.

## What's inside

- `models.py` — the two tables: `Book` (sample catalog) and
  `ShelfRange` (call-number range → floor/aisle/shelf)
- `seed.py` — fills the database with 18 sample books across
  Computer Science, Business, Architecture, and Africana & Archives,
  plus 5 shelf ranges
- `main.py` — FastAPI backend (`/search`, `/locate`, `/find`)
- `streamlit_app.py` — the student-facing search screen
- `database.py` — SQLite by default; set `DATABASE_URL` to point at
  Postgres later with no other code changes

## Run it locally

```bash
pip install -r requirements.txt
python seed.py                              # one-time: creates library.db + sample data
uvicorn main:app --reload                   # terminal 1 — backend on :8000
streamlit run streamlit_app.py              # terminal 2 — frontend on :8501
```

Then open the Streamlit URL it prints and search for something like
"Clean Code", "Algorithms", or "Africa".

## What to change before demoing to the library

1. In `seed.py`, replace the sample titles/call numbers and shelf
   ranges with real categories and (rough, even if approximate) floor
   layout from your own library, so the demo feels grounded in the
   actual building rather than generic.
2. Deploy both pieces to Railway so you can hand over a live link
   instead of asking them to run code — set `API_URL` as an
   environment variable on the Streamlit service pointing at the
   deployed FastAPI URL.

## What's deliberately left out (for later, once you have real access)

- QR code scanning — a text search box proves the same point faster
- Real floor-plan/map graphics
- Live catalog integration — this is the piece that gets swapped in
  once the library grants API/export access, replacing the sample
  `books` table with real data
