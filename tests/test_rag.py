from backend.rag.pipeline import RepoRAG

rag = RepoRAG()

result = rag.ask(
    "What does make_not_authenticated_error do?"
)

print("\n")
print("=" * 100)
print("ANSWER")
print("=" * 100)

print(result["answer"])

print("\n")
print("=" * 100)
print("SOURCES")
print("=" * 100)

for source in result["sources"]:

    print(
        f"""
File: {source['file']}
Type: {source['chunk_type']}
Name: {source['name']}
Rerank Score: {source.get('rerank_score', 0)}
"""
    )