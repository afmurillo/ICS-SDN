from minicps.devices import Tank
from utils import *

import sys
import time

FIT201 = ('FIT201', 2)
PH201 = ('PH201', 2)
P201 = ('P201', 2)

class RawWaterTank(Tank):
	def pre_loop(self):
		self.ph_level = self.set(PH201, 0.7)
		self.set(P201, 0)

	def main_loop(self):
		count = 0
		while(count <= PP_SAMPLES):

			p201 = float(self.get(P201))
			if  int(p201) == 1:
				phup = PH_PUMP_FLOWRATE_IN * PH_PERIOD_HOURS
				self.ph_level += phup
			else:
				phdown = PH_PUMP_FLOWRATE_OUT * PH_PERIOD_HOURS
				self.ph_level -= phdown

			new_ph201 = self.set(PH201, self.ph_level)

			self.ph_level = new_ph201

			print "DEBUG  PH Level %.5f " % new_ph201
		
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
