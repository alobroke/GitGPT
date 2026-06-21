from backend.retrieval.retriever import Retriever
from backend.retrieval.reranker import Reranker

from backend.llm.generator import Generator
from backend.llm.prompt import SYSTEM_PROMPT


class QueryExpander:

    def expand(self, query):

        return f"""
Repository code question:

{query}

Relevant functions, classes, implementation details,
source code, methods, dependencies, behavior.
"""


class RepoRAG:

    def __init__(self):

        self.retriever = Retriever()

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

            start_line = chunk.get(
                "start_line",
                ""
            )

            end_line = chunk.get(
                "end_line",
                ""
            )

            content = chunk.get(
                "content",
                ""
            )

            context_parts.append(
                f"""
FILE: {file_name}

TYPE: {chunk_type}

CLASS: {class_name}

NAME: {name}

LINES: {start_line}-{end_line}

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

        # Step 1: Expand Query
        expanded_query = self.query_expander.expand(
            question
        )

        # Step 2: Retrieve
        retrieved_chunks = self.retriever.search(
            expanded_query,
            top_k=20
        )

        # Step 3: Rerank
        reranked_chunks = self.reranker.rerank(
            expanded_query,
            retrieved_chunks,
            top_k=top_k
        )

        # Step 4: Build Context
        context = self.build_context(
            reranked_chunks
        )

        # Step 5: Build Prompt
        prompt = f"""
{SYSTEM_PROMPT}

QUESTION:
{question}

REPOSITORY CONTEXT:
{context}

ANSWER:
"""

        # Step 6: Generate Answer
        answer = self.generator.generate(
            prompt
        )

        return {
            "question": question,
            "answer": answer,
            "sources": reranked_chunks
        }