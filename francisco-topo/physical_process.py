from minicps.devices import Tank
from scipy.integrate import odeint
from utils import *
import numpy as np
import sys
import time
import math
import logging


Q101 = ('Q101', 1)
Q102 = ('Q102', 1)
LIT101 = ('LIT101', 1)
LIT102 = ('LIT102', 1)
LIT103 = ('LIT103', 1)


class RawWaterTank(Tank):

	def plant_model(self, l, t, q):
  		Q1, Q2 = q
		L1, L2, L3 = l

		# System of 3 differential equations of the water tanks
  		f = [
                Q1 - u13*sn*np.sign(L1-L3)*math.sqrt(abs(2*g*(L1-L3))),
      		Q2 + u32*sn*np.sign(L3-L2)*math.sqrt(abs(2*g*(L3-L2)))  - u20*sn*math.sqrt(abs(2*g*L2)),
      		u13*sn*np.sign(L1-L3)*math.sqrt(abs(2*g*(L1-L3))) - u32*sn*np.sign(L3-L2)*math.sqrt(abs(2*g*(L3-L2)))
      		]

	  	return f

	def pre_loop(self):
		logging.basicConfig(filename="plant.log", level=logging.DEBUG)
		logging.debug('plant enters pre_loop')
		self.L1= 0.4
		self.L2=0.2
		self.L3=0.3
		self.Q1 = mu13*sn*math.sqrt(abs(2*g*(Y10-Y30)))
		self.Q2 = mu20*sn*math.sqrt(2*g*Y20)-mu32*sn*math.sqrt(abs(2*g*(Y30-Y20)))

		# Writes values in the database
		self.set(Q101, self.Q1)
		self.set(Q102, self.Q2)

		self.set(LIT101, self.L1)
		self.set(LIT102, self.L2)
		self.set(LIT103, self.L3)

		# These vectors are used by the model
		self.q = [self.Q1, self.Q2]
		self.l = [self.L1, self.L2, self.L3]

		self.abserr = 1.0e-8
		self.relerr = 1.0e-6

	def main_loop(self):
		count = 0
		logging.debug('starting simulation')
		t = np.linspace(start=0, stop=1, num=100)


		while(count <= PP_SAMPLES):
			self.Q1 = float(self.get(Q101))
			self.Q2 = float(self.get(Q102))
			self.q = [self.Q1, self.Q2]
			wsol = odeint(self.plant_model, self.l, t, args=(self.q,),atol=self.abserr, rtol=self.relerr)

			if (wsol[-1][0]) > 1.0:
				wsol[-1][0] = 1.0

                        if (wsol[-1][1]) > 1.0:
                                wsol[-1][1] = 1.0

                        if (wsol[-1][2]) > 1.0:
                                wsol[-1][2] = 1.0

			self.l=[wsol[-1][0], wsol[-1][1], wsol[-1][2]]

			print "Result at time", count, " ", self.l
			#Update the values in the database
			self.set(LIT101, self.l[0])
			self.set(LIT102, self.l[1])
			self.set(LIT103, self.l[2])
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

