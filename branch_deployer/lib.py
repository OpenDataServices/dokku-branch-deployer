from sh import pushd, ssh, ErrorReturnCode
from sh.contrib import git
import os
from branch_deployer import settings
from datetime import datetime
from textwrap import dedent

SSH_CONNECT_STRING = f'{settings.SSH_DOKKU_USER}@{settings.SSH_DOKKU_HOST}'
dokku = ssh.bake('-tp', settings.SSH_DOKKU_PORT, SSH_CONNECT_STRING, '--')

def update_repo(repository):
    if not os.path.exists(repository.local_git_directory):
        os.makedirs(repository.local_git_directory)
        with pushd(repository.local_git_directory):
            git.clone(repository.clone_url, '.', mirror=True)
    else:
        with pushd(repository.local_git_directory):
            git.remote('update')
            git.fetch('--prune')

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


def apps_destroy(repository, branch_name):
    dokku('apps:destroy', repository.app_name_for_branch(branch_name), force=True)


def push_repo(repository, branch_name):
    app_name = repository.app_name_for_branch(branch_name)
    dokku_host = f'{SSH_CONNECT_STRING}:{settings.SSH_DOKKU_PORT}'
    if not settings.DEPLOY_LOGS_BASE_PATH.exists():
        settings.DEPLOY_LOGS_BASE_PATH.mkdir()

    deploy_log_file = settings.DEPLOY_LOGS_BASE_PATH / f'{repository.id}.txt'
    with deploy_log_file.open('wb') as dlfo:
        dlfo.write(dedent(f"""\
            =====================================================
            Deployment:  {datetime.utcnow().isoformat()}
            Repository:  {repository.url}
            Branch name: {branch_name}
            App name:    {app_name}
            =====================================================
        """).encode('utf-8'))
        with pushd(repository.local_git_directory):
            git.push('--force',
                     f'ssh://{dokku_host}/{app_name}',
                     f'{branch_name}:refs/heads/master',
                     _err_to_out=True,
                     _out=dlfo)



def get_branch_name(ref):
    """
    Take a full git ref name and return a more simple branch name.
    e.g. `refs/heads/demo/dude` -> `demo/dude`

    :param ref: the git head ref sent by GitHub
    :return: str the simple branch name
    """
    refs_prefix = 'refs/heads/'
    if ref.startswith(refs_prefix):
        # ref is in the form "refs/heads/master"
        ref = ref[len(refs_prefix):]

    return ref