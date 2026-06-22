from sentence_transformers import (
    SentenceTransformer
)

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def create_embedding_text(chunk):

    file_name = chunk.get(
        "file",
        ""
    )

    class_name = chunk.get(
        "class_name",
        ""
    )

    name = chunk.get(
        "name",
        ""
    )

    chunk_type = chunk.get(
        "chunk_type",
        ""
    )

    content = chunk.get(
        "content",
        ""
    )

    text = f"""
Repository File:
{file_name}

Class:
{class_name}

Function:
{name}

Type:
{chunk_type}

Keywords:
{file_name}
{name}
{class_name}
{chunk_type}

Source Code:
{content}
"""

    return text


def get_embeddings(texts):

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    return embeddings