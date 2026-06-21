import os
import json

from backend.ingestion.chunker import (
    chunk_python_file
)

OUTPUT_DIR = "data/generated"

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "chunks.json"
)


def build_repository_chunks(repo_path):

    all_chunks = []

    ignored_dirs = {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "tests",
        "node_modules"
    }

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            d for d in dirs
            if d not in ignored_dirs
        ]

        for file in files:

            if not file.endswith(".py"):
                continue

            file_path = os.path.join(root, file)

            # extra safety
            if "tests" in file_path.lower():
                continue

            chunks = chunk_python_file(
                file_path
            )

            all_chunks.extend(chunks)

    return all_chunks


def save_chunks(chunks):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Chunks saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":

    repo_path = "data/repos/fastapi"

    print("Building chunks...")

    chunks = build_repository_chunks(
        repo_path
    )

    print(
        f"Total Chunks: {len(chunks)}"
    )

    save_chunks(chunks)