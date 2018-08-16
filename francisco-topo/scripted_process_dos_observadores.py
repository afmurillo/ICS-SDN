from minicps.devices import Tank
from scipy.integrate import odeint
from utils import *
import numpy as np
import sys
import time
import math
import logging

class TankControl():

        def saturar_xhat(self, valores):

            for i in range(len(valores)):
                if valores[i] > self.xmax[i]:
                    valores[i] = self.xmax[i]

                if  valores[i] < self.xmin[i]:
                    valores[i] = self.xmin[i]

            return valores

        def saturar_inc(self, valores):
            for i in range(len(valores)):
                if valores[i] > self.xmax[i]:
                    valores[i] = self.xmax[i]

                if  valores[i] < self.xmin[i]:
                    valores[i] = self.xmin[i]

            return valores



	def init(self):

		self.stoptime = 1
		self.numpoints = 100
		self.t = [self.stoptime * float(i) / (self.numpoints - 1) for i in range(self.numpoints)]

		self.count = 0

		self.abserr = 1.0e-8
		self.relerr = 1.0e-6

		# PLC values
		self.ref_y0 = Y10
   	        self.ref_y1 = Y20

	        self.delta_q1 = 0.0
		self.delta_q2 = 0.0

		self.q1 = Q1 + self.delta_q1
		self.q2 = Q2 + self.delta_q2

		self.lit101_error = 0.0
		self.lit102_error = 0.0

		self.diff_lit101 = 0.0
		self.lit101_prev = Y10

		self.diff_lit102 = 0.0
		self.lit102_prev = Y20

		self.diff_lit103 = 0.0
		self.lit103_prev = Y30

		self.z =  np.array([[0.0],[0.0]], )
		self.current_inc_i = np.array([[0.0],[0.0]])
		self.K1K2 = np.concatenate((K1,K2),axis=1)

		self.script_time = 0.01

		self.xhat =  np.array([[0.0],[0.0],[0.0]])
	        self.w1 =  np.array([[0.0],[0.0],[0.0]])
	        self.w2 =  np.array([[0.0],[0.0],[0.0]])

		self.prev_inc_i = np.array([[0.0],[0.0]])
		self.ym=np.array([[0.0],[0.0]])
		self.ya=np.array([[0.0],[0.0]])
		self.yr=np.array([[0.0],[0.0]])
	        self.prev_ya=np.array([[0.0],[0.0]])

		self.xmin = [-0.4, -0.2, -0.3]
		self.xmax = [0.22, 0.42, 0.32]

		self.umin = [-4e-5, -4e-5]
		self.umax = [5e-5, 5e-5]

		self.prod_3 = np.matmul(T1,B)
		self.prod_4 = np.matmul(T2,B)

		self.tim_uio_1 = 0
		self.tim_uio_2 = 0
		self.th_uio_on = 0.003*2

		self.defense = 1.0


	def plant_model(self, l, t, q):
		MQ1, MQ2 = q
		L1, L2, L3 = l

		# System of 3 differential equations of the water tanks
	        f = [(MQ1 - mu13*sn*np.sign(L1-L3)*math.sqrt(2*g*abs(L1-L3)))/s,
		        (MQ2 + mu32*sn*np.sign(L3-L2)*math.sqrt(2*g*abs(L3-L2)) - mu20*sn*math.sqrt(2*g*L2))/s,
     		        (mu13*sn*np.sign(L1-L3)*math.sqrt(2*g*abs(L1-L3)) - mu32*sn*np.sign(L3-L2)*math.sqrt(abs(2*g*abs(L3-L2))))/s
	    	]

	  	return f



        def simulate_plant(self):
		# These vectors are used by the model
		q = [self.q1, self.q2]
		l = [self.lit101, self.lit102, self.lit103]

		wsol = odeint(self.plant_model, l, self.t, args=(q,),atol=self.abserr, rtol=self.relerr)

		if (wsol[-1][0]) > 1.0:
			wsol[-1][0] = 1.0
                if (wsol[-1][1]) > 1.0:
                        wsol[-1][1] = 1.0
                if (wsol[-1][2]) > 1.0:
                        wsol[-1][2] = 1.0

		l=[wsol[-1][0], wsol[-1][1], wsol[-1][2]]


		print self.count, " ", l

		return l

        def change_references(self):

		if self.count <= 50:
			self.ref_y0 = 0.4
		if self.count > 50 and self.count <= 350:
			self.ref_y0 = 0.450
		if self.count > 350:
			self.ref_y0 = 0.4

                if self.count <= 70:
                        self.ref_y1 = 0.2
                if self.count > 70 and self.count <= 400:
                  	self.ref_y1 = 0.225
                if self.count > 400:
              	        self.ref_y1 = 0.2

        def simulate_plc(self):

   	        #self.diff_lit101 = self.lit101 - self.lit101_prev
   	        self.diff_lit101 = self.lit101 - Y10
		self.lit101_prev = self.lit101

		#self.diff_lit102 = self.lit102 - self.lit102_prev
		self.diff_lit102 = self.lit102 - Y20
		self.lit102_prev = self.lit102

		#self.diff_lit103 = self.lit103 - self.lit103_prev
		self.diff_lit103 = self.lit103 - Y30
		self.lit103_prev = self.lit103

		# Asignamos ym
                self.ym[0,0]=self.diff_lit101
                self.ym[1,0]=self.diff_lit102

		
		#if self.count >=  self.attack_time_begin and self.count <= self.attack_time_end:
		#if self.bad_lit_flag == 1:
		#self.diff_lit101 = self.diff_lit101 + self.diff_attack_value

		self.ya[0,0]=self.ym[0,0]
		self.ya[1,0]=self.ym[1,0]

		if self.count >=  self.attack_time_begin and self.count <= self.attack_time_end:
			if self.bad_lit_flag == 1:
				#self.diff_lit101 = self.diff_lit101 + self.diff_attack_value
				self.ya[1,0] = self.ym[1,0] + self.diff_attack_value
			elif self.bad_lit_flag == 2:
				self.ya[1,0] = self.abs_attack_value
			
		# Two observers
		self.w1 = np.matmul(F1, self.w1) + np.matmul(self.prod_3,self.prev_inc_i) + Ksp1*self.prev_ya[1,0]
		self.zhat_uio1 = self.w1 + Hsp1*self.ya[1,0]

		self.ruio1 = self.ya - np.matmul(Cobsv,self.zhat_uio1 )		
		#print self.count, " ", self.ruio1.transpose()

		self.w2 = np.matmul(F2, self.w2) + np.matmul(self.prod_4,self.prev_inc_i) + Ksp2*self.prev_ya[0,0]
		self.zhat_uio2 = self.w2 + Hsp2*self.ya[0,0]	

		self.ruio2 = self.ya - np.matmul(Cobsv,self.zhat_uio2 )		
		#print self.count, " ", self.ruio2.transpose()

		if abs(self.ruio1[0]) >= self.th_uio_on:
			self.tim_uio_1 = 1
		else:
			self.tim_uio_1 = 0

		if abs(self.ruio2[1]) >= self.th_uio_on:
			self.tim_uio_2 = 1
		else:
			self.tim_uio_2 = 0

		#print self.count, " ", self.tim_uio_1
		#print self.count, " ", self.tim_uio_2

		self.v1 = np.matmul(Cobsv[0],(self.zhat_uio1-self.zhat_uio2))*self.tim_uio_1
		#print  self.count, " ", self.v1

		self.v2 = np.matmul(Cobsv[1],(self.zhat_uio2-self.zhat_uio1))*self.tim_uio_2
		#print  self.count, " ", self.v2

		self.v_total=np.array([[self.v1[0]],[self.v2[0]]])	
		#print self.count, " ", self.v_total.transpose()

		self.yr = self.ya + self.defense*self.v_total
		#self.yr = self.ya

		# xhat should be xhat(t) = xhat(t) - xhat(-1)
		self.xhat = np.matmul((Aobsv-(np.matmul(np.matmul(Gobsv,Cobsv),Aobsv))),self.xhat) + np.matmul((Bobsv-(np.matmul(np.matmul(Gobsv,Cobsv),Bobsv))),self.prev_inc_i) + np.matmul(Gobsv,self.ya)
		self.xhat = self.saturar_xhat(self.xhat)

		self.xhatz=np.concatenate((self.xhat,self.z), axis=0)


		self.current_inc_i = np.matmul(-self.K1K2,self.xhatz)
                self.current_inc_i = self.saturar_inc(self.current_inc_i)

		self.prev_inc_i = self.current_inc_i
		self.prev_ya = self.ya

		# Aca hay que calcular el error de L1, L2 (self.lit101' y self.lit102')
		self.lit101_error = self.ref_y0 - self.yr[0,0] - Y10
		self.lit102_error = self.ref_y1 - self.yr[1,0] - Y20
		#print "Error: ", self.lit101_error, " ", self.lit102_error


		# Z(k+1) = z(k) + error(k)
		self.z[0,0] = self.z[0,0] + self.lit101_error
		self.z[1,0] = self.z[1,0] + self.lit102_error


		return self.current_inc_i


        def main(self):

		self.lit101= Y10
		self.lit102 = Y20
		self.lit103 = Y30


		x = []
		u = []

		# 0 = No attack present
		# 1 = Differential attack 
		# 2 = Absolute attack

		self.bad_lit_flag = 1
 	 	self.diff_attack_value = -0.02
		self.abs_attack_value = -0.01
		self.attack_time_begin = 200
		self.attack_time_end = 300

		while(self.count <= PP_SAMPLES):
			# Variable real
			x=self.simulate_plant()

			# Variable que entrega el sensor
			self.lit101 = x[0]
			self.lit102 = x[1]
			self.lit103 = x[2]
			
			self.change_references()
			u=self.simulate_plc()

			self.delta_q1 = u[0]
			self.delta_q2 = u[1]

			#self.q1 = self.q1 + self.delta_q1
			#self.q2 = self.q2 + self.delta_q2

			self.q1 = Q1 + self.delta_q1
			self.q2 = Q2 + self.delta_q2

			#print "Sending to actuators: ", " ", self.q1, " ", self.q2

			self.count += 1
			if (self.count >= 2000):
				break

			#print "----"
			time.sleep(self.script_time)

if __name__ == '__main__':
	tank = TankControl()
	tank.init()
	tank.main()
