#!/usr/bin/python

import os

git_plugins_dir = os.path.dirname(os.path.realpath(__file__)) + "/downloads/plugins/git/"


def update_plugins():
    for plugin in next(os.walk(git_plugins_dir))[1]:
        message = """
        ===========================
        updating plugin $
        ===========================
        """.replace("$", plugin)  # type: str
        print(message)
        os.chdir(git_plugins_dir + plugin)
        os.system("git reset --hard")
        os.system("git fetch --all")
        os.system("git pull")
        os.system("composer.phar update")


if __name__ == "__main__":
    update_plugins()

