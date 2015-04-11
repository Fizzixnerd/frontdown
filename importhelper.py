import platformhelper

try:
    import yaml
    from trashcli import cmds as trash
except ImportError as e:
    logging.error("This program requires the 'python-yaml' and 'trash-cli' packages to be installed.  This program will now attempt to install them.  Or, press control+c and install it manually, then run this program again.")
    Installer().aptget_install(["python-yaml", "trash-cli"])
    import yaml
    from trashcli import cmds as trash
