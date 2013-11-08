VIRTUALENV = venv/
# Makefile
install:
	virtualenv venv --no-site-packages --distribute
	# Install pip packages
	. $(VIRTUALENV)bin/activate; pip install -r requirements.txt
# EOF