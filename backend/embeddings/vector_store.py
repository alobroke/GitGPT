import json
import os

import faiss
import numpy as np

from backend.embeddings.embedder import (
    create_embedding_text,
    get_embeddings
)


CHUNKS_PATH = "data/generated/chunks.json"

INDEX_PATH = "data/generated/faiss_index.bin"

METADATA_PATH = "data/generated/metadata.json"


def build_faiss_index():

    print("Loading chunks...")

    with open(
        CHUNKS_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)

    print(f"Loaded {len(chunks)} chunks")

    texts = [
        create_embedding_text(chunk)
        for chunk in chunks
    ]

    print("Generating embeddings...")

    embeddings = get_embeddings(texts)

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    print(
        f"Embeddings Shape: {embeddings.shape}"
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(embeddings)

    os.makedirs(
        "data/generated",
        exist_ok=True
    )

    faiss.write_index(
        index,
        INDEX_PATH
    )

    metadata = []

    for chunk in chunks:

        metadata.append({
            "id": chunk["id"],
            "file": chunk["file"],
            "chunk_type": chunk["chunk_type"],
            "name": chunk["name"],
            "class_name": chunk.get(
                "class_name",
                ""
            ),
            "content": chunk["content"]
        })

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"FAISS Index Saved → {INDEX_PATH}"
    )

    print(
        f"Metadata Saved → {METADATA_PATH}"
    )

    print(
        f"Indexed {len(metadata)} chunks"
    )