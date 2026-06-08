"""
retrieve.py - Milestone 4b: Retrieval

Given a user question, find the top-k most similar chunks in ChromaDB.

CRITICAL: the question must be embedded with the SAME model used to embed the
chunks (all-MiniLM-L6-v2). Comparing vectors from two different models is
meaningless -- it's like measuring distance with two different rulers.
"""

import chromadb
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL, CHROMA_COLLECTION, CHROMA_PATH, N_RESULTS

# Load the model and open the existing collection once, when this module is imported.
_model = SentenceTransformer(EMBEDDING_MODEL)
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_collection(CHROMA_COLLECTION)


def retrieve(question, k=N_RESULTS):
    """
    Return the top-k chunks most similar to `question`.

    Each result is a dict: {"text": ..., "source": ..., "distance": ...}
    (smaller distance = more similar).
    """
    # Embed the question the same way we embedded the chunks.
    query_embedding = _model.encode([question]).tolist()

    # ChromaDB ranks every stored chunk by closeness and returns the nearest k.
    results = _collection.query(query_embeddings=query_embedding, n_results=k)

    # Chroma nests results one level per query; we only sent one query, so index [0].
    hits = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        hits.append({"text": text, "source": meta["source"], "distance": dist})
    return hits


# Verification: the "right chunk came back" check from planning.md.
if __name__ == "__main__":
    question = "Nobody can hear me on zoom call."
    print(f"Q: {question}\n")
    for i, hit in enumerate(retrieve(question), start=1):
        preview = hit["text"][:160].replace("\n", " ")
        print(f"{i}. [{hit['source']}]  (distance {hit['distance']:.3f})")
        print(f"   {preview}...\n")
