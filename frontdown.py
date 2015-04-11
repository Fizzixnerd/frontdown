#!/usr/bin/env python

# Copyright Matthew Walker 2014-2015
# See LICENSE file for redistribution terms.

"""See LICENSE file for redistribution terms.

"""

import argparse

from system import System
from appconfigparser import AppConfigParser
from installer import Installer


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
    app_configs = [AppConfigParser.parse_class_directory(app_class)
                   for app_class in app_classes]
    if args.install:
        installer = Installer()
        installer.install(args.install)

    for config_class in app_configs:
        for _ in config_class:
            for app_config in _:
                if args.restore or args.install:
                    app_config.restore()
                elif args.backup:
                    app_config.backup()

if __name__ == "__main__":
    main()
