from pathlib import Path
import os.path
import yaml
from .models import RepositoryModel

BASE_PATH = Path(__file__).parents[1]
REPOS_BASE_PATH = BASE_PATH / 'repos'
DEPLOY_LOGS_BASE_PATH = BASE_PATH / 'deploy-logs'
SETTINGS_BASE_PATH = BASE_PATH / 'settings'

REPOSITORIES = []

if os.path.exists(os.path.join(SETTINGS_BASE_PATH, "settings.yaml")):
    with open(os.path.join(SETTINGS_BASE_PATH, "settings.yaml")) as fp:
        settings_data = yaml.safe_load(fp)
    for r in settings_data.get('repositories'):
        REPOSITORIES.append(RepositoryModel(r))

