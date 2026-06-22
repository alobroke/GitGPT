import json
import os

import faiss
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

from backend.utils.repository_utils import (
    get_repo_index_dir
)


class Retriever:

    def __init__(
        self,
        repo_name
    ):

        print(
            f"Loading repository: {repo_name}"
        )

        self.embedding_model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

        index_dir = get_repo_index_dir(
            repo_name
        )

        index_path = os.path.join(
            index_dir,
            "faiss_index.bin"
        )

        metadata_path = os.path.join(
            index_dir,
            "metadata.json"
        )

        self.index = faiss.read_index(
            index_path
        )

        with open(
            metadata_path,
            "r",
            encoding="utf-8"
        ) as f:

            self.metadata = json.load(f)

        print(
            f"Loaded {len(self.metadata)} chunks"
        )

    def embed_query(
        self,
        query
    ):

        embedding = self.embedding_model.encode(
            [query],
            normalize_embeddings=True
        )

        return np.array(
            embedding,
            dtype=np.float32
        )

    def deduplicate(
        self,
        results
    ):

        seen = set()

        unique_results = []

        for item in results:

            key = (
                item["file"],
                item["name"]
            )

            if key in seen:
                continue

            seen.add(key)

            unique_results.append(item)

        return unique_results

    def search(
        self,
        query,
        top_k=30
    ):

        query_embedding = self.embed_query(
            query
        )

        distances, indices = self.index.search(
            query_embedding,
            top_k * 5
        )

        results = []

        for score, idx in zip(
            distances[0],
            indices[0]
        ):

            if idx < 0:
                continue

            chunk = self.metadata[idx].copy()

            chunk["score"] = float(score)

            results.append(chunk)

        results = self.deduplicate(
            results
        )

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results[:top_k]