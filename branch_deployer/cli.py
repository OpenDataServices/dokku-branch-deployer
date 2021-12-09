import argparse

from branch_deployer import settings
import branch_deployer.lib


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="subparser_name")

    subparsers.add_parser("showsettings")

    subparsers.add_parser("process")

    args = parser.parse_args()

    if args.subparser_name == "showsettings":

        print("BASE_PATH = " + str(settings.BASE_PATH))
        print("REPOS_BASE_PATH = " + str(settings.REPOS_BASE_PATH))
        print("DEPLOY_LOGS_BASE_PATH = " + str(settings.DEPLOY_LOGS_BASE_PATH))
        print("SETTINGS_BASE_PATH = " + str(settings.SETTINGS_BASE_PATH))

        for repository in settings.REPOSITORIES:
            print("------ REPOSITORY")
            print("id = " + repository.id)
            print("url = " + repository.url)
            print("Clone URL = " + repository.clone_url)
            print("Local Git Dir = " + repository.local_git_directory)
            print("App Name Format = " + repository.app_name_format)
            print("All branches = " +
                  ("Yes" if repository.all_branches else "No"))
            if not repository.all_branches and repository.branches:
                print("Branches = ")
                [print("- " + b) for b in repository.branches]
            if repository.setup_dokku_commands:
                print("Setup Commands = ")
                [print("- " + b) for b in repository.setup_dokku_commands]
            if repository.teardown_dokku_commands:
                print("Leave Commands = ")
                [print("- " + b) for b in repository.teardown_dokku_commands]

    elif args.subparser_name == "process":

        for repository in settings.REPOSITORIES:
            print("------ REPOSITORY " + repository.url)
            branch_deployer.lib.update_repo(repository)
            for branch_name in \
                    branch_deployer.lib.get_all_branches_in_repo(repository):
                if repository.should_deploy_branch(branch_name):
                    print("Will Deploy branch " + branch_name)
                    branch_deployer.lib.app_create(repository, branch_name)
                    branch_deployer.lib.push_repo(repository, branch_name)


if __name__ == "__main__":
    main()
