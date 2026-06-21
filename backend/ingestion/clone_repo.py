from git import Repo
import os

def clone_repository(repo_url, save_path):
    
    if os.path.exists(save_path):
        print("Repository already exists")
        return

    Repo.clone_from(repo_url, save_path)

    print("Repository cloned successfully")
