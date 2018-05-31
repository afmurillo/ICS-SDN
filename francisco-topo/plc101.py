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
lit103 = 0


class Lit301Socket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, plc_object):
        Thread.__init__(self)
        self.plc = plc_object

    def run(self):
        print "DEBUG entering socket thread run"
        self.sock = socket.socket()     # Create a socket object
        self.sock.bind((IP['plc101'] , 8754 ))
        self.sock.listen(5)

        while (self.plc.count <= PLC_SAMPLES):
            try:
            	client, addr = self.sock.accept()
		data = client.recv(4096)                                                # Get data from the client
            	message_dict = eval(json.loads(data))
	        lit103 = float(message_dict['Variable'])

	        print "received from LIT103!", lit103

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

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s1 plc1 enters pre_loop'
	# Controller Initial Conditions
	self.z =  np.array([[0],[0]])
	self.current_inc_i = np.array([[0],[0]])
        time.sleep(sleep)

    def main_loop(self):
        """plc1 main loop.
            - reads sensors value
            - drives actuators according to the control strategy
            - updates its enip server
        """

        print 'DEBUG: swat-s1 plc1 enters main_loop.'

        lit301socket = Lit301Socket(self)
        lit301socket.start()
        self.count = 0
        #hmi = HMISocket(self)
        #hmi.start()

        # Only for random control experiment!
        random_control_experiment = 0
        random_control_active = 0
        random_counter = 0
        control_file = '/home/mininet/ICS-SDN/paper-topo/control_actions.txt'
        input_file = "/home/mininet/ICS-SDN/paper-topo/control_list.txt"

        out_file = open(control_file, 'w')
	in_file = open(input_file, 'r')

        ref_y0 = Y10
        ref_y1 = Y20

        while(self.count <= PLC_SAMPLES):
	    try:
		if self.count <= 200:
			ref_y0 = 0.4
		if self.count > 200 and self.count <= 1500:
			ref_y0 = 0.450
		if self.count > 1500:
			ref_y0 = 0.4

                if self.count <= 400:
                        ref_y1 = 0.2
                if self.count > 400 and self.count <= 1700:
                        ref_y1 = 0.225
                if self.count > 1700:
                        ref_y1 = 0.2

	    	self.lit101 = float(self.receive(LIT101, SENSOR_ADDR))
	        #print 'DEBUG plc1 lit101: %.5f' % lit101
		print "plc1 lit101", self.lit101

		#xhat is the vector used for the controller. In the next version, xhat shouldn't be read from sensors, but from luerenberg observer
		self.lit102 = float(self.get(LIT102))
		print "plc1 lit102", self.lit102
		print "plc1 lit103", lit103

		self.xhat= np.array([[self.lit101],[self.lit102],[lit103]])
		self.K1K2 = np.concatenate((K1,K2),axis=1)

		self.xhatz=np.concatenate((self.xhat,self.z), axis=0)
		self.current_inc_i = np.matmul(-self.K1K2,self.xhatz)
		#print "non cumulative control action: ", np.matmul(-self.K1K2,self.xhatz)
		#self.current_inc_i = self.current_inc_i + np.matmul(-self.K1K2,self.xhatz)

		if self.current_inc_i[0] > QMAX:
			self.current_inc_i[0] = QMAX

                if self.current_inc_i[1] > QMAX:
                        self.current_inc_i[1] = QMAX

		self.q1 = self.current_inc_i[0]
		self.q2 = self.current_inc_i[1]

                self.send_message(IP['q101'], 7842 ,float(self.q1))
                self.send_message(IP['q102'], 7842 ,float(self.q2))

		print "plc1 q101", self.q1
		print "plc1 q102", self.q2

		# Z(k+1) = z(k) + ref(k) - xhat(k)
		self.z[0,0] = self.z[0,0] + float(ref_y0) - self.lit101
		self.z[1,0] = self.z[1,0] + float(ref_y1) - self.lit102

		self.count = self.count + 1

	    except Exception as e:
                   print e
		   print "Switching to backup"
		   break


if __name__ == "__main__":

    plc101 = PLC101(name='plc101',state=STATE,protocol=PLC101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
