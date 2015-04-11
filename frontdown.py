#!/usr/bin/env python

# Copyright Matthew Walker 2014-2015
# See LICENSE file for redistribution terms.

"""See LICENSE file for redistribution terms.

"""

import argparse

import importhelper  # checks for yaml and trashcli.
from system import System
from platform import Platform
from appsinstaller import AppsInstaller
from appconfigparser import AppConfigParser


def main():
    parser = argparse.ArgumentParser(description="Restore a Linux system to a previous state in terms of applications installed and configuration files.",
                                     add_help=True)
    main_command = parser.add_mutually_exclusive_group()
    main_command.add_argument("--install", nargs="+", type=str,
                              choices=System.app_classes,
                              help="Install a class of apps, and restore their configuration files.")
    main_command.add_argument("--backup", nargs="+", type=str,
                              choices=System.app_classes,
                              help="Initiate backup to the frontdown directory.")
    main_command.add_argument("--restore", nargs="+", type=str,
                              choices=System.app_classes,
                              help="Initiate a restore from the frontdown directory.")
    args = parser.parse_args()

    app_classes = args.install or args.backup or args.restore

    if not app_classes:
        parser.print_help()
        exit(0)

    if "all" in app_classes:
        app_classes = filter(lambda x: x != "all", System.app_classes)

    app_configs = map(AppConfigParser.parse_class_directory,
                      app_classes)

    if args.install:
        apps_installer = AppsInstaller(Platform().installer)
        map(apps_installer.install_class, app_classes)
        exit(0)

    for config_class in app_configs:
        for configs in config_class:
            for app_config in configs:
                if args.restore:
                    app_config.restore()
                elif args.backup:
                    app_config.backup()
    exit(0)

if __name__ == "__main__":
    main()
