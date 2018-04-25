from minicps.devices import PLC
from utils import *
import logging
import time

SENSOR_ADDR = IP['lit102']

LIT102 = ('LIT102', 1)

class Lit102(PLC):
	def pre_loop(self, sleep=0.1):
		logging.basicConfig(filename=s, level=logging.DEBUG)
		logging.debug('sensor enters pre_loop')
		time.sleep(sleep)

	def main_loop(self):
		print 'DEBUG: sensor enters main_loop'
		count = 0
		while count<=PLC_SAMPLES:
			self.level = float(self.get(LIT102))
			logging.debug('LIT102 level %s', self.level)			
			self.send(LIT102, self.level, IP['lit102'])
			time.sleep(PLC_PERIOD_SEC)


if __name__ == '__main__':
	lit102 = Lit102(name='lit102',state=STATE,protocol=LIT102_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
			

