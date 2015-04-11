import subprocess


class InstallError(Exception):
    pass


class AptError(InstallError):
    pass


class Installer:
    """Abstract Base Class for an installer.  Represents the installation
    system for the current platform (ie apt, yum, pacman, emerge,
    etc).

    """

    def __init__(self):
        self.update()

    def install(self, apps=[]):
        raise InstallError("This is a generic installer.  Use a specialized one.")

    def update(self):
        raise InstallError("This is a generic installer.  Use a specialized one.")


class AptInstaller(Installer):
    """Installer for apt-based systems.

    """

    def _aptget(self, command, args=[]):
        command_list = ["sudo", "apt-get", command]
        command_list.extend(args)
        exit_code = subprocess.call(command_list)
        if not exit_code:
            return 0
        else:
            raise AptError("Apt exited with non-zero exit code {} when called with commands {}".format(exit_code, command_list))

    def update(self):
        return self._aptget("update")

    def install(self, apps=[]):
        return self._aptget("install", apps)
