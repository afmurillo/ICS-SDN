from minicps.devices import PLC
from utils import *

import time
import signal
import sys

SENSOR_ADDR = IP['ph201']

PH201 = ('PH201', 2)

class Ph201(PLC):
	def sigint_handler(self, sig, frame):
		print "I received a SIGINT!"
		sys.exit(0)

	def pre_loop(self, sleep=0.1):
		signal.signal(signal.SIGINT, self.sigint_handler)
		signal.signal(signal.SIGTERM, self.sigint_handler)
	def main_loop(self):
		print 'DEBUG: sensor enters main_loop'
		count = 0
		while count<=PLC_SAMPLES:
			self.level = float(self.get(PH201))
			self.send(PH201, self.level, IP['ph201'])
			time.sleep(PLC_PERIOD_SEC)


if __name__ == '__main__':
	ph201 = Ph201(name='ph201',state=STATE,protocol=PH201_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
