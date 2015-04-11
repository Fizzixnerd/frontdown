import os

from filemover import FileMover


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
        return {"source": self.source, "target": self.target,
                "link": self.link}.__str__()

    def __repr__(self):
        return self.__str__()

    def restore(self):
        FileMover.copy(self.source, self.target)
        if self.link:
            FileMover.link(self.target, self.link)

    def backup(self):
        FileMover.copy(self.target, self.source)
