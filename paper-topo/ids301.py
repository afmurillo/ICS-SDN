from minicps.devices import PLC
from utils import *

from threading import Thread

import sys
import time
import socket
import json
import select

SENSOR_ADDR = IP['lit301']
#PLC101_ADDR = IP['plc101']
PLC101_ADDR = IP['plc101-HMI']
IDS_ADDR = IP['ids101']
LIT301_ADDR = IP['lit301']

P301 = ('P301', 3)
LIT301 = ('LIT301', 3)

class Ids101(PLC):

	def switch_component(self, controller_ip, controller_port, component):
		print "Connecting to ONOS"
	        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	        sock.connect((controller_ip, int(controller_port)))
	        msg_dict = dict.fromkeys(['Type', 'Variable'])
	        msg_dict['Type'] = "Command"		
	        msg_dict['Variable'] = component
	        message = json.dumps(str(msg_dict))
	        try:
	            ready_to_read, ready_to_write, in_error = select.select([sock, ], [sock, ], [], 5)
	        except socket.error, exc:
	            print "Socket error"
		    print exc
	            return
	        if(ready_to_write > 0):
	            sock.send(message)
	        sock.close()

	def calculate_controls(self, variable):
 	    print "calculate action control"
	    estimated = 1

            if variable >= LIT_301_M['HH'] :
	        estimated = 0
            elif variable >= LIT_301_M['H'] :
		estimated = 0
            elif variable <= LIT_301_M['L']:
		estimated = 1
            elif variable <= LIT_301_M['LL']:
		estimated = 1

	    if variable > LIT_301_M['L'] and variable < LIT_301_M['H']:
		if self.filling:
			estimated = 1
		else:
			estimated = 0
	
 	    return estimated

	def pre_loop(self, sleep=0.1):

		# Estimated values
		self.section = TANK_SECTION
		print "DEBUG: in pre_loop"
		time.sleep(sleep)

	def main_loop(self):
		print "main loop"
		count = 0
		self.received_level = 0.0
		self.previous_level = 0.0

		# The values are for a 0.2 period, we calculate every 1.0 period
		inflow = float( (PUMP_FLOWRATE_IN * PP_PERIOD_HOURS * 2 )  / self.section )
		outflow = float( (PUMP_FLOWRATE_OUT_2 * PP_PERIOD_HOURS * 2  ) / self.section )

		self.controller_port = PORTS['controller_ids_port']
		self.controller_ip = IP['controller']
		self.threshold = 0.1
		self.plc_intrusion = False	
		self.plc_count = 0
		self.filling = False
		self.wait_time = PLC_PERIOD_SEC

		#print "Connecting to controller"		

		print "Entering while"
		#self.send_message(IP['plc101'], 4234, 0)

		while(count <= PP_SAMPLES):	

		    # IDS needs to:
		    # Detect compromised PLC
		    # If plc is compromised needs to:
		    #  1. Keep sendind data to the PLC101
		    #  2. Calculate and send control action to P301

		    try:
			self.received_level = float(self.receive(LIT301, SENSOR_ADDR))
			print "Received LIT301", self.received_level
		    except:
			continue

		    if self.plc_intrusion == False:
			p301 = int(self.get(P301))
			if self.received_level > self.previous_level:
			    self.filling = True
		        else:
			    self.filling = False

			self.estimated_p301 = self.calculate_controls(self.received_level)
			   
			if p301 != self.estimated_p301:
			    if count > 5:
			        self.plc_count += 1		    
				if self.plc_count >= 3:
				    self.plc_intrusion = True
				    print "Received P301 ", p301
				    print "Estimated P301 ", self.estimated_p301
				    print "Filling ", self.filling
				    print "@@@ PLC INTRUSION!!! @@@@"
				    self.switch_component(self.controller_ip, self.controller_port, "Switch_plc")
			    else:
				self.plc_count = 0 
			    
		    	#x(t) = x(t+1)
		    	self.previous_level = self.received_level

		    else:
			self.send_message(PLC101_ADDR, 8754, self.received_level)
			print "Sending level to PLC101", self.received_level
	            	if self.received_level >= LIT_301_M['HH'] :	            
	                    p301 = 1
	                elif self.received_level >= LIT_301_M['H']:
	                    p301 = 1
	                elif self.received_level <= LIT_301_M['LL']:
	                    p301 = 0
	            	elif self.received_level <= LIT_301_M['L']:
	            	    p301 = 0
	                	            
			print "Sending to P301", p301
	            	self.send_message(IP['p301'], 6568, p301)

	            count += 1		
        	    time.sleep(self.wait_time)					

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

if __name__ == '__main__':
	ids101 = Ids101(name='ids101',state=STATE,protocol=IDS101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
