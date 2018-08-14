from minicps.devices import PLC
from utils import *

import time
import random
import threading

SENSOR_ADDR = IP['lit101']

LIT101 = ('LIT101', 1)

class Lit101(PLC):
	def pre_loop(self, sleep=0.1):
		print 'DEBUG: sensor enters pre_loop'
		time.sleep(sleep)

	def main_loop(self):
		print 'DEBUG: sensor enters main_loop'
		count = 0
		self.attack = 0
		while count<=PLC_SAMPLES:

			self.level = float(self.get(LIT101))
			print "Lit level", self.level

			if count> 200:
				self.attack = 1

			if self.attack:
				print "Attack!!"		
				#self.level = self.level - random.uniform(0, 0.3)				
				self.level = 0
				#self.level = self.level - ((0.001) * (count - 200))
			else:
				print "Regular"			
			
			print "Counter: ", count

			self.send(LIT101, self.level, SENSOR_ADDR)
			time.sleep(PLC_PERIOD_SEC)
			count = count + 1


if __name__ == '__main__':
	lit101 = Lit101(name='lit101',state=STATE,protocol=LIT101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
			

