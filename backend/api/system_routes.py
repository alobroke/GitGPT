import os

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():

    indexes_dir = os.path.join(
        "data",
        "indexes"
    )

    repositories = []

    if os.path.exists(indexes_dir):

        repositories = [
            repo
            for repo in os.listdir(indexes_dir)
            if os.path.isdir(
                os.path.join(
                    indexes_dir,
                    repo
                )
            )
        ]

    return {
        "status": "healthy",
        "repositories": len(repositories),
        "repository_names": repositories
    }


@router.get("/repositories")
def repositories():

    indexes_dir = os.path.join(
        "data",
        "indexes"
    )

    if not os.path.exists(
        indexes_dir
    ):

        return {
            "repositories": []
        }

    repos = [
        repo
        for repo in os.listdir(
            indexes_dir
        )
        if os.path.isdir(
            os.path.join(
                indexes_dir,
                repo
            )
        )
    ]

    return {
        "repositories": repos
    }