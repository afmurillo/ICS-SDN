from minicps.devices import Tank
from utils import *
from numpy import *
import sys
import time
import math
import logging

class RawWaterTank(Tank):
	def pre_loop(self):
		logging.basicConfig(filename="plant.log", level=logging.DEBUG)
		logging.debug('plant enters pre_loop')
		self.L1= 0.4
		self.L2=0.2
		self.L3=0.3

		self.Q1 = Q1
		self.Q2 = Q2

		self.q13 = 0
		self.q32 = 0
		self.q20 = 0

	def main_loop(self):
		count = 0
		logging.debug('starting simulation')
		while(count <= PP_SAMPLES):

			Q1 = mu13*sn*math.sqrt(2*g*(Y10-Y30));
			Q2 = mu20*sn*math.sqrt(2*g*Y20)-mu32*sn*math.sqrt(2*g*(Y30-Y20));

			self.L1 = self.Q1 - self.q13
			self.L2 = self.Q2 + self.q32 - self.q20
			self.L3 = self.q13 - self.q32

			self.q13 = u13*sn*sign(self.L1-self.L3)*math.sqrt(2*g*(self.L1-self.L3))
			print "q13", self.q13

			print "L3", self.L3
			print "L2", self.L2
			print "u32", u32
			print "sn", sn 

			# Por que L2 es menor que L3?
			self.q32=u32*sn*sign(self.L3-self.L2)*math.sqrt(abs(2*g*(self.L3-self.L2)))
			print "q32", self.q32

			self.q20 = u20*sn*math.sqrt(2*g*self.L2)
			print "q20", self.q20
		
			logging.debug('L1: %s', self.L1)
			logging.debug('L2: %s', self.L2)
			logging.debug('L3: %s', self.L3)

			count += 1
			time.sleep(PP_PERIOD_SEC)

if __name__ == '__main__':
	rwt = RawWaterTank(
		name='rwt',
		state=STATE,
		protocol=None,
		section=TANK_SECTION,
		level=RWT_INIT_LEVEL
	)
