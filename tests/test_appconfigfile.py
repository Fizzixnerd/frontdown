import os
import shutil

from ..appconfigfile import AppConfigFile


class test_ClassAttributes:

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_withoutLink(self):
        acf = AppConfigFile("source", "target")
        assert (acf.source == "source")
        assert (acf.target == "target")
        assert (not acf.link)

    def test_withLink(self):
        acf = AppConfigFile("src", "tgt", "lnk")
        assert (acf.source == "src")
        assert (acf.target == "tgt")
        assert (acf.link == "lnk")

    def test_notEnoughArgs(self):
        try:
            acf = AppConfigFile("src")
            assert False
        except TypeError:
            pass


class test_BackupRestore:

    def setUp(self):
        # TODO: Make this use actual OS temporary directories.
        source_location = os.path.expanduser("~/temp/source_location/")
        target_location = os.path.expanduser("~/temp/target_location/")
        link_location = os.path.expanduser("~/temp/link_location/")
        source = os.path.join(source_location, "src")
        target = os.path.join(target_location, "tgt")
        link = os.path.join(link_location, "lnk")
        os.mkdir(os.path.expanduser("~/temp"))
        os.mkdir(source_location)
        os.mkdir(target_location)
        os.mkdir(link_location)
        os.mkdir(target)
        self.acf = AppConfigFile(source, target, link)

    def tearDown(self):
        pass
        shutil.rmtree(os.path.expanduser("~/temp"))

    def test_backup(self):
        self.acf.backup()
        assert os.path.exists(self.acf.target)
        assert os.path.exists(self.acf.source)
        assert (not os.path.exists(self.acf.link))

    def test_restore(self):
        self.acf.backup()
        shutil.rmtree(self.acf.target)
        self.acf.restore()
        assert os.path.exists(self.acf.target)
        assert os.path.exists(self.acf.source)
        # NOTE: os.path.exists returns False for broken symbolic
        # links.
        assert os.path.exists(self.acf.link)
