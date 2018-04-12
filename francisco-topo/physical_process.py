from minicps.devices import Tank
from utils import *
from numpy import *
import sys
import time

class RawWaterTank(Tank):
	def pre_loop(self):
		L1= 0.4
		L2=0.2
		L3=0.3

	def main_loop(self):
		count = 0
		while(count <= PP_SAMPLES):

			# First tank
			L1 = Q1 - q13
			L2 = Q2 + q32 - q20
			L3 = q13 - q32

			q13 = u13*sn*sign(L1-L3)*math.sqrt(2*g*(L1-l3))
			q32=u32*sn*sign(L3-L2)*math.sqrt(2*g*(L3-L2))
			q20 = u20*sn*math.sqrt(2*g*L2)
		
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
#	rwt.pre_loop()
#	rwt.main_loop()
