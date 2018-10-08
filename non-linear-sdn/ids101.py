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
LIT101 = ('LIT101', 1)


class Ids101Socket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, plc_object):
        Thread.__init__(self)
        self.ids = plc_object

    def run(self):
        self.sock = socket.socket()     # Create a socket object
        self.sock.bind((IP['ids101'] , 8754 ))
        self.sock.listen(5)

        while (self.ids.count <= PLC_SAMPLES):
            try:
            	client, addr = self.sock.accept()
		data = client.recv(4096)                                                # Get data from the client
            	message_dict = eval(json.loads(data, parse_float=Decimal))
            	#message_dict = eval(json.loads(data))
	        self.ids.received_lit101 = float(message_dict['Variable'])		
            except KeyboardInterrupt:
 	        print "\nCtrl+C was hitten, stopping server"
                client.close()
        	break
        print "Socket closed"


class Ids101(PLC):

	def pre_loop(self, sleep=0.1):


	def main_loop(self):
		count = 0

        ids101socket = Ids101Socket(self)
        ids101socket.start()

		while(count <= PLC_SAMPLES):	
			print "Received from lit101", self.received_lit101 


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
