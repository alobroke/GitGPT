from backend.embeddings.vector_store import (
    build_faiss_index
)


def build_index(
    repo_name
):

    build_faiss_index(
        repo_name
    )


if __name__ == "__main__":

    build_index(
        "fastapi"
    )