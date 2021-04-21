
from branch_deployer import settings
import os

class RepositoryModel:
    def __init__(self, settings_data):
        url_bits = settings_data['url'].split('/')
        if url_bits[2] != 'github.com':
            raise Exception('We only support  GitHub.com')
        self.url = settings_data['url']
        self.id = settings_data['id']
        self.clone_url = self.url + ".git"
        self.local_git_directory = os.path.join(settings.REPOS_BASE_PATH, "github", url_bits[3], url_bits[4])
        self.branches = settings_data.get('branches',[])

    def should_deploy_branch(self, branch_name):
        if branch_name in self.branches:
            return True
        return False
