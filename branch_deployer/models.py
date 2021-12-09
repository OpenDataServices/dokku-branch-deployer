
from branch_deployer import settings
import os
from slugify import slugify


class RepositoryModel:
    def __init__(self, settings_data):
        url_bits = settings_data['url'].split('/')
        if url_bits[2] != 'github.com':
            raise Exception('We only support GitHub.com')
        self.url = settings_data['url']
        self.id = settings_data['id']
        self.local_git_directory = \
            os.path.join(settings.REPOS_BASE_PATH, "github",
                         url_bits[3], url_bits[4])
        self.branches = settings_data.get('branches', [])
        self.all_branches = settings_data.get('all_branches', False)
        self.app_name_format = \
            settings_data.get('app_name_format', '{repo_name}-{branch_name}')
        self.setup_dokku_commands = \
            settings_data.get('setup_dokku_commands', [])
        self.teardown_dokku_commands = \
            settings_data.get('teardown_dokku_commands', [])
        self.get_repository_by_ssh = \
            settings_data.get('get_repository_by_ssh', False)

    def clone_url(self):
        if self.get_repository_by_ssh:
            url_bits = self.url.split('/')
            return 'git@github.com:' + url_bits[3] + '/' + url_bits[4] + '.git'
        else:
            return self.url + ".git"

    def should_deploy_branch(self, branch_name):
        if self.all_branches:
            return True
        if branch_name in self.branches:
            return True
        return False

    def app_name_for_branch(self, branch_name):
        url_bits = self.url.split('/')
        app_name = self.app_name_format.format(
            repo_owner=url_bits[3],
            repo_name=url_bits[4],
            branch_name=branch_name,
        )
        return slugify(app_name)

    def matches_github_webhook_data(self, data):
        url_bits = self.url.split('/')
        return url_bits[3] == \
            data.get('repository', {}).get('owner', {}).get('login') \
            and url_bits[4] == data.get('repository', {}).get('name')
