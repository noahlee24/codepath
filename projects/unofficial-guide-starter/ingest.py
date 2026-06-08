"""
ingest.py - Milestone 3a: Document Ingestion

Reads every .txt file in the documents/ folder and returns their text,
keeping track of which file each piece of text came from (source attribution).
"""

import os
from config import DOCS_PATH


def load_documents(folder=DOCS_PATH):
    """
    Load all .txt files from `folder` (defaults to DOCS_PATH from config.py).

    Returns a list of dicts, one per file:
        [{"source": "chrome_browser.txt", "text": "...file contents..."}, ...]

    We keep the filename ("source") alongside the text so that later, when the
    bot answers a question, we can tell the user WHICH guide the answer came from.
    """
    documents = []

    # os.listdir gives us every name inside the folder, e.g. "chrome_browser.txt".
    # Note: these are bare names, NOT full paths.
    for filename in os.listdir(folder):

        # Keep only the text files; skip the .png, .gitkeep, etc.
        if not filename.endswith(".txt"):
            continue

        # os.listdir gave us "chrome_browser.txt", but open() needs the folder
        # too. os.path.join builds "./documents/chrome_browser.txt" on any OS.
        path = os.path.join(folder, filename)

        # encoding="utf-8" matters: these docs contain curly quotes, em-dashes,
        # and arrows. Without it, Windows' default encoding can crash or mangle them.
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append({"source": filename, "text": text})

    return documents


# This block only runs when you execute `python ingest.py` directly.
# It's our verification step: prove we found all the files and read them.
if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents:\n")
    for doc in docs:
        print(f"  {doc['source']:45} {len(doc['text']):>6} chars")
