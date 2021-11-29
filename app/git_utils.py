import os

from git import Repo


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


# Copied from https://stackoverflow.com/a/9728478
def list_files(startpath):
    if folder_exists(startpath+'/src'):
        startpath += '/src'
    elif folder_exists(startpath+'/lib'):
        startpath += '/lib'

    tree_string = ''
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree_string += '\n' + ('{}📂{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            tree_string += '\n' + ('{}📜{}'.format(subindent, f))

    return tree_string.strip('\n')


def folder_exists(path: str):
    return(os.path.isdir(path))
