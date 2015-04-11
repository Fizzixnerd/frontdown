import os
import shutil
import logging

from trash import trash


class FileMover:

    @staticmethod
    def copy(src, tgt):
        if os.path.exists(tgt):
            logging.info("Moving old {0} to the Trash.".format(tgt))
            trash(tgt)
        logging.info("Copying {0} to {1}.".format(src, tgt))
        if os.path.isdir(src):
            shutil.copytree(src, tgt)
        else:
            shutil.copy(src, tgt)

    @staticmethod
    def link(tgt, lnk):
        if os.path.exists(lnk):
            logging.info("Moving old {0} to the Trash.".format(lnk))
            trash(lnk)
        logging.info("Symlinking {0} to {1}".format(lnk, tgt))
        os.symlink(tgt, lnk)
