import os
from urllib.parse import urlparse


def get_repo_name(repo_url):

    path = urlparse(repo_url).path

    repo_name = path.split("/")[-1]

    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    return repo_name


def get_repo_index_dir(repo_name):

    return os.path.join(
        "data",
        "indexes",
        repo_name
    )