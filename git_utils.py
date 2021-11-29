import os

from git import Repo

# https://github.com/Team-3-Software-Evolution-Project/smce-gd.git
def download_repo(git_url: str):
    folder_name = git_url.split('/')[-1].removesuffix('.git')
    download_path = f'./repos/{folder_name}'

    if folder_exists(download_path):
        return download_path
    else:
        try:
            Repo.clone_from(git_url, download_path)
            return download_path
        except:
            print(f'Could not download repo: {git_url}')

    return None

def folder_exists(path: str):
    return(os.path.isdir(path))