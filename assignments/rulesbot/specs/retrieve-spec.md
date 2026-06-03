# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

```
we use _collection.query to search through the created list. I pass through query and wrap it as a list, n_results is a default output of results. documents is the the chunck, metadatas is the name of the game, and distances is what is run in the background
```

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```
"text": d, each field comes from the include parameter. same goes for  "game": metadatas[i]["game"], "distance": distances[i]
```

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

```
you need index [0]. it wants to be able to search between multiple querues
```

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

```
For  return all n_results trade off is that it will always return something regarless of its relency. The  filter out might nake the parameters to small and information becomes not usables
```

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

```
(a)Line 68 returns an empty list if the collection is empty. (b)if it matches no chunks well it will still produce all the chuncks that are closest, and for (c) If a user asks about chess and there is Chess and Srabble in the database, it will return the one that is semantically closest. Its a problem because it may reutrn the one that is the closest semanticalyl but can still be for  the wrong game
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query:"How do you set up the board in Catan?"
Top result game: Catan
Distance score: 0.3798601031303406
Does it make sense? Yes
```

**One thing about the query results that surprised you:**

```
[your answer here]
```
