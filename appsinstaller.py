import os

from system import System
from platform import Platform
from appfilereader import AppFileReader


class AppClassDoesNotExistError(Exception):
    pass


class AppsInstaller:
    """Installs classes of apps.  By default, uses the installer
    determined by Platform.

    """

    def __init__(self, installer=Platform().installer):
        self.installer = installer
        self.apps_filenames = {app_class:
                               os.path.join(System.frontdown_dir,
                                            app_class,
                                            app_class +
                                            System.apps_file_suffix)
                               for app_class in System.app_classes}
        self.apps_file_readers = {app_class: AppFileReader(app_filename)
                                  for (app_class, app_filename) in self.apps_filenames.iteritems()}

    def install_class(self, class_):
        if class_ == "all":
            map(lambda class__: self.install_class(class__),
                self.apps_file_readers.keys())
        else:
            try:
                self.installer.install(self.apps_file_readers[app_class].read_apps())
            except KeyError:
                raise AppClassDoesNotExistError("{} is not a valid app class.".format(app_class))
