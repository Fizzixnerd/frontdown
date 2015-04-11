import sys

from trashcli.trash import TrashPutCmd


def trash(filename):
    tpc = TrashPutCmd(sys.stdout, sys.stderr)
    tpc.run(["", filename])
