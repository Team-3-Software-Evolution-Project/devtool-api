import os
import shutil
from typing import Optional

from git import Repo


def download_repo(git_url: str):
    folder_name = git_url.split('/')[-1].removesuffix('.git')
    download_path = f'./repos/{folder_name}'

    if folder_exists(download_path):
        shutil.rmtree(download_path)
        download_repo(git_url)
        return download_path
    else:
        try:
            Repo.clone_from(git_url, download_path)
            return download_path
        except:
            print(f'Could not download repo: {git_url}')

    return None


def list_files(startpath: str, after: Optional[str] = None, until: Optional[str] = None):
    full_startpath = startpath
    # if folder_exists(startpath+'/src'):
    #     startpath += '/src'
    # elif folder_exists(startpath+'/lib'):
    #     startpath += '/lib'

    tree_string = ''
    commit_values = []
    for root, dirs, files in os.walk(startpath):
        if '.git' not in os.path.relpath(root):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            folder_path = str('/'.join(os.path.relpath(root).split('/')[2:]))
            commits = execute_command(
                full_startpath, f'git log --oneline -- {folder_path} | wc -l', after, until)
            tree_string += f'\n{indent}📂{os.path.basename(root)}/ [{commits}]'
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                full_path = os.path.relpath(root).split('/')[2:]
                path = str('/'.join(full_path)) + f'/{f}'
                # Need this in order to correctly get path to files in root
                if len(path.split('/')[0]) == 0:
                    path = path.removeprefix('/')
                commits = execute_command(
                    full_startpath, f'git log --oneline -- {path} | wc -l', after, until)
                commit_values.append(int(commits))
                tree_string += f'\n{subindent}📜{f} [{commits}]'

    return tree_string.strip('\n'), round(sum(commit_values) / len(commit_values), 2)


def execute_command(root: str, command: str, after: Optional[str] = None, until: Optional[str] = None):
    if until:
        commandArray = command.split(' ')
        commandArray.insert(2, f'--until="{until}"')
        command = ' '.join(commandArray)
    if after:
        commandArray = command.split(' ')
        commandArray.insert(2, f'--after="{after}"')
        command = ' '.join(commandArray)
    pre_cwd = os.getcwd()
    os.chdir(root)
    # Execute command in repo directory
    stream = os.popen(f'{command}')
    output = stream.read()
    # Change CWD back to normal one
    os.chdir(pre_cwd)

    # print(f'root: {root} \ncommand: {command} \noutput: {output}')
    return output.removesuffix('/n').strip()


def folder_exists(path: str):
    return(os.path.isdir(path))
