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
