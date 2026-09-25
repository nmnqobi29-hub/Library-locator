

import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Library Book Finder", page_icon="📚")

st.title("📚 Library Book Finder")
st.write("Type a book title or author and we'll tell you which shelf to go to.")

query = st.text_input("What book are you looking for?", placeholder="e.g. Clean Code")

if st.button("Find it") or query:
    if not query.strip():
        st.info("Type something to search for.")
    else:
        with st.spinner("Searching the catalog..."):
            try:
                resp = requests.get(f"{API_URL}/find", params={"q": query}, timeout=5)
            except requests.exceptions.ConnectionError:
                st.error(
                    "Can't reach the backend. Make sure it's running: "
                    "`uvicorn main:app --reload`"
                )
                st.stop()

        if resp.status_code == 404:
            st.warning("No books matched that search. Try a different title or author.")
        elif resp.status_code != 200:
            st.error("Something went wrong on the server.")
        else:
            results = resp.json()
            st.success(f"Found {len(results)} result(s).")
            for r in results:
                with st.container(border=True):
                    st.subheader(r["title"])
                    st.caption(f"by {r['author']} — {r['category']} — Call number: {r['call_number']}")
                    loc = r["location"]
                    if loc:
                        st.markdown(f"**📍 {loc['floor']}, {loc['aisle']}, {loc['shelf']}**")
                        st.write(loc["directions"])
                    else:
                        st.warning("Found the book, but no shelf mapping exists for its call number yet.")
