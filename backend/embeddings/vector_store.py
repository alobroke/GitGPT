import json
import os

import faiss
import numpy as np

from backend.embeddings.embedder import (
    create_embedding_text,
    get_embeddings
)

from backend.utils.repository_utils import (
    get_repo_index_dir
)


CHUNKS_PATH = "data/generated/chunks.json"


def build_faiss_index(
    repo_name
):

    print("Loading chunks...")

    with open(
        CHUNKS_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)

    print(
        f"Loaded {len(chunks)} chunks"
    )

    texts = []

    for chunk in chunks:

        texts.append(
            create_embedding_text(
                chunk
            )
        )

    print(
        "Generating embeddings..."
    )

    embeddings = get_embeddings(
        texts
    )

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

    index.add(
        embeddings
    )

    index_dir = get_repo_index_dir(
        repo_name
    )

    os.makedirs(
        index_dir,
        exist_ok=True
    )

    index_path = os.path.join(
        index_dir,
        "faiss_index.bin"
    )

    metadata_path = os.path.join(
        index_dir,
        "metadata.json"
    )

    faiss.write_index(
        index,
        index_path
    )

    metadata = []

    for chunk in chunks:

        metadata.append(
            {
                "id": chunk["id"],
                "file": chunk["file"],
                "chunk_type": chunk["chunk_type"],
                "name": chunk["name"],
                "class_name": chunk.get(
                    "class_name",
                    ""
                ),
                "content": chunk["content"]
            }
        )

    with open(
        metadata_path,
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
        f"FAISS Index Saved → {index_path}"
    )

    print(
        f"Metadata Saved → {metadata_path}"
    )

    print(
        f"Indexed {len(metadata)} chunks"
    )