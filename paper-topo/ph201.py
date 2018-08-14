from minicps.devices import PLC
from utils import *

import time

SENSOR_ADDR = IP['ph201']

PH201 = ('PH201', 2)

class Ph201(PLC):
	def pre_loop(self, sleep=0.1):
		print 'DEBUG: sensor enters pre_loop'
		time.sleep(sleep)

	def main_loop(self):
		print 'DEBUG: sensor enters main_loop'
		count = 0
		while count<=PLC_SAMPLES:
			self.level = float(self.get(PH201))
			self.send(PH201, self.level, IP['ph201'])
			time.sleep(PLC_PERIOD_SEC)


if __name__ == '__main__':
	ph201 = Ph201(name='ph201',state=STATE,protocol=PH201_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
