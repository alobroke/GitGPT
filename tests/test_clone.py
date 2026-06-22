from backend.ingestion.github_cloner import (
    clone_repository
)

repo = clone_repository(
    "https://github.com/tiangolo/fastapi"
)

print(repo)