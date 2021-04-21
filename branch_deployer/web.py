
from branch_deployer import settings

from flask import Flask


app = Flask('branch_deployer')
app.config.from_object(settings)

@app.route('/')
def home():
    return {'app': 'branch_deployer'}




