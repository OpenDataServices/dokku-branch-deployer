# CLI

There are some CLI commands

## Show Config

This just prints out all config settings.

```shell
$ python -m branch_deployer.cli showsettings
```

## Process

This will process all repositories that are configured.

Use this if a webhook call was missed for some reason, or if the repository config has changed.

```shell
$ python -m branch_deployer.cli process
```
