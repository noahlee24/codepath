"""
chunk.py - Milestone 3b: Chunking

Splits each document's text into overlapping, fixed-size character chunks.

Design (decided during planning):
  - CHARACTER COUNT is the backbone. A ~1000-char cap guarantees every chunk
    stays under the embedding model's ~256-token ceiling, on EVERY document --
    even the headerless blog (resource_monitor.txt).
  - OVERLAP carries the tail of one chunk into the start of the next, so a
    procedure that gets cut across a boundary isn't severed mid-step.
"""

from ingest import load_documents

# Defaults match the Chunking Strategy in planning.md.
CHUNK_SIZE = 1000   # characters (~250 tokens, just under the 256 ceiling)
OVERLAP = 150       # characters carried over between neighbouring chunks


def chunk_text(text, source, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """
    Split one document's `text` into overlapping chunks.

    Returns a list of dicts:
        [{"source": source, "text": "...up to chunk_size chars..."}, ...]

    How the sliding window works:
        - Take characters [start : start + chunk_size] as a chunk.
        - Move `start` forward by (chunk_size - overlap), so each chunk begins
          a little before the previous one ended -> the overlap.
    """
    chunks = []
    step = chunk_size - overlap   # how far we advance each loop (e.g. 1000-150=850)

    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))   # don't run past the end
        chunk = text[start:end]
        chunks.append({"source": source, "text": chunk})

        # If this chunk reached the end of the document, we're done.
        if end == len(text):
            break

        start += step

    return chunks


def chunk_documents(documents=None):
    """
    Run chunk_text() over every document and flatten into one big list of chunks.
    This is what the embedding stage (Milestone 4) will consume.
    """
    if documents is None:
        documents = load_documents()

    all_chunks = []
    for doc in documents:
        all_chunks.extend(chunk_text(doc["text"], doc["source"]))
    return all_chunks


# Verification step (your three checks from planning.md).
if __name__ == "__main__":
    chunks = chunk_documents()
    print(f"Total chunks: {len(chunks)}\n")

    # CHECK 1: sizes should cluster near 1000, none far over the ceiling.
    sizes = [len(c["text"]) for c in chunks]
    print(f"Chunk sizes -> min {min(sizes)}, max {max(sizes)}, "
          f"avg {sum(sizes) // len(sizes)}")
    over = [s for s in sizes if s > CHUNK_SIZE]
    print(f"Chunks over {CHUNK_SIZE} chars: {len(over)} (should be 0)\n")

    # CHECK 2: overlap worked -> the end of chunk 0 reappears at the start of chunk 1.
    if len(chunks) >= 2:
        tail = chunks[0]["text"][-OVERLAP:]
        head = chunks[1]["text"][:OVERLAP]
        print("Overlap matches:", tail == head)
