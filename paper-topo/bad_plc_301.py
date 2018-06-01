"""
PLC 3
"""

from minicps.devices import PLC
from threading import Thread
from utils import *

import time
import sys
import socket
import json
import select

P301 = ('P301', 3)
LIT301 = ('LIT301', 3)

LIT301_ADDR = IP['lit301']
P301_ADDR = IP['p301']
PLC101_ADDR = IP['plc101-HMI']

class HMISocket(Thread):
    """ Class that responds to the POLL command from HMI """
    def __init__(self, plc_object):
        Thread.__init__(self)
        self.plc = plc_object
        self.lit301 = 0.0

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
                    self.sock.send("LIT301: "+str(self.lit101))
                data = ''
    def setLit301(self, val):
        self.lit301 = val

# TODO: real value tag where to read/write flow sensor
class PLC301(PLC):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s1 plc1 enters pre_loop'
        print
        time.sleep(sleep)

    def main_loop(self):
        """plc1 main loop.

            - reads sensors value
            - drives actuators according to the control strategy
            - updates its enip server
        """

        print 'DEBUG: swat-s1 plc1 enters main_loop.'
        print

        count = 0
        while(count <= PLC_SAMPLES):	    

            lit301 = float(self.receive(LIT301, LIT301_ADDR))

	    if (lit301 > 0.5) and (count > 10):
		    print "Attack!"
                    if lit301 >= LIT_301_M['HH'] :
                        self.send(P301, 0, IP['plc301'])

                    elif lit301 >= LIT_301_M['H']:
                        self.send(P301, 0, IP['plc301'])

                    elif lit301 <= LIT_301_M['LL']:
                        self.send(P301, 0, IP['plc301'])

                    elif lit301 <= LIT_301_M['L']:
                        self.send(P301, 0, IP['plc301'])
		        

            else:
	            self.send_message(PLC101_ADDR, 8754, lit301)
		    print "Regular"

	            if lit301 >= LIT_301_M['HH'] :
	                self.send(P301, 1, IP['plc301'])

	            elif lit301 >= LIT_301_M['H']:
	                self.send(P301, 1, IP['plc301'])

	            elif lit301 <= LIT_301_M['LL']:
	                self.send(P301, 0, IP['plc301'])

	            elif lit301 <= LIT_301_M['L']:
	                self.send(P301, 0, IP['plc301'])

            count += 1 


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

if __name__ == "__main__":

    plc301 = PLC301(name='plc301',state=STATE,protocol=PLC301_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
