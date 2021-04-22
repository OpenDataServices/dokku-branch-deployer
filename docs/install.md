# Installation

This app is meant to be deployed to your [Dokku][] server, but could really run anywhere. All that is required
is for Github to be able to post webhooks to it, and for it to have SSH access to your Dokku server. All of the shell
commands below should be run on your Dokku server as the `dokku` user.

It also does not have to run on the Dokku server it is managing, althought for simplicity we see no reason not to do that.

## 1. Create and configure your app

```shell
$ export APP_NAME=deployer # or whatever you want your app name to be
$ dokku apps:create $APP_NAME
$ dokku config:set $APP_NAME \
    GITHUB_SECRET=<sekrit> \ # the secret you use to configure webhooks at github
    SSH_DOKKU_HOST=dokku.me \ # your dokku server domain    
```

You can see more about all of the configuration options in the [config docs](config.md), but this should
be a good start.

## 2. Setup the volumes

The app will store some things on the Dokku host: ssh keys, deployment logs, settings, and the bare git repos.

```shell
$ mkdir -p /var/lib/dokku/data/storage/$APP_NAME/{ssh,deploy-logs,repos,settings}
$ dokku storage:mount $APP_NAME /var/lib/dokku/data/storage/$APP_NAME/ssh:/home/dokku/.ssh
$ dokku storage:mount $APP_NAME /var/lib/dokku/data/storage/$APP_NAME/deploy-logs:/app/deploy-logs
$ dokku storage:mount $APP_NAME /var/lib/dokku/data/storage/$APP_NAME/repos:/app/repos
$ dokku storage:mount $APP_NAME /var/lib/dokku/data/storage/$APP_NAME/settings:/app/settings
```

## 3. Create the settings file

```shell
$ vi /var/lib/dokku/data/storage/$APP_NAME/settings:/app/settings/settings.yaml
```

You can see more about all of the configuration options in the [config docs](config.md), but for now you can leave it blank.

## 4. Setup the build arguments

Because the app interacts with the filesystem via the above volumes, it's best if it does so as the `dokku`
user so that permission issues don't arise. To combat that the Dockerfile will accept build args for the user
and group IDs for the local user and will add said user in the image and run as that user rather than root.

```shell
$ dokku docker-options:add $APP_NAME build "--build-arg GROUP_ID=$(id -g)"
$ dokku docker-options:add $APP_NAME build "--build-arg USER_ID=$(id -u)"
```

## 5. Create an SSH key

The app communicates with Dokku via SSH. You should create a new key pair for this specifically.
Make sure you create it with an empty passphrase.

```shell
$ pushd /var/lib/dokku/data/storage/$APP_NAME/ssh
$ ssh-keygen -t rsa -b 4096 -C "dokku-branch-deployer" -f ./id_rsa
```

Then you can add it to your Dokku users:

```shell
$ sudo dokku ssh-keys:add dokku-branch-deployer ./id_rsa.pub
```

> Note: You may have to do this one as root. Run it via `sudo` from an account with permission to do that.

## 6. Deploy the webhook-deploy app

From your machine:

```shell
$ git clone https://github.com/pmac/dokku-webhook-deploy
```

Push this to the Dokku app you previously created.

Once the initial deployment
is finished and working it is strongly recommended to use the [Let's Encrypt plugin][] to enable TLS on this app so that
communication between GitHub and your server is encrypted:

```shell
$ dokku letsencrypt $APP_NAME
```

## 7. Setup the webhook in Github

Navigate to your repo's webhook settings (URL below) and enter the following for the web:

* URL: `https://github.com/<your-user-or-org>/<your-repo>/settings/hooks/new`
* Payload URL: `https://deployer.<your-dokku-server-domain>/hooks/github`
* Content Type: `application/json`
* Secret: The secret you set in your app config from step 3
* Which events would you like to trigger this webhook?: `Just the push event`
* Active: checked

## 8. Profit

You should be done! 

