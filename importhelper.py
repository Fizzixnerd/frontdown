from platform import Platform

try:
    import yaml
    import trashcli
except ImportError as e:
    logging.error("This program requires the 'python-yaml' and 'trash-cli' packages to be installed.  This program will now attempt to install them.  Or, press control+c and install it manually, then run this program again.")
    Platform().installer.install(["python-yaml", "trash-cli"])
    import yaml
    import trashcli
