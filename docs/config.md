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
    branches:                                                           
        - main
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

If not set, only specific branches will deployed and further settings are needed to configure that.

### branches

This should be a list of branch names to deploy


