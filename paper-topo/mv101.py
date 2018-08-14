from minicps.devices import PLC
from utils import *

import time
from threading import Thread

import socket
import json
import select


PLC101_ADDR = IP['plc101']

MV101 = ('MV101', 1)

class MVSocket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, plc_object):        
        Thread.__init__(self)
        self.plc = plc_object

    def run(self):
        print "DEBUG entering socket thread run"
        self.sock = socket.socket()     # Create a socket object    
        self.sock.bind((IP['mv101'] ,9587 ))
        self.sock.listen(5)
	self.command_time = 0

        while True:
            try:
            	client, addr = self.sock.accept()
		data = client.recv(4096)                                                # Get data from the client                     		
            	message_dict = eval(json.loads(data))
	        mv101 = int(message_dict['Variable'])

	        print "received from PLC101!", mv101
		self.plc.set(MV101, mv101)          
		self.command_time = time.time() - self.command_time
		print "Command time:", self.command_time
 
            except KeyboardInterrupt:
 	        print "\nCtrl+C was hitten, stopping server"
                client.close()
        	break


class Mv101(PLC):
	def pre_loop(self, sleep=0.1):
		print 'DEBUG: mv101 enters pre_loop'
		time.sleep(sleep)

	def main_loop(self):
		print 'DEBUG: mv101 enters main_loop'
		count = 0


	        mvsocket = MVSocket(self)
	        mvsocket.start()

		while count<=PLC_SAMPLES:
			try:
				mv101 = int(self.receive(MV101, PLC101_ADDR))
				print "DEBUG: Received mv101 command %.5f" % mv101
				self.set(MV101, mv101)

		        except:
				print "Switching to backup"
			        break			


if __name__ == '__main__':
	mv101 = Mv101(name='mv101',state=STATE,protocol=MV101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
#	mv101.pre_loop()
#	mv101.main_loop()

