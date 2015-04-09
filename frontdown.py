#!/usr/bin/env python

# Copyright Matthew Walker 2014
# See LICENSE file for redistribution terms.

"""See LICENSE file for redistribution terms.

"""

import os
import shutil
import subprocess

import argparse
import logging

from system import System

try:
    import yaml
    from trashcli import cmds as trash
except ImportError as e:
    logging.error("This program requires the 'python-yaml' and 'trash-cli' packages to be installed.  This program will now attempt to install them.  Or, press control+c and install it manually, then run this program again.")
    Installer().aptget_install(["python-yaml", "trash-cli"])
    import yaml
    from trashcli import cmds as trash


class AptError(Exception):
    pass


class AppClassDoesNotExistError(Exception):
    pass


class Installer:
    def __init__(self):
        suffix = ".apps"
        self.apps_filenames = {app_class: os.path.join(System.frontdown_dir, app_class,
                                                       app_class + suffix)
                               for app_class in System.app_classes}
        self.aptget_update()
        self.aptget_upgrade()

    def aptget(self, command, args=[]):
        command_list = ["sudo", "apt-get", command]
        command_list.extend(args)
        exit_code = subprocess.call(command_list)
        if not exit_code:
            return 0
        else:
            raise AptError("Apt exited with non-zero exit code {0}".format(exit_code))

    def aptget_update(self):
        return self.aptget("update")

    def aptget_upgrade(self):
        return self.aptget("upgrade")

    def aptget_install(self, package_list=[]):
        return self.aptget("install", package_list)

    def list_packages_from_file(self, filename):
        package_list = []
        with open(filename) as f:
            for line in f:
                package_list.extend(line.split())
        return package_list

    def install(self, app_class_list=[]):
        if "all" in app_class_list:
            app_class_list = self.apps_filenames
        for app_class in app_class_list:
            if app_class in System.app_classes:
                self.aptget_install(self.list_packages_from_file(
                    self.apps_filenames[app_class]))
            else:
                raise AppClassDoesNotExistError(
                    "%s is not a valid app class." % app_class)


class AppConfigFile:
    def __init__(self, source, target, link=None):
        # source is the backup location.
        self.source = os.path.expanduser(source)
        # target is the location the file must be in a standard install.
        self.target = os.path.expanduser(target)
        if link:
            self.link = os.path.expanduser(link)
        else:
            self.link = None

    def __str__(self):
        return str({"source": self.source, "target": self.target,
                    "link": self.link}.__str__())

    def __repr__(self):
        return self.__str__()

    def _copy(self, src, tgt):
        # FIXME OMG THIS IS SO DANGEROUS AND IT LIES!
        if os.path.exists(tgt):
            logging.info("Moving old {0} to the Trash.".format(tgt))
            trash.put(tgt)
        logging.info("Copying {0} to {1}.".format(src, tgt))
        if os.path.isdir(src):
            shutil.copytree(src, tgt)
        else:
            shutil.copy(src, tgt)

    def _link(self, tgt, lnk):
        logging.info("Symlinking {0} to {1}".format(lnk, tgt))
        if os.path.exists(lnk):
            logging.info("Moving old {0} to the Trash.".format(lnk))
            trash.put(lnk)
        os.symlink(tgt, lnk)

    def restore(self):
        self._copy(self.source, self.target)
        if self.link:
            self._link(self.target, self.link)

    def backup(self):
        self._copy(self.target, self.source)


class AppConfig:
    def __init__(self, app_config_files=[]):
        self.config_files = app_config_files

    def __str__(self):
        return self.config_files.__str__()

    def __repr__(self):
        return self.__str__()

    def pre_backup(self):
        pass

    def post_backup(self):
        pass

    def pre_restore(self):
        pass

    def post_restore(self):
        pass

    def backup(self):
        self.pre_backup()
        for config_file in self.config_files:
            config_file.backup()
        self.post_backup()

    def restore(self):
        self.pre_restore()
        for config_file in self.config_files:
            config_file.restore()
        self.post_restore()


class AppConfigParser:
    @staticmethod
    def parse_file(control_filename):
        with open(control_filename) as f:
            parsed_yaml = yaml.load(f)
        filenames_list = parsed_yaml["files"]
        app_config_files = [
            AppConfigFile(os.path.join(System.frontdown_dir, files["source"]),
                          files["target"],
                          files.get("link"))
            for files in filenames_list]
        app_config = AppConfig(app_config_files)
        return app_config

    @staticmethod
    def parse_directory(directory_name):
        return [
            AppConfigParser.parse_file(os.path.join(directory_name, filename))
            for filename in os.listdir(directory_name)
            if filename.endswith(".yaml")]

    @staticmethod
    def parse_class_directory(app_class):
        directory_name = os.path.join(System.frontdown_dir, app_class)
        return [
            AppConfigParser.parse_directory(os.path.join(directory_name, filename))
            for filename in os.listdir(directory_name)
            if os.path.isdir(os.path.join(directory_name, filename))]


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
