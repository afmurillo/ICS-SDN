from minicps.devices import Tank
from utils import *

import sys
import time
import logging

MV101 = ('MV101', 1)
P101 = ('P101', 1)
LIT101 = ('LIT101', 1)

FIT201 = ('FIT201', 2)
PH201 = ('PH201', 2)
P201 = ('P201', 2)

LIT301 = ('LIT301', 3)
P301 = ('P301', 3)

class RawWaterTank(Tank):
	def pre_loop(self):
		self.set(MV101, 1)
		self.set(P101, 0)
		self.lit101 = self.set(LIT101, 0.4)

		self.ph_level = self.set(PH201, 0.7)
		self.set(P201, 0)

		self.set(P301, 1)
		self.lit301 = self.set(LIT301, 0.4)

	def main_loop(self):
		count = 0
		logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='replay_defense_short_attacks/plant.log')
		while(count <= PP_SAMPLES):

			# First tank
			new_lit_101 = float(self.get(LIT101))
			water_volume = self.section*new_lit_101

			mv101 = self.get(MV101)
			if int(mv101) == 1:
				inflow = PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
				water_volume += inflow
			else:
				inflow = 0

			# outflow volumes
			p101 = self.get(P101)
			if int(p101) == 1:
				outflow = PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
				water_volume -= outflow
				fit_201 = outflow
			else:
				outflow = 0
				fit_201 = 0

			self.set(FIT201, fit_201)
			new_lit_101 = water_volume / self.section

			if new_lit_101 <= 0.0:
				new_lit_101 = 0.0

			self.lit101 = self.set(LIT101, new_lit_101)

			# PH Second loop
			p201 = float(self.get(P201))
			if  int(p201) == 1:
				phup = PH_PUMP_FLOWRATE_IN * PH_PERIOD_HOURS
				self.ph_level += phup
			else:
				phdown = PH_PUMP_FLOWRATE_OUT * PH_PERIOD_HOURS
				self.ph_level -= phdown

			new_ph201 = self.set(PH201, self.ph_level)

			self.ph_level = new_ph201

			# Second tank - third loop
			new_lit_301 = float(self.get(LIT301))
			water_volume_2 = self.section*new_lit_301

			if int(p101) == 1:
				inflow_2 = PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
				water_volume_2 += inflow_2
			else:
				inflow_2 = 0

			p301 = self.get(P301)
			if int(p301) == 1:
				outflow_2 = PUMP_FLOWRATE_OUT_2 * PP_PERIOD_HOURS
				water_volume_2 -= outflow_2
			else:
				outflow_2 = 0

			new_lit_301 = water_volume_2 / self.section

			if new_lit_301 <= 0.0:
				new_lit_301 = 0.0

			self.lit301 = self.set(LIT301, new_lit_301)
			#print "Water ", new_lit_101, self.lit301
			logging.info('LIT101: %f, LIT301 %f', new_lit_101, self.lit301)
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
