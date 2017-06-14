from minicps.devices import PLC
from utils import *

import time

SENSOR_ADDR = IP['lit301']

LIT301 = ('LIT301', 3)

class Lit301(PLC):
	def pre_loop(self, sleep=0.1):
		print 'DEBUG: sensor enters pre_loop'
		time.sleep(sleep)

	def main_loop(self):
		print 'DEBUG: sensor enters main_loop'
		count = 0
		while count<=PLC_SAMPLES:
			self.level = float(self.get(LIT301))
			print "LIT301", self.level
			self.send(LIT301, self.level, IP['lit301'])
			time.sleep(PLC_PERIOD_SEC)


if __name__ == '__main__':
	lit301 = Lit301(name='lit301',state=STATE,protocol=LIT301_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
			

