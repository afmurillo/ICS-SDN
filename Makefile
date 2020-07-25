.DEFAULT_GOAL := final
# MiniCPS makefile

# VARIABLES {{{1
MININET = sudo mn

PYTHON = sudo python
PYTHON_OPTS = 

paper:
	if [ ! -d paper-topo/logs ]; then\
	   mkdir paper-topo/logs;\
	fi
	if [ ! -d paper-topo/output ]; then\
	   mkdir paper-topo/output;\
	fi
	cd paper-topo; rm -rf industry_db.sqlite; $(PYTHON) $(PYTHON_OPTS) init.py; sudo chown mininet:mininet industry_db.sqlite
	sudo pkill -f -u root "python -m cpppo.server.enip"
	sudo mn -c
	cd paper-topo; sudo $(PYTHON) $(PYTHON_OPTS) run.py

replay:
	cd replay-topo/; $(PYTHON) $(PYTHON_OPTS) run.py; cd ..

fran:
	./controller.sh &
	sleep .5
	cd francisco-topo/; $(PYTHON) $(PYTHON_OPTS) run.py; cd ..

linear:
	sleep .5
	cd non-linear-sdn/; $(PYTHON) $(PYTHON_OPTS) run.py; cd ..

clean-simulation:
	sudo pkill  -f -u root "python -m cpppo.server.enip"
	sudo mn -c

kill:
	sudo pkill python
