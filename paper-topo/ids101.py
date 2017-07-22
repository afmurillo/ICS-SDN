from minicps.devices import PLC
from utils import *

from threading import Thread

import sys
import time
import socket
import json
import select

SENSOR_ADDR = IP['lit101']
PLC101_ADDR = IP['plc101']
IDS_ADDR = IP['ids101']
LIT301_ADDR = IP['lit301']

MV101 = ('MV101', 1)
P101 = ('P101', 1)
LIT101 = ('LIT101', 1)


class Ids101(PLC):

	def switch_sensor(self, controller_ip, controller_port):
		print "Connecting to ONOS"
	        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	        sock.connect((controller_ip, int(controller_port)))
	        msg_dict = dict.fromkeys(['Type', 'Variable'])
	        msg_dict['Type'] = "Command"
	        msg_dict['Variable'] = "Switch_flow"
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
            if variable >= LIT_101_M['HH'] :
		self.estimated_p101 = 1
		self.estimated_mv101 = 0

            elif variable >= LIT_101_M['H']:
		self.estimated_p101 = 1
		self.estimated_mv101 = 0

            elif variable <= LIT_101_M['L']:
		self.estimated_p101 = 0
		self.estimated_mv101 = 1

            elif variable <= LIT_101_M['LL']:
		self.estimated_p101 = 0
		self.estimated_mv101 = 1

	def pre_loop(self, sleep=0.1):

		# Estimated values
		self.section = TANK_SECTION
		print "DEBUG: in pre_loop"
		time.sleep(sleep)

	def main_loop(self):
		print "main loop"
		count = 0
		self.received_level = 0.0
		self.estimated_level = 0.0

		# The values are for a 0.2 period, we calculate every 1.0 period
		inflow = float( (PUMP_FLOWRATE_IN * PP_PERIOD_HOURS * 2 )  / self.section )
		outflow = float( (PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS * 2  ) / self.section )

		self.controller_port = PORTS['controller_ids_port']
		self.controller_ip = IP['controller']
		self.threshold = 0.1
		self.intrusion = False		
		self.wait_time = PLC_PERIOD_SEC

		#print "Connecting to controller"		

		print "Entering while"
		#self.send_message(IP['plc101'], 4234, 0)

		while(count <= PP_SAMPLES):	


	                mv101 = int(self.get(MV101))
   	                p101 = int(self.get(P101))

                	if self.intrusion == False:

			    print "No attack detected"
		
			    try:
				    self.received_level = float(self.receive(LIT101, SENSOR_ADDR))
			    except:
				    continue

			    #  x(t+1)                =        x(t)          +              u(t)            +  L (      y(t)           -     x(t)            )   
			    self.new_estimated_level = self.estimated_level + inflow*mv101 - outflow*p101  + 1.0*(self.received_level - self.estimated_level)

		            print "DEBUG estimated : %.5f" % (self.estimated_level)
		            print "DEBUG received : %.5f" % (self.received_level)

	                    delta =  abs(self.estimated_level - self.received_level)
		            print "DEBUG delta : %.5f" % (delta)

	                    if (delta > self.threshold) and (count>2):
	                        self.switch_sensor(self.controller_ip, self.controller_port)
	                        self.intrusion = True
	                        print "Intrusion detected!"
				continue

			    #x(t) = x(t+1)
			    self.estimated_level = self.new_estimated_level

		        else:
			    self.new_estimated_level = self.estimated_level + inflow*mv101 - outflow*p101

                            print "DEBUG estimated : %.5f" % (self.estimated_level)
                            print "DEBUG received : %.5f" % (self.received_level)

			    self.send_message(IP['plc101'], 4234, self.new_estimated_level)
			    self.estimated_level = self.new_estimated_level
		            #self.received_level = float(self.receive(LIT301, LIT301_ADDR))
			    self.wait_time = PLC_PERIOD_SEC

	                #self.switch_sensor(self.controller_ip, self.controller_port)
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
