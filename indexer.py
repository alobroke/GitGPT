from dataclasses import dataclass
from pathlib import Path

import faiss
import numpy as np

from sentence_transformers import (
    SentenceTransformer,
    CrossEncoder
)


@dataclass
class Chunk:
    file_path: str
    start_line: int
    end_line: int
    text: str


class RepositoryIndex:

    def __init__(
        self,
        chunks,
        embeddings
    ):
        self.chunks = chunks
        self.embeddings = embeddings

        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dim
        )

        self.index.add(
            embeddings
        )

        self.embedder = (
            SentenceTransformer(
                "BAAI/bge-small-en-v1.5"
            )
        )

    def search(
        self,
        query,
        top_k=10
    ):

        q = self.embedder.encode(
            [query],
            normalize_embeddings=True
        )

        q = np.array(
            q,
            dtype=np.float32
        )

        scores, ids = self.index.search(
            q,
            top_k
        )

        results = []

        for score, idx in zip(
            scores[0],
            ids[0]
        ):

            if idx < 0:
                continue

            results.append(
                (
                    self.chunks[idx],
                    float(score)
                )
            )

        return results


class Reranker:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query,
        chunks,
        top_n=5
    ):

        pairs = []

        for chunk, score in chunks:

            pairs.append(
                (
                    query,
                    chunk.text
                )
            )

        scores = self.model.predict(
            pairs
        )

        ranked = []

        for item, score in zip(
            chunks,
            scores
        ):

            ranked.append(
                (
                    item[0],
                    float(score)
                )
            )

        ranked.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_n]


def chunk_repository(
    repo_root,
    patterns
):

    chunks = []

    for pattern in patterns:

        for file in Path(
            repo_root
        ).rglob(
            pattern.replace("**/", "")
        ):

            if not file.is_file():
                continue

            try:

                text = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

            except Exception:
                continue

            lines = text.splitlines()

            step = 80

            for i in range(
                0,
                len(lines),
                step
            ):

                chunk_text = "\n".join(
                    lines[i:i+step]
                )

                chunks.append(
                    Chunk(
                        file_path=str(file),
                        start_line=i + 1,
                        end_line=min(
                            i + step,
                            len(lines)
                        ),
                        text=chunk_text
                    )
                )

    return chunks


def get_or_build_index(
    repo_root,
    embedding_model,
    patterns,
    use_cache=True
):

    chunks = chunk_repository(
        repo_root,
        patterns
    )

    embedder = (
        SentenceTransformer(
            embedding_model
        )
    )

    embeddings = embedder.encode(
        [c.text for c in chunks],
        normalize_embeddings=True,
        show_progress_bar=True
    )

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    return RepositoryIndex(
        chunks,
        embeddings
    )