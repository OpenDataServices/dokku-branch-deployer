# All Configuration Options

Configuration is done by a mix of environment variables and a settings file.

Some config options must be set in environment variables, as they are used in several different places.  Most settings can in theory be set in either place.

A settings file must be placed in `/app/settings/settings.yaml` inside the container. If you follow the setup instructions in the docs, that means at `/var/lib/dokku/data/storage/$APP_NAME/settings/settings.yaml` on your host.

## SSH_DOKKU_* environment variables

The connection information for your Dokku server via SSH. The only required one is `SSH_DOKKU_HOST` which has no default
and nothing else really works without it. The others have useful defaults:

```dotenv
SSH_DOKKU_HOST=dokku.me # set this to your domain
SSH_DOKKU_USER=dokku # default
SSH_DOKKU_PORT=22 # default
```

## LOG_LEVEL environment variable

Can be the usual things (e.g. 'DEBUG', 'INFO', etc.). Default is 'INFO'.

## GITHUB_SECRET environment variable

When you create your webhook in your GitHub repo settings, you have the option of setting a secret. It's highly recommended that you set this. If you do, github will use that secret to calculate an HMAC signature of the POST data using SHA1 and [send it with the POST in a header](https://developer.github.com/webhooks/#delivery-headers). Set the same secret in this variable to have the app calculate the same HMAC signature and verify that they match. In this way we can verify that this POST request did indeed come from a service that has this secret, which hopefully means only Github.

## Repositories

The app needs to know a list of repostories it should process. It will only process these apps.

These have to be set in the settings file. Eg:

```yaml
repositories:                                                           
  - id: test-dokku-jekyll                                               
    url: https://github.com/OpenDataServices/test-dokku-jekyll
    app_name_format: {repo_name}-{branch_name}
    all_branches: false
    get_repository_by_ssh: false
    branches:                                                           
        - main
    setup_dokku_commands:
      - dokku postgres:create pg-$APP_NAME
      - dokku postgres:link pg-$APP_NAME $APP_NAME
    teardown_dokku_commands:
      - dokku postgres:unlink pg-$APP_NAME $APP_NAME
      - dokku postgres:destroy pg-$APP_NAME -f
```

### id

Each repository should have an unique Id

### url

This should be the URL of the GitHub repository. Currently only GitHub is supported.

### app_name_format

The app name for each branch is set by this format.

The following variables can be used:

* `{repo_owner}` - Repo owner. eg for https://github.com/OpenDataServices/dokku-branch-deployer this is `OpenDataServices`
* `{repo_name}` - Repo name. eg for https://github.com/OpenDataServices/dokku-branch-deployer this is `dokku-branch-deployer`
* `{branch_name}` - Branch name

### all_branches

If set, every branch of this repo will be deployed. 

If not set, only specific branches will be deployed and further settings are needed to configure that.

### branches

This should be a list of branch names to deploy

### setup_dokku_commands & teardown_dokku_commands

In some cases, there may be other things you need to do to setup or teardown the app here, such as:

* Attach databases
* Enable lets encrypt
* Set a basic auth password so dev sites can't be seen be everyone

You can do the commands to do so here.

These can only be dokku commands.

The special token `$APP_NAME` will be replaced with the name of the app for that branch.

### get_repository_by_ssh

This determines how git operations are run against the source repository.

If false, http actions will be used. Use for public repositories only. Works like:

    git clone https://github.com/OpenDataServices/dokku-branch-deployer.git

If true, ssh actions will be used. Use for private repositories, but remember you'll need to add a deploy key. Works like:

    git clone git@github.com:OpenDataServices/dokku-branch-deployer.git
