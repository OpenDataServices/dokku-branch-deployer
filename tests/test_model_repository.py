
from branch_deployer.models import RepositoryModel
import pytest


def test_github_clone_url_http_1():
    settings = {
        'id': 'test',
        'url': 'https://github.com/OpenDataServices/dokku-branch-deployer'
    }
    repo = RepositoryModel(settings)
    assert 'https://github.com/OpenDataServices/dokku-branch-deployer.git'\
           == repo.clone_url()


def test_github_clone_url_ssh_1():
    settings = {
        'id': 'test',
        'url': 'https://github.com/OpenDataServices/dokku-branch-deployer',
        'get_repository_by_ssh': True
    }
    repo = RepositoryModel(settings)
    assert 'git@github.com:OpenDataServices/dokku-branch-deployer.git'\
           == repo.clone_url()


def test_gitlab_1():
    settings = {
        'id': 'test',
        'url': 'https://gitlab.com/OpenDataServices/dokku-branch-deployer'
    }
    with pytest.raises(Exception) as error:
        RepositoryModel(settings)
    assert "We only support GitHub.com" == str(error.value)
