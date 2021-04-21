from sh import pushd, ssh
from sh.contrib import git
import os

def update_repo(repository):
    if not os.path.exists(repository.local_git_directory):
        os.makedirs(repository.local_git_directory)
        with pushd(repository.local_git_directory):
            git.clone(repository.clone_url, '.', bare=True)
    else:
        with pushd(repository.local_git_directory):
            git.fetch('origin')
