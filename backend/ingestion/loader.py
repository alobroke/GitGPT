import os

def load_repository(repo_path):

    documents = []

    allowed_extensions = [
        ".py",
        ".md",
        ".txt"
    ]

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            if any(file.endswith(ext)
                   for ext in allowed_extensions):

                path = os.path.join(root, file)

                try:

                    with open(
                        path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        text = f.read()

                        documents.append({
                            "file": path,
                            "content": text
                        })

                except:
                    pass

    return documents

docs = load_repository(
    "data/repos/fastapi"
)

print(len(docs))