from branch_deployer import settings
import branch_deployer.lib
import hmac
from flask import Flask, request
from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': settings.LOG_LEVEL,
        'handlers': ['wsgi']
    }
})


app = Flask('branch_deployer')
app.config.from_object(settings)

@app.route('/')
def home():
    return {'app': 'branch_deployer'}

@app.route('/hooks/github', methods=['POST'])
def hooks():
    sig = check_github_sig()
    if sig is not None:
        return sig

    handle_push(request.json)
    return '', 204


def check_github_sig():
    if settings.GITHUB_SECRET:
        signature = request.headers.get('X-Hub-Signature')
        if signature:
            their_sig = signature[5:]
            key = settings.GITHUB_SECRET.encode()
            our_sig = hmac.new(key, request.data, 'sha1').hexdigest()
            if their_sig != our_sig:
                app.logger.warning(f'HMAC error: {their_sig}, {our_sig}')
                return 'HMAC Signature error', 401
        else:
            app.logger.warning('No HMAC signature received')
            return 'HMAC Signature missing', 401

    return None


def handle_push(data):
    for repository in settings.REPOSITORIES:
        if repository.matches_github_webhook_data(data):
            branch_name = branch_deployer.lib.get_branch_name(data['ref'])
            branch_deployer.lib.update_repo(repository)
            branch_deployer.lib.app_create(repository, branch_name)
            branch_deployer.lib.push_repo(repository, branch_name)

