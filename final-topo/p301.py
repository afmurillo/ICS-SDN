from minicps.devices import PLC
from utils import *

import time

PLC301_ADDR = IP['plc301']

P301 = ('P301', 3)

class PP301(PLC):
	def pre_loop(self, sleep=0.1):
		print 'DEBUG: p301 enters pre_loop'
		time.sleep(sleep)

	def main_loop(self):
		print 'DEBUG: p301 enters main_loop'
		count = 0
		while count<=PLC_SAMPLES:
			p301 = int(self.receive(P301, PLC301_ADDR))
			print "DEBUG: Received p301 command %.5f" % p301
			self.set(P301, p301)


if __name__ == '__main__':
	p301 = PP301(name='p301',state=STATE,protocol=P301_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
#	p301.pre_loop()
#	p301.main_loop()

