""" PLC 1 """

from minicps.devices import PLC
from threading import Thread
from utils import *
from random import *

import json
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

#lit103 = Y30
#lit103_prev = Y30

class Lit301Socket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, plc_object):
        Thread.__init__(self)
        self.plc = plc_object

    def run(self):
        #print "DEBUG entering socket thread run"
        self.sock = socket.socket()     # Create a socket object
        self.sock.bind((IP['plc101'] , 8754 ))
        self.sock.listen(5)

        while (self.plc.count <= PLC_SAMPLES):
            try:
            	client, addr = self.sock.accept()
		data = client.recv(4096)                                                # Get data from the client
            	message_dict = eval(json.loads(data))
	        lit103 = float(message_dict['Variable']) - lit103_prev
		lit103_prev = lit103

	        #print "received from LIT103!", lit103

            except KeyboardInterrupt:
 	        print "\nCtrl+C was hitten, stopping server"
                client.close()
        	break

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
            if self.count > 50 and self.count <= 150:
                    self.ref_y0 = 0.450
            if self.count > 150:
                    self.ref_y0 = 0.4

            if self.count <= 70:
                    self.ref_y1 = 0.2
            if self.count > 70 and self.count <= 200:
                    self.ref_y1 = 0.225
            if self.count > 200:
                    self.ref_y1 = 0.2

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s1 plc1 enters pre_loop'
	# Controller Initial Conditions
        self.count = 0

        self.ref_y0 = Y10
        self.ref_y1 = Y20

	self.lit101 = 0.0
	self.lit102 = 0.0
	lit103 = 0.0

	self.q1 = 0.0
	self.q2 = 0.0

	self.received_lit101 = 0.0
	self.received_lit102 = 0.0
	received_lit103 = 0.0

	self.z =  np.array([[0.0],[0.0]])
        self.xhat =  np.array([[0.0],[0.0],[0.0]])
        self.xhat_2 =  np.array([[0.0],[0.0],[0.0]])
	self.K1K2 = np.concatenate((K1,K2),axis=1)
	self.prev_inc_i = np.array([[0.0],[0.0]])
        self.ya=np.array([[0.0],[0.0]])

    def main_loop(self):
        """plc1 main loop.
            - reads sensors value
            - drives actuators according to the control strategy
            - updates its enip server
        """

        print 'DEBUG: swat-s1 plc1 enters main_loop.'

        while(self.count <= PLC_SAMPLES):
	    try:

		self.change_references()
		print "Count: ", self.count, "ref_y0: ", self.ref_y0
		self.received_lit101 = float(self.receive(LIT101, SENSOR_ADDR))
	    	self.lit101 = self.received_lit101 - Y10

		#xhat is the vector used for the controller. In the next version, xhat shouldn't be read from sensors, but from luerenberg observer
		self.received_lit102 = float(self.get(LIT102))
		self.lit102 = self.received_lit102 - Y20

		received_lit103 = float(self.get(LIT103))
		lit103 = received_lit103 - Y30

		# Aca hay que calcular el error de L1, L2 (self.lit101' y self.lit102')
		self.lit101_error = self.ref_y0 - self.received_lit101
		self.lit102_error = self.ref_y1 - self.received_lit102
		#print "Error: ", self.lit101_error, " ", self.lit102_error

		# Z(k+1) = z(k) + error(k)
		self.z[0,0] = self.z[0,0] + self.lit101_error
		self.z[1,0] = self.z[1,0] + self.lit102_error

                self.ya[0,0]=self.lit101
                self.ya[1,0]=self.lit102
		#Xhat with attack
                self.xhat_2 = np.matmul(Aobsv-np.matmul(np.matmul(Gobsv,Cobsv),Aobsv),self.xhat_2) + np.matmul(Bobsv-np.matmul(np.matmul(Gobsv,Cobsv),Bobsv),self.prev_inc_i) + np.matmul(Gobsv,self.ya)

                # Xhat used without attack
		self.xhat= np.array([[self.lit101],[self.lit102],[lit103]])
		#print "Calculado xhat"
		print self.count, self.xhat[0], self.xhat[1], self.xhat[2]
		#print self.z
		self.xhatz=np.concatenate((self.xhat,self.z), axis=0)
		#print "xhatz: ", self.xhatz

		#print "Concatenado"

		self.current_inc_i = np.matmul(-self.K1K2,self.xhatz)
                self.prev_inc_i = self.current_inc_i

		self.q1 = Q1 + self.current_inc_i[0]
		self.q2 = Q2 + self.current_inc_i[1]
		#print "Cumulative inc: ", " ", self.current_inc_i[0], " ", self.current_inc_i[1]
		#print "Sending to actuators: ", " ", self.q1, " ", self.q2

		#self.set(Q101, float(self.q1))
		#self.set(Q102, float(self.q2))
                self.send_message(IP['q101'], 7842 ,float(self.q1))
                self.send_message(IP['q102'], 7842 ,float(self.q2))

		#print "plc1 q101", self.q1
		#print "plc1 q102", self.q2



		self.count += 1
		time.sleep(PLC_PERIOD_SEC)

		# Nos hace falta definir antes del loop el vector con los valores de referencia (numpy.zeros inicializa un arreglo con 0 del tamano deseado)

	    except Exception as e:
                   print e
		   print "Switching to backup"
		   break


if __name__ == "__main__":

    plc101 = PLC101(name='plc101',state=STATE,protocol=PLC101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
