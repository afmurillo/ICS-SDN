from minicps.devices import PLC
from utils import *

import time
import logging

SENSOR_ADDR = IP['ph201']

PH201 = ('PH201', 2)

class Ph201(PLC):
	def pre_loop(self, sleep=0.1):

		logging.basicConfig(filename=LOG_PH201_FILE, level=logging.DEBUG)
		logging.debug('sensor enters pre_loop')
		time.sleep(sleep)

	def main_loop(self):
		count = 0
		while count<=PLC_SAMPLES:
			self.level = float(self.get(PH201))
			logging.debug('PH201 level %s', self.level)
                        self.send(PH201, self.level, IP['ph201'])
			time.sleep(PLC_PERIOD_SEC)


if __name__ == '__main__':
	ph201 = Ph201(name='ph201',state=STATE,protocol=PH201_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
