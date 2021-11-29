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

    pre_cwd = os.getcwd()
    os.chdir(repo_path)
    # Execute command in repo directory
    stream = os.popen(f'{command}')
    output = stream.read()
    # Change CWD back to normal one
    os.chdir(pre_cwd)

    return {"result": output.removesuffix('/n')}
