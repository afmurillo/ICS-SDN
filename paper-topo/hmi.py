#!/usr/bin/python

from utils import *
from socket import *
from time import sleep

# need to have 3 different connections or an array of connections
connections = 3

PLC1_ADDRESS = '192.168.4.1'
PLC2_ADDRESS = '192.168.4.2'
PLC3_ADDRESS = '192.168.4.3'
SELF_ADDRESS = '192.168.4.4'
HMI_PORT = int(PORTS['hmi_poll_port'])
BUFFER_SIZE = 100

# Setup TCP connections with all the PLCs
def setupConnection():
	s = socket(AF_INET, SOCK_STREAM)
	s.bind((SELF_ADDRESS, HMI_PORT))
	s.listen(1)
	sockets = []
	for _ in xrange(connections):
		conn, addr = s.accept()
		sockets += [(conn, addr)]
	return sockets

# at every PLC_PERIOD_SEC*10 poll values from all the PLCs
def pollValue(sockets):
	while True:
		sleep(PLC_PERIOD_SEC*10)
		# for each connection, get value.
		for conn, addr in sockets:
			conn.send('POLL')
			data = None
			while not data:
				data = conn.recv(BUFFER_SIZE)
			print "Data from " + str(addr) + " : " + data

if __name__=="__main__":
	sockets = setupConnection()
	# After this all the connections are already up and running.
	# Now we can begin polling the values.
	pollValue(sockets)
