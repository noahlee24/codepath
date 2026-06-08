"""
generate.py - Milestone 5a: Generation

Ties retrieval to the LLM. Takes a user question, retrieves the top-k chunks,
and asks Groq to answer USING ONLY those chunks (so it can't make things up).
"""

from groq import Groq

from config import GROQ_API_KEY, LLM_MODEL, N_RESULTS
from retrieve import retrieve

client = Groq(api_key=GROQ_API_KEY)

# The system prompt is the guardrail. It forces the model to stay grounded in the
# retrieved context and to admit when the answer isn't there -- this is what stops
# hallucination (the risk you named in Anticipated Challenges).
SYSTEM_PROMPT = (
    "You are a helpful PC-troubleshooting assistant. Answer the user's question "
    "USING ONLY the provided context from official guides. If the context does not "
    "contain the answer, say you don't know rather than guessing. Keep answers "
    "concise and step-by-step, and cite the source file(s) you used."
)


def generate_answer(question, k=N_RESULTS):
    """Retrieve context, ask the LLM, return (answer_text, retrieved_hits)."""
    hits = retrieve(question, k)

    # Stitch the retrieved chunks into one context block, labelled by source.
    context = "\n\n".join(
        f"[Source: {h['source']}]\n{h['text']}" for h in hits
    )

    user_message = f"Context:\n{context}\n\nQuestion: {question}"

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,   # low = stick close to the facts, less creative drift
    )
    answer = response.choices[0].message.content
    return answer, hits


# Verification: run all 5 of your Evaluation Plan questions end-to-end.
if __name__ == "__main__":
    eval_questions = [
        "My pc is running slow",
        "Nobody can hear me on zoom call.",
        "Chrome is taking a long time to load",
        "what should i name my folder",
        "How do I find a file",
    ]
    for q in eval_questions:
        answer, hits = generate_answer(q)
        sources = ", ".join(sorted({h["source"] for h in hits}))
        print(f"Q: {q}")
        print(f"A: {answer}")
        print(f"(sources: {sources})\n{'=' * 72}")
