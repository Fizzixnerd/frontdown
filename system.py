import os


class System:
    """The frontdown_dir contains the different app classes as
    directories.  Each directory contains FIXME

    """
    frontdown_dir = os.path.expanduser("~/.system/frontdown.d/")
    app_classes = [app_class
                   for app_class in os.listdir(frontdown_dir)
                   if os.path.isdir(os.path.join(frontdown_dir, app_class))]
        # Right now System.app_classses looks something like:
        # ["core", "programming", "art", "gaming", "gui", "misc"]
