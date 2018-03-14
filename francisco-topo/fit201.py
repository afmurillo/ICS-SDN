from minicps.devices import PLC
from utils import *

import time
import logging

SENSOR_ADDR = IP['fit201']

FIT201 = ('FIT201', 2)

class Fit201(PLC):
	def pre_loop(self, sleep=0.1):
		logging.basicConfig(filename=LOG_FIT201_FILE, level=logging.DEBUG)
		logging.debug('sensor enters pre_loop')
		time.sleep(sleep)

	def main_loop(self):
		count = 0
		while count<=PLC_SAMPLES:
			self.level = float(self.get(FIT201))
			logging.debug('FIT201 level %s', self.level)
			self.send(FIT201, self.level, IP['fit201'])
			time.sleep(PLC_PERIOD_SEC)


if __name__ == '__main__':
	fit201 = Fit201(name='fit201',state=STATE,protocol=FIT201_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
