from dataclasses import dataclass
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


IGNORED_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".vscode",
    "venv",
    ".venv",
    "node_modules",
    "dist",
    "build",
    "data",
    ".cache"
}


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
        embeddings,
        embedding_model
    ):

        self.chunks = chunks

        self.embedder = SentenceTransformer(
            embedding_model,
            cache_folder=".cache/models"
        )

        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dim)

        self.index.add(embeddings)

    def search(
        self,
        query,
        top_k=10
    ):

        query_embedding = self.embedder.encode(
            [query],
            normalize_embeddings=True
        )

        query_embedding = np.array(
            query_embedding,
            dtype=np.float32
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0]
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
        pass

    def rerank(
        self,
        query,
        candidates,
        top_n=5
    ):

        if not candidates:
            return []

        return candidates[:top_n]

def should_skip(
    path
):

    path_parts = set(
        Path(path).parts
    )

    return bool(
        path_parts.intersection(
            IGNORED_DIRS
        )
    )


def chunk_repository(
    repo_root,
    patterns
):

    chunks = []

    repo_root = Path(
        repo_root
    )

    for pattern in patterns:

        clean_pattern = (
            pattern
            .replace("**/", "")
            .replace("*", "")
        )

        if not clean_pattern.startswith("."):
            clean_pattern = (
                "." + clean_pattern
            )

        for file in repo_root.rglob("*"):

            if not file.is_file():
                continue

            if should_skip(file):
                continue

            if file.suffix != clean_pattern:
                continue

            try:

                text = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

            except Exception:
                continue

            lines = text.splitlines()

            chunk_size = 80
            overlap = 20

            start = 0

            while start < len(lines):

                end = min(
                    start + chunk_size,
                    len(lines)
                )

                chunk_text = "\n".join(
                    lines[start:end]
                )

                if chunk_text.strip():

                    chunks.append(
                        Chunk(
                            file_path=str(file),
                            start_line=start + 1,
                            end_line=end,
                            text=chunk_text
                        )
                    )

                start += (
                    chunk_size - overlap
                )

    print(
        f"Total chunks created: {len(chunks)}"
    )

    return chunks


def get_or_build_index(
    repo_root,
    embedding_model,
    patterns,
    use_cache=True
):

    print(
        "Building chunks..."
    )

    chunks = chunk_repository(
        repo_root,
        patterns
    )

    print(
        "Loading embedding model..."
    )

    embedder = SentenceTransformer(
        embedding_model,
        cache_folder=".cache/models"
    )

    print(
        "Generating embeddings..."
    )

    embeddings = embedder.encode(
        [chunk.text for chunk in chunks],
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    print(
        f"Embeddings shape: {embeddings.shape}"
    )

    return RepositoryIndex(
        chunks,
        embeddings,
        embedding_model
    )