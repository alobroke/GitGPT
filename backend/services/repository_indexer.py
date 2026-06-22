from backend.ingestion.github_cloner import clone_repository
from backend.ingestion.build_chunks import build_chunks
from backend.embeddings.build_index import build_index


class RepositoryIndexer:

    def index_repository(
        self,
        repo_url: str
    ):

        print("Cloning repository...")

        repo_path = clone_repository(
            repo_url
        )

        print("Building chunks...")

        build_chunks(
            repo_path
        )

        print("Building FAISS index...")

        build_index()

        return {
            "status": "success",
            "repository": repo_url
        }