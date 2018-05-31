from minicps.devices import PLC
from utils import *

import time
from threading import Thread

import socket
import json
import select


PLC101_ADDR = IP['plc101']

Q102 = ('Q102', 1)

class PSocket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, plc_object):        
        Thread.__init__(self)
        self.plc = plc_object
	self.q102 = 0

    def run(self):
        print "DEBUG entering socket thread run"
        self.sock = socket.socket()     # Create a socket object    
        self.sock.bind((IP['q102'] , 7842 ))
        self.sock.listen(5)

        while True:
            try:
                client, addr = self.sock.accept()
                data = client.recv(4096)                                                # Get data from the client         

                message_dict = eval(json.loads(data))
                self.q102 = float(message_dict['Variable'])

                print "received from PLC101!", self.q102 
		self.plc.set(Q102, self.q102)           

            except KeyboardInterrupt:
                print "\nCtrl+C was hitten, stopping server"
                client.close()
                break

class PP102(PLC):
        def pre_loop(self, sleep=0.1):
                print 'DEBUG: q102 enters pre_loop'
                time.sleep(sleep)

        def main_loop(self):
                print 'DEBUG: q102 enters main_loop'
                count = 0
                psocket = PSocket(self)
                psocket.start()       

if __name__ == '__main__':
	q102 = PP102(name='q102',state=STATE,protocol=Q102_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)

