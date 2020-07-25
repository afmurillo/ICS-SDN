from minicps.devices import PLC
from utils import *

import time
import signal
import sys

PLC201_ADDR = IP['plc201']

P201 = ('P201', 2)

class PP201(PLC):
	def sigint_handler(self, sig, frame):
		print "I received a SIGINT!"
		sys.exit(0)

	def pre_loop(self, sleep=0.1):
		signal.signal(signal.SIGINT, self.sigint_handler)
		signal.signal(signal.SIGTERM, self.sigint_handler)

	def main_loop(self):
		print 'DEBUG: p201 enters main_loop'
		count = 0
		while count<=PLC_SAMPLES:
			p201 = int(self.receive(P201, PLC201_ADDR))
			print "DEBUG: Received p201 command %.5f" % p201
			self.set(P201, p201)


if __name__ == '__main__':
	p201 = PP201(name='p201',state=STATE,protocol=P201_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)

