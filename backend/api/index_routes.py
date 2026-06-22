from fastapi import APIRouter
from pydantic import BaseModel

from backend.utils.repository_utils import (
    get_repo_name
)

from backend.ingestion.github_cloner import (
    clone_repository
)

from backend.ingestion.build_chunks import (
    build_chunks
)

from backend.embeddings.build_index import (
    build_index
)

router = APIRouter()


class RepositoryRequest(BaseModel):
    repo_url: str


@router.post("/index-repository")
def index_repository(
    request: RepositoryRequest
):

    repo_path = clone_repository(
        request.repo_url
    )
    repo_name = get_repo_name(
    request.repo_url
    )

    chunks = build_chunks(
        repo_path
    )

    build_index(
        repo_name
    )

    return {
        "status": "success",
        "repository": request.repo_url,
        "chunks": len(chunks)
    }