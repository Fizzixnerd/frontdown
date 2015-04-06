# frontdown

A simple Linux apt-based backup utility

This is a backup program designed for use on apt-based systems such as
Ubuntu and Debian.  It allows users to classify their apps into
"classes", which can be installed and configured in groups.

For each program installed, one can assign configuration files that
one wishes to be backed-up/restored.

For example, one could create a class "programming" which contained
the apps "emacs" and "ipython", which backed-up and restored those
programs along with their configuration files.

One would create a folder in ~/.system/frontdown.d/ called
"programming".  Within this folder, create a file called
"programming.apps" and place within it a space- and/or
newline-separated list of programs which will be fed to apt-get to
install.  In this case, the file would contain "emacs ipython".

Then create folders "ipython" and "emacs" within
~/.system/frontdown.d/programming/.  It does not matter what you
actually call these folders, so you can organize things so that you
have, say, a "python" folder that takes care of all your python
configs.

Create a file within the folder "python" called "python.yaml" which
looks like this (your config may look slightly different depending on
how you setup ipython):

# python.yaml
files:
  - source: programming/python/.ipython_history
    target: ~/.ipython_history

  - source: programming/python/ipython
    target: ~/.config/ipython
# EOF

This will tell frontdown that you want to backup your ipython history
and configuration, and where to restore those files to.  The source
location is relative to ~/.system/frontdown.d/; you do not need to mix your
configuration and backup files if that is your wish.

Similarly, create a file called "emacs.yaml" that contains:

# emacs.yaml
files:
  - source: programming/emacs/.emacs
    target: ~/.emacs
# EOF

Now when running "frontdown --backup programming", frontdown will copy
and paste the files/directories listed in the yaml config files to
their source directories.  Running "frontdown --restore programming"
performs the inverse action.  Finally, "frontdown --install
programming" first installs emacs and ipython, and then restores their
configurations.

There is also a "link" option in addition to "source" and "target".
If present, it will create a symbolic link in the given location that
points to the restored file.
