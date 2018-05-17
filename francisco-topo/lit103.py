from minicps.devices import PLC
from utils import *
import logging
import time

SENSOR_ADDR = IP['lit103']

LIT103 = ('LIT103', 1)

class Lit103(PLC):
	def pre_loop(self, sleep=0.1):
		logging.basicConfig(filename=LOG_LIT103_FILE, level=logging.DEBUG)
		time.sleep(sleep)

	def main_loop(self):
		print 'DEBUG: sensor enters main_loop'
		count = 0
		while count<=PLC_SAMPLES:
			self.level = float(self.get(LIT103))
			logging.debug('LIT103 level %s', self.level)			
			self.send(LIT103, self.level, IP['lit103'])
			time.sleep(PLC_PERIOD_SEC)


if __name__ == '__main__':
	lit103 = Lit103(name='lit103',state=STATE,protocol=LIT103_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
			

