import os
import shutil

from ..filemover import FileMover


class test_FileMover:
    # TODO: Use real OS temporary directories

    def setUp(self):
        os.mkdir("temp")
        os.mkdir("temp/src")

    def tearDown(self):
        shutil.rmtree("temp")

    def test_copy(self):
        FileMover.copy("temp/src", "temp/tgt")
        assert os.path.exists("temp/tgt")
        assert os.path.exists("temp/src")

    def test_copyExisting(self):
        os.mkdir("temp/tgt")
        os.mkdir("temp/tgt/1")
        FileMover.copy("temp/src", "temp/tgt")
        assert os.path.exists("temp/tgt")
        assert not os.path.exists("temp/tgt/1")
        assert os.path.exists("temp/src")

    def test_link(self):
        FileMover.link("src", "temp/lnk")
        assert os.path.exists("temp/src")
        assert os.path.exists("temp/lnk")

    def test_linkExisting(self):
        os.mkdir("temp/lnk")
        FileMover.link("src", "temp/lnk")
        assert os.path.exists("temp/src")
        assert os.path.exists("temp/lnk")
