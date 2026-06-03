# RulesBot — Planning Doc

Use this file to record your design decisions as you work through the lab.
There are no wrong answers — write enough that you could explain your reasoning to another group.

---

## Chunking Strategy

**Chunk size:**  300


**Overlap:** 50


**Why this strategy fits rule book text:**
I tested retrieval with 100 characters. Some of the information was out of context. As for 300 to 512 there wasn;t that much of a difference whne it came to the context.

---

## Retrieval Observations

After implementing retrieval, try these test queries and record what comes back:

| Query | Top result game | Does it make sense? |
|-------|----------------|---------------------|
| "How do you win?" |Risk | Kinda, it gives a way to win with little context |
| "What happens when you roll a 7?" |Catan| It slightly makes sense. Missing a bit of context but general question was answered. |
| "Can two players share a route?" |Ticket To Ride | Easy question with an easy answer. Pretty much a yes or no. |

**Anything surprising?**
The precision is pretty high, like a 50% on precision when asking questions that arent seemling yes or no.

---

## Response Quality

After implementing generation, try 2–3 questions and assess the answers:

| Query | Answer accurate? | Properly grounded? | Cited the right game? |
|-------|-----------------|-------------------|----------------------|
| | | | |
| | | | |

**What would you change about the prompt to improve grounding?**

