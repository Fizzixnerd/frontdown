class AppsFileReader:
    """Reads a ".apps" file and can return a list of the apps listed
    within.

    """

    def __init__(self, filename):
        self.filename = filename

    def read_apps(self):
        app_list = []
        with open(self.filename) as f:
            for line in f:
                app_list.extend(line.split())
        return app_list
