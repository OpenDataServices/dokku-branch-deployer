from pathlib import Path
import os.path
import yaml
from .models import RepositoryModel

from everett.manager import (
    ConfigEnvFileEnv,
    ConfigManager,
    ConfigOSEnv,
    ListOf,
)

config = ConfigManager([
    # first check for environment variables
    ConfigOSEnv(),
    # then look in the .env file
    ConfigEnvFileEnv('.env'),
])

# SSH settings need to come from env and not a file, because other scripts in bin/ also use them.
SSH_DOKKU_HOST = config('SSH_DOKKU_HOST', raise_error=False)
SSH_DOKKU_PORT = config('SSH_DOKKU_PORT', parser=int, default='22')
SSH_DOKKU_USER = config('SSH_DOKKU_USER', default='dokku')

# Some paths are hard coded for now
BASE_PATH = Path(__file__).parents[1]
REPOS_BASE_PATH = BASE_PATH / 'repos'
DEPLOY_LOGS_BASE_PATH = BASE_PATH / 'deploy-logs'
SETTINGS_BASE_PATH = BASE_PATH / 'settings'

# These settings can in theory come from env or file
GITHUB_SECRET = config('GITHUB_SECRET', raise_error=False)
REPOSITORIES = []
LOG_LEVEL = config('LOG_LEVEL', default='INFO')

if os.path.exists(os.path.join(SETTINGS_BASE_PATH, "settings.yaml")):
    with open(os.path.join(SETTINGS_BASE_PATH, "settings.yaml")) as fp:
        settings_data = yaml.safe_load(fp)
    for r in settings_data.get('repositories'):
        REPOSITORIES.append(RepositoryModel(r))
