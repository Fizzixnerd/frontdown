from installer import AptInstaller, YumInstaller, ArchInstaller, GentooInstaller


class Platform:
    """Create to determine the current platform.  Its `installer' member is the
    appropriate installer for the platform.

    Only works on debian-derived platforms currently.

    """

    def __init__(self):
        with open("/etc/os-release") as f:
            lines = f.readlines()
        values = Platform._os_release_lines_to_dict(lines)
        self.id = values["ID"]
        self.id_like = values.get("ID_LIKE")
        self.installer = self.determine_installer()

    @staticmethod
    def _os_release_lines_to_dict(lines):
        ret = {}
        for line in lines:
            name, value = line.split("=")
            ret[name] = value.strip()
        return ret

    def determine_installer(self):
        if (self.id_like == "debian") or \
           (self.id_like == "ubuntu") or \
           (self.id == "debian"):
            return AptInstaller()
        elif self.id == "arch":
            return ArchInstaller()
        elif self.id == "gentoo":
            return GentooInstaller()
        elif (self.id == "fedora") or \
             (self.id == "red-hat") or \
             (self.id == "centos"):
            return YumInstaller()
