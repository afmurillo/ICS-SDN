.DEFAULT_GOAL := final
# MiniCPS makefile

# VARIABLES {{{1
MININET = sudo mn

PYTHON = sudo python
PYTHON_OPTS = 

# regex testMatch: (?:^|[b_.-])[Tt]est)
# --exe: include also executable files
# -s: don't capture std output
# nosetests -s tests/devices_tests.py:fun_name

# TODO: add testing conditionals for verbosity, doctest plugin and coverage plugin
# http://web.mit.edu/gnu/doc/html/make_7.html

# sudo because of mininet
TESTER = sudo nosetests
TESTER_TRAVIS = nosetests
TESTER_OPTS = -s -v --exe
TESTER_OPTS_COV_HTML = $(TESTER_OPTS) --with-coverage --cover-html

# http://stackoverflow.com/questions/3931741/why-does-make-think-the-target-is-up-to-date
.PHONY: tests tests-travis clean

paper:
	cd paper-topo/; $(PYTHON) $(PYTHON_OPTS) run.py; cd ..

final:
	cd final-topo/; $(PYTHON) $(PYTHON_OPTS) run.py; cd ..

industry:
	cd industry-based/; $(PYTHON) $(PYTHON_OPTS) run.py; cd ..

prog:
	./controller.sh &
	sleep .5
	cd programatic-test/; $(PYTHON) $(PYTHON_OPTS) run.py; cd ..

fran:
	./controller.sh &
	sleep .5
	cd francisco-topo/; $(PYTHON) $(PYTHON_OPTS) run.py; cd ..

javier:
	cd javier-topo/; $(PYTHON) $(PYTHON_OPTS) run.py; cd ..

clean-simulation:
	sudo pkill  -f -u root "python -m cpppo.server.enip"
	sudo mn -c
	sudo pkill -9 python2.7
