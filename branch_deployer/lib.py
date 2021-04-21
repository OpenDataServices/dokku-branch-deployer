from sh import pushd, ssh, ErrorReturnCode
from sh.contrib import git
import os
from branch_deployer import settings

SSH_CONNECT_STRING = f'{settings.SSH_DOKKU_USER}@{settings.SSH_DOKKU_HOST}'
dokku = ssh.bake('-tp', settings.SSH_DOKKU_PORT, SSH_CONNECT_STRING, '--')

def update_repo(repository):
    if not os.path.exists(repository.local_git_directory):
        os.makedirs(repository.local_git_directory)
        with pushd(repository.local_git_directory):
            git.clone(repository.clone_url, '.', bare=True)
    else:
        with pushd(repository.local_git_directory):
            git.fetch('origin')

def get_all_branches_in_repo(repository):
    branches = []
    with pushd(repository.local_git_directory):
        for branch in git.branch():
            branch = branch[2:].strip()
            if branch:
                branches.append(branch)
    return branches


def app_create(repository, branch_name):
    try:
        dokku('apps:create', repository.app_name_for_branch(branch_name))
    except ErrorReturnCode as e:
        #print(str(e))
        # app already exists
        # TODO can we not do better than this?
        pass

