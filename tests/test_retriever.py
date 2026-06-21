from backend.retrieval.retriever import Retriever

retriever = Retriever()

results = retriever.search(
    "How does OAuth authentication work?",
    top_k=10
)

for i, result in enumerate(results, 1):

    print("\n" + "=" * 80)

    print(f"Result {i}")

    print("Score:", result["score"])

    print("Type:", result["chunk_type"])

    print("Name:", result["name"])

    print("File:", result["file"])

    print(
        result["content"][:300]
    )