
from branch_deployer.models import RepositoryModel
import pytest


def test_github_1():
    settings = {
        'id': 'test',
        'url': 'https://github.com/OpenDataServices/dokku-branch-deployer'
    }
    RepositoryModel(settings)
    # Test is it doesn't crash


def test_gitlab_1():
    settings = {
        'id': 'test',
        'url': 'https://gitlab.com/OpenDataServices/dokku-branch-deployer'
    }
    with pytest.raises(Exception) as error:
        RepositoryModel(settings)
    assert "We only support GitHub.com" == str(error.value)

