import os

import yaml

from system import System
from appconfig import AppConfig
from appconfigfile import AppConfigFile


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
            AppConfigParser.parse_directory(os.path.join(directory_name,
                                                         filename))
            for filename in os.listdir(directory_name)
            if os.path.isdir(os.path.join(directory_name, filename))]
