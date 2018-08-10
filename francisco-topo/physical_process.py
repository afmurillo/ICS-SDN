from minicps.devices import Tank
from minicps.devices import PLC
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
PLC_ADDR = IP['plc101']

class RawWaterTank(PLC):

	def plant_model(self, l, t, q):
  		MQ1, MQ2 = q
		L1, L2, L3 = l

		# System of 3 differential equations of the water tanks
                f = [(MQ1 - mu13*sn*np.sign(L1-L3)*math.sqrt(2*g*abs(L1-L3)))/s,
                (MQ2 + mu32*sn*np.sign(L3-L2)*math.sqrt(2*g*abs(L3-L2)) - mu20*sn*math.sqrt(2*g*L2))/s,
                (mu13*sn*np.sign(L1-L3)*math.sqrt(2*g*abs(L1-L3)) - mu32*sn*np.sign(L3-L2)*math.sqrt(abs(2*g*abs(L3-L2))))/s
                ]

	  	return f

	def pre_loop(self):
		logging.basicConfig(filename="plant.log", level=logging.DEBUG)
		logging.debug('plant enters pre_loop')
		self.Y1= 0.4
		self.Y2=0.2
		self.Y3=0.3

		self.set(LIT101, self.Y1)
		self.set(LIT102, self.Y2)
		self.set(LIT103, self.Y3)

		self.Q1 = Q1
		self.Q2 = Q2

		self.set(Q101, self.Q1)
		self.set(Q102, self.Q2)

		# These vectors are used by the model
		self.l = [self.Y1, self.Y2, self.Y3]
		self.abserr = 1.0e-8
		self.relerr = 1.0e-6
		self.lock = 0.0

	def main_loop(self):
		count = 0
		#logging.debug('starting simulation')
		#logging.debug('Initial values: L1: ', self.l[0], ' L2: ', self.l[1], ' L3: ', self.l[2])
		stoptime = 1
		numpoints = 100
		t = [stoptime * float(i) / (numpoints - 1) for i in range(numpoints)]

		while(count <= PP_SAMPLES):
			print count, " ", self.l
			self.Q1 = float(self.get(Q101))
			self.Q2 = float(self.get(Q102))
			self.q = [self.Q1, self.Q2]
			wsol = odeint(self.plant_model, self.l, t, args=(self.q,),atol=self.abserr, rtol=self.relerr)

			#print "dl/dt ", wsol

			if (wsol[-1][0]) > 1.0:
				wsol[-1][0] = 1.0

                        if (wsol[-1][1]) > 1.0:
                                wsol[-1][1] = 1.0

                        if (wsol[-1][2]) > 1.0:
                                wsol[-1][2] = 1.0

			self.l=[wsol[-1][0], wsol[-1][1], wsol[-1][2]]

			#Update the values in the database
			self.set(LIT101, self.l[0])
			self.set(LIT102, self.l[1])
			self.set(LIT103, self.l[2])
			count += 1
			#self.lock = float(self.receive(LIT101, PLC_ADDR))
			time.sleep(PLC_PERIOD_SEC)

if __name__ == '__main__':
	plc101 = RawWaterTank(name='plant101',state=STATE,protocol=TANK_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
