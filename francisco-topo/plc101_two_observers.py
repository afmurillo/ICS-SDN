""" PLC 1 """

from minicps.devices import PLC
from threading import Thread
from utils import *
from random import *


import json
from decimal import Decimal
import select
import socket
import time

Q101 = ('Q101', 1)
Q102 = ('Q102', 1)

LIT101 = ('LIT101', 1)
LIT102 = ('LIT102', 1)
LIT103 = ('LIT103', 1)

SENSOR_ADDR = IP['lit101']
IDS_ADDR = IP['ids101']
PLC_ADDR = IP['plc101']

#lit103 = Y30
#lit103_prev = Y30

class Lit101Socket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, plc_object):
        Thread.__init__(self)
        self.plc = plc_object

    def run(self):
        self.sock = socket.socket()     # Create a socket object
        self.sock.bind((IP['plc101'] , 8754 ))
        self.sock.listen(5)

        while (self.plc.count <= PLC_SAMPLES):
            try:
            	client, addr = self.sock.accept()
		data = client.recv(4096)                                                # Get data from the client
            	message_dict = eval(json.loads(data, parse_float=Decimal))
            	#message_dict = eval(json.loads(data))
	        self.plc.received_lit101 = float(message_dict['Variable'])
		self.plc.lit_rec_time = time.time()
            except KeyboardInterrupt:
 	        print "\nCtrl+C was hitten, stopping server"
                client.close()
        	break
        print "Socket closed"

class Lit102Socket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, plc_object):
        Thread.__init__(self)
        self.plc = plc_object

    def run(self):
        self.sock = socket.socket()     # Create a socket object
        self.sock.bind((IP['plc101'] , 8755 ))
        self.sock.listen(5)

        while (self.plc.count <= PLC_SAMPLES):
            try:
            	client, addr = self.sock.accept()
		data = client.recv(4096)                                                # Get data from the client
            	message_dict = eval(json.loads(data, parse_float=Decimal))
	        self.plc.received_lit102 = float(message_dict['Variable'])
            except KeyboardInterrupt:
 	        print "\nCtrl+C was hitten, stopping server"
                client.close()
        	break
        print "Socket closed"


class PLC101(PLC):

    def send_message(self, ipaddr, port, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ipaddr, port))

        msg_dict = dict.fromkeys(['Type', 'Variable'])
        msg_dict['Type'] = "Report"
        msg_dict['Variable'] = message
        message = json.dumps(str(msg_dict))

        try:
            ready_to_read, ready_to_write, in_error = select.select([sock, ], [sock, ], [], 5)
        except:
            print "Socket error"
            return
        if(ready_to_write > 0):
            sock.send(message)
        sock.close()

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


    def pre_loop(self, sleep=0.1):
	# Controller Initial Conditions
        self.count = 0


	self.received_lit101 = 0.4
	self.lit101 = 0.0
	self.lit102 = 0.0
	lit103 = 0.0

	self.q1 = 0.0
	self.q2 = 0.0

	self.z =  np.array([[0.0],[0.0]])

        self.xhat =  np.array([[0.0],[0.0],[0.0]])
        self.w1 =  np.array([[0.0],[0.0],[0.0]])
        self.w2 =  np.array([[0.0],[0.0],[0.0]])

	self.K1K2 = np.concatenate((K1,K2),axis=1)
	self.prev_inc_i = np.array([[0.0],[0.0]])
        self.ym=np.array([[0.0],[0.0]])
	self.ya=np.array([[0.0],[0.0]])
	self.yr=np.array([[0.0],[0.0]])
        self.prev_ya=np.array([[0.0],[0.0]])

	self.xmin = [-0.4, -0.2, -0.3]
	self.xmax = [0.22, 0.42, 0.32]

	self.umin = [-4e-5, -4e-5]
	self.umax = [5e-5, 5e-5]

	self.prod_1 = Aobsv-(np.matmul(np.matmul(Gobsv,Cobsv),Aobsv))
	self.prod_2 = Bobsv-(np.matmul(np.matmul(Gobsv,Cobsv),Bobsv))

	self.prod_3 = np.matmul(T1,B)
	self.prod_4 = np.matmul(T2,B)

	self.tim_uio_1 = 0
	self.tim_uio_2 = 0
	#self.th_uio_on = 0.003*2
	self.th_uio_on = 0.0015

	self.bad_lit_flag = 0
	self.defense = 0.0

    def main_loop(self):
        """plc1 main loop.
            - reads sensors value
            - drives actuators according to the control strategy
            - updates its enip server
        """
        lit101socket = Lit101Socket(self)
        lit101socket.start()

        lit102socket = Lit102Socket(self)
        lit102socket.start()

	begin = time.time()
	#print " %Begin ",         begin
	while_begin = 0.0
	self.lit_rec_time =0.0
	control_time = 0.0
	act_send_time = 0.0
	time_btw_cycles = 0.0


        while(self.count <= PLC_SAMPLES):
	    try:

		time_btw_cycles = time.time()
		self.change_references()

                self.lit101 = self.received_lit101 - Y10
		self.lit102 = float(self.get(LIT102)) - Y20
		lit103 =  float(self.get(LIT103)) - Y30

                self.ym[0,0]=self.lit101
                self.ym[1,0]=self.lit102

                #self.xhat = np.matmul((Aobsv-(np.matmul(np.matmul(Gobsv,Cobsv),Aobsv))),self.xhat) + np.matmul((Bobsv-(np.matmul(np.matmul(Gobsv,Cobsv),Bobsv))),self.prev_inc_i) + np.matmul(Gobsv,self.ya)

	    	self.ya[0,0]=self.ym[0,0]
		self.ya[1,0]=self.ym[1,0]

		self.w1 = np.matmul(F1, self.w1) + np.matmul(self.prod_3,self.prev_inc_i) + Ksp1*self.prev_ya[1,0]
		self.zhat_uio1 = self.w1 + Hsp1*self.ya[1,0]
		self.ruio1 = self.ya - np.matmul(Cobsv,self.zhat_uio1 )

		#print self.count, " ", self.ruio1[0]
		#print self.count, " ", self.ruio1.transpose()

		self.w2 = np.matmul(F2, self.w2) + np.matmul(self.prod_4,self.prev_inc_i) + Ksp2*self.prev_ya[0,0]
		self.zhat_uio2 = self.w2 + Hsp2*self.ya[0,0]
		self.ruio2 = self.ya - np.matmul(Cobsv,self.zhat_uio2 )

		print self.count, " ", self.ruio2.transpose()

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

	        self.xhat = np.matmul(self.prod_1,self.xhat) + np.matmul(self.prod_2,self.prev_inc_i) + np.matmul(Gobsv,self.ya)
		self.xhat=self.saturar_xhat(self.xhat)
		self.xhatz=np.concatenate((self.xhat,self.z), axis=0)

		self.current_inc_i = np.matmul(-self.K1K2,self.xhatz)
		self.current_inc_i = self.saturar_inc(self.current_inc_i)

                self.prev_inc_i = self.current_inc_i
		self.prev_ya = self.ya

		# Aca hay que calcular el error de L1, L2 (self.lit101' y self.lit102')
		self.lit101_error = self.ref_y0 - self.yr[0,0] - Y10
		self.lit102_error = self.ref_y1 - self.yr[1,0] - Y20

		# Z(k+1) = z(k) + error(k)
		self.z[0,0] = self.z[0,0] + self.lit101_error
		self.z[1,0] = self.z[1,0] + self.lit102_error

		self.q1 = Q1 + self.current_inc_i[0]
		self.q2 = Q2 + self.current_inc_i[1]

		#self.set(Q101, float(self.q1))
		#self.set(Q102, float(self.q2))

		control_time = time.time() - time_btw_cycles

                self.send_message(IP['q101'], 7842 ,float(self.q1))
                self.send_message(IP['q102'], 7842 ,float(self.q2))

		act_send_time = time.time() - control_time

		self.count = self.count + 1

		#print "% control ", control_time
		#print "% act send ", act_send_time
		#print "% btw ", time_btw_cycles
		#print "% lit rec ", self.lit_rec_time

		time.sleep(PLC_PERIOD_SEC)

	    except Exception as e:
                   print e
		   print "Switching to backup"
		   break


if __name__ == "__main__":

    plc101 = PLC101(name='plc101',state=STATE,protocol=PLC101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
