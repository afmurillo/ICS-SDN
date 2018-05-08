"""
PLC 1
"""

from minicps.devices import PLC
from threading import Thread
from utils import *
from random import *

import json
import select
import socket
import time

MV101 = ('MV101', 1)
LIT101 = ('LIT101', 1)
P101 = ('P101', 1)

LIT301 = ('LIT301', 3)

SENSOR_ADDR = IP['lit101']
IDS_ADDR = IP['ids101']


# TODO: real value tag where to read/write flow sensor

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
		self.xhat[2] = lit103
	
            except KeyboardInterrupt:
 	        print "\nCtrl+C was hitten, stopping server"
                client.close()
        	break


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

class HMISocket(Thread):
    """ Class that responds to the POLL command from HMI """
    def __init__(self, plc_object):
        Thread.__init__(self)
        self.plc = plc_object
        self.lit101 = 0.0

    def run(self):
        print "DEBUG entering socket thread run"
        self.sock = socket.socket()
        self.sock.connect((IP['HMI'], int(PORTS['hmi_poll_port'])))
        data = ''
        while True:
            while data=='':
                data = self.sock.recv(100)
                time.sleep(1)
                if data == "POLL":
                    self.sock.send("LIT101: "+str(self.lit101))
                data = ''
    def setLit101(self, val):
        self.lit101 = val

class IdsSocket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, plc_object):        
        Thread.__init__(self)
        self.plc = plc_object

    def run(self):
        print "DEBUG entering socket thread run"
        self.sock = socket.socket()     # Create a socket object    
        self.sock.bind((IP['plc101'] , 4234 ))
        self.sock.listen(5)

        while (self.plc.count <= PLC_SAMPLES):
            try:
	        client, addr = self.sock.accept()
		data = client.recv(4096)                                                # Get data from the client         

		#lit101 = float(self.plc.recieve(LIT101, IDS_ADDR))
	        message_dict = eval(json.loads(data))
	        lit101 = float(message_dict['Variable'])
		print "received from IDS!", lit101

            
	        #print 'DEBUG plc1 lit101: %.5f' % lit101

	        if lit101 >= LIT_101_M['HH'] :
	            #self.plc.send(MV101, 0, IP['plc101'])
               	    mv = 0

	        elif lit101 >= LIT_101_M['H']:
	            #self.plc.send(MV101, 0, IP['plc101'])
                    mv = 0

	        elif lit101 <= LIT_101_M['L']:
	            #self.plc.send(MV101, 1, IP['plc101'])
                    mv = 1

	        elif lit101 <= LIT_101_M['LL']:
	            #self.plc.send(MV101, 1, IP['plc101'])                
                    mv = 1

                self.send_message(IP['mv101'], 9587, mv)
       	    except KeyboardInterrupt:
	    	print "\nCtrl+C was hitten, stopping server"
	        client.close()
		break

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

class PLC101(PLC):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s1 plc1 enters pre_loop'
	
	# Controller Initial Conditions	
	self.xhat = [0; 0; 0];
	self.prev_inc_i = [0; 0];
	self.w1 = [0; 0; 0];
	self.w2 = [0; 0; 0];
	self.prev_ya = [0; 0];
	self.u_min = [-4e-5; -4e-5];
	self.u_max = [5e-5; 5e-5];
	#self.x_min = zeros(3,1) - [Y10; Y20; Y30];
	self.x_max = 0.62*ones(3,1) - [Y10; Y20; Y30]
	self.z = [0; 0];
	current_inc_i = -[K1, K2] * [self.xhat; self.z]
	#n_a = 5e-6*randn(2,2001);
	
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
        backup = IdsSocket(self)
	backup.start()
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

        while(self.count <= PLC_SAMPLES):

            # lit101 [meters]
	    try:
	    	lit101 = float(self.receive(LIT101, SENSOR_ADDR))
	        #print 'DEBUG plc1 lit101: %.5f' % lit101
		print "plc1 lit101", lit101
		
		#xhat is the vector used for the controller. In the next version, xhat shouldn't be read from sensors, but from luerenberg observer
		self.xhat[0]= lit101
		self.xhat[1]= float(self.get(LIT102))
		
		self.current_inc_i = -[K1, K2] * [self.xhat; self.z]
		#self.current_inc_i = sat_vec(Current_inc_i, u_min, u_max);
		# Z(k+1) = z(k) + ref(k) - xhat(k)
		self.q1 = self.current_inc_i[0]
		self.q2 = self.current_inc_i[1]
		self.send(Q101, self.q1, IP['plc101'])
		self.send(Q102, self.q2, IP['plc101'])
					
                #hmi.setLit101(lit101)
	    except Exception as e:
                   print e
		   print "Switching to backup"
		   break


if __name__ == "__main__":

    plc101 = PLC101(name='plc101',state=STATE,protocol=PLC101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
