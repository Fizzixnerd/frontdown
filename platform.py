from installer import AptInstaller


class Platform:
    """Create to determine the current platform.  Its member is the
    appropriate installer for the platform.

    Only works on apt-based platforms currently.

    """

    def __init__(self):
        self.installer = AptInstaller()
