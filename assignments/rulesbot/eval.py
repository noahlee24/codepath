from retriever import retrieve


test_cases = [
    {"query": "How do you set up the board in Catan?", "expected_game": "Catan"},
    {"query": "How does the SpyMaster give clues", "expected_game": "Codenames"},  
    {"query": "How do you win in tic-tac-toe", "expected_game": "Tic Tac Toe"},
    {"query": "What is Wild Card", "expected_game": "Uno"},
]
count = 0
for t in test_cases:
    
    results = retrieve(t["query"])
    correct = any(r["game"] == t["expected_game"] for r in results)
    if correct:
        count+=1
    print (correct)
accuracy = (count / len(test_cases)) * 100   

print("Accuracy score", accuracy)

  