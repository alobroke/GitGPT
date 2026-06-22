import os
import subprocess


REPOS_DIR = "data/repos"


def clone_repository(repo_url: str):

    repo_name = repo_url.rstrip("/").split("/")[-1]

    repo_path = os.path.join(
        REPOS_DIR,
        repo_name
    )

    os.makedirs(
        REPOS_DIR,
        exist_ok=True
    )

    if os.path.exists(repo_path):

        print(f"Repository already exists: {repo_path}")

        return repo_path

    print("Cloning repository...")

    subprocess.run(
        [
            "git",
            "clone",
            repo_url,
            repo_path
        ],
        check=True
    )

    print("Clone completed")

    return repo_path