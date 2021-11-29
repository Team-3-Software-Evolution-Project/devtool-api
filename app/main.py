import os
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.git_utils as git_utils


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# git log src/SMCE | wc -l
@app.get("/analyze")
def analyze_repo(command: str, git_url: str):
    repo_path = git_utils.download_repo(git_url)
    repo_file_tree = git_utils.list_files(repo_path)

    output = git_utils.execute_command(repo_path, command)

    return {"result": output.removesuffix('/n').strip(), "file_tree": repo_file_tree}
