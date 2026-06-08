"""
embed_store.py - Milestone 4a: Embedding + Vector Store

Turns every chunk into a vector (embedding) with all-MiniLM-L6-v2 and stores
it in a ChromaDB collection so we can search by meaning later.

Run this ONCE to build the database:  python embed_store.py
(Re-running rebuilds it from scratch.)
"""

import chromadb
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL, CHROMA_COLLECTION, CHROMA_PATH
from chunk import chunk_documents


def build_store():
    # 1. Get all chunks (ingest -> chunk, end to end).
    chunks = chunk_documents()
    print(f"Embedding {len(chunks)} chunks with {EMBEDDING_MODEL} ...")

    # 2. Load the embedding model. First run downloads it (~80MB); then it's cached.
    model = SentenceTransformer(EMBEDDING_MODEL)

    texts = [c["text"] for c in chunks]
    # encode() returns one vector per chunk. tolist() converts numpy -> plain lists
    # because that's what ChromaDB wants.
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    # 3. Connect to a persistent ChromaDB (saved to disk at CHROMA_PATH).
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Rebuild cleanly: drop the old collection if it exists, then recreate.
    # (Otherwise re-running would collide on duplicate IDs.)
    try:
        client.delete_collection(CHROMA_COLLECTION)
    except Exception:
        pass
    collection = client.create_collection(CHROMA_COLLECTION)

    # 4. Add everything. Each chunk needs a unique id; we keep its source filename
    #    as metadata so retrieval can tell us which guide it came from.
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"source": c["source"]} for c in chunks],
    )

    print(f"Stored {collection.count()} chunks in collection '{CHROMA_COLLECTION}'.")
    return collection


# Verification: the collection count should equal the number of chunks.
if __name__ == "__main__":
    build_store()
