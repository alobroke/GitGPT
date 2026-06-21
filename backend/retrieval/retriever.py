import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


class Retriever:

    def __init__(self):

        self.embedding_model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

        self.index = faiss.read_index(
            "data/generated/faiss_index.bin"
        )

        with open(
            "data/generated/metadata.json",
            "r",
            encoding="utf-8"
        ) as f:

            self.metadata = json.load(f)

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
        top_k=5
    ):

        query_embedding = self.embed_query(
            query
        )

        distances, indices = self.index.search(
            query_embedding,
            top_k * 4
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

        return results[:top_k]