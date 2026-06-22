from backend.retrieval.retriever import Retriever
from backend.retrieval.reranker import Reranker

from backend.llm.generator import Generator


class QueryExpander:

    def expand(self, query):

        return f"""
Repository source code question:

{query}

Related repository keywords:

oauth
oauth2
authentication
authorization
security
scope
scopes
bearer
token
api key
openid
credentials

Find implementation details, classes,
methods, functions, files and source code.
"""


class RepoRAG:

    def __init__(
        self,
        repo_name
    ):

        self.repo_name = repo_name

        self.retriever = Retriever(
            repo_name
        )

        self.reranker = Reranker()

        self.generator = Generator()

        self.query_expander = QueryExpander()

    def build_context(
        self,
        chunks
    ):

        context_parts = []

        for chunk in chunks:

            file_name = chunk.get(
                "file",
                "Unknown"
            )

            name = chunk.get(
                "name",
                "Unknown"
            )

            chunk_type = chunk.get(
                "chunk_type",
                "Unknown"
            )

            class_name = chunk.get(
                "class_name",
                ""
            )

            content = chunk.get(
                "content",
                ""
            )

            context_parts.append(
                f"""
REPOSITORY FILE:
{file_name}

TYPE:
{chunk_type}

CLASS:
{class_name}

NAME:
{name}

CODE:
{content}
"""
            )

        return "\n\n".join(
            context_parts
        )

    def ask(
        self,
        question,
        top_k=5
    ):

        expanded_query = (
            self.query_expander.expand(
                question
            )
        )

        retrieved_chunks = (
            self.retriever.search(
                expanded_query,
                top_k=30
            )
        )

        print("\n" + "=" * 100)
        print("TOP VECTOR RESULTS")
        print("=" * 100)

        for chunk in retrieved_chunks[:20]:

            print(
                f"{chunk['score']:.4f}"
                f" | {chunk['file']}"
                f" | {chunk['name']}"
            )

        reranked_chunks = (
            self.reranker.rerank(
                expanded_query,
                retrieved_chunks,
                top_k=top_k
            )
        )

        print("\n" + "=" * 100)
        print("TOP RETRIEVED CHUNKS")
        print("=" * 100)

        for chunk in reranked_chunks:

            print(
                f"{chunk['file']} | "
                f"{chunk['chunk_type']} | "
                f"{chunk['name']}"
            )

        print("=" * 100)

        context = self.build_context(
            reranked_chunks
        )

        prompt = f"""
You are GitGPT.

You are NOT a general AI assistant.

You MUST answer ONLY using the repository context.

IMPORTANT:

- Do NOT explain concepts from your training data.
- Do NOT use outside knowledge.
- If the repository does not contain the answer, say:
- Use ONLY the repository context.
- Do NOT use outside knowledge.
- Do NOT invent files, classes, methods, APIs, or behavior.
- Every statement must be supported by repository context.
- Mention filenames whenever possible.
- Mention class names and method names.
- If the answer is not present in the repository, respond exactly:


"I could not find enough information in the repository."

- Every claim must come from the repository context.
- Mention file names.
- Mention method names.
- Mention class names.
- Quote behavior from code.

REPOSITORY:
{self.repo_name}

QUESTION:
{question}

CONTEXT:
{context}

TASK:

Extract facts from the repository context only.

ANSWER:
REPOSITORY FACTS:

1. Mention the relevant files.
2. Mention relevant methods/classes.
3. Explain only what exists in the repository.
4. If missing, say:
"I could not find enough information in the repository."

FINAL ANSWER:
"""

        answer = self.generator.generate(
            prompt,
            max_new_tokens=250
        )

        return {
            "repository": self.repo_name,
            "question": question,
            "answer": answer,
            "sources": reranked_chunks
        }