from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def create_embedding_text(chunk):

    text = f"""
File: {chunk.get('file', '')}

Class: {chunk.get('class_name', '')}

Name: {chunk.get('name', '')}

Type: {chunk.get('chunk_type', '')}

Code:

{chunk.get('content', '')}
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