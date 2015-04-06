scripts='scripts/bash/rrawc.bash scripts/bash/slca.bash scripts/bash/touchpad.sh scripts/bash/start_emacs_server.bash'


.PHONY : all make-scripts-executable

all :
	make make-scripts-executable

make-scripts-executable : ${scripts}
	chmod +x ${scripts}

