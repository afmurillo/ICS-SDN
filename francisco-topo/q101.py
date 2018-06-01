from minicps.devices import PLC
from utils import *

import time
from threading import Thread

import socket
import json
import select


PLC101_ADDR = IP['plc101']

Q101 = ('Q101', 1)

class PSocket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, plc_object):
        Thread.__init__(self)
        self.plc = plc_object
	self.q101 = 0

    def run(self):
        print "DEBUG entering socket thread run"
        self.sock = socket.socket()     # Create a socket object
        self.sock.bind((IP['q101'] , 7842 ))
        self.sock.listen(5)

        while True:
            try:
                client, addr = self.sock.accept()
                data = client.recv(4096)                                                # Get data from the client

                message_dict = eval(json.loads(data))
                self.q101 = float(message_dict['Variable'])

                print "received from PLC101!", self.q101
		self.plc.set(Q101, self.q101)

            except KeyboardInterrupt:
                print "\nCtrl+C was hitten, stopping server"
                client.close()
                break

class PP101(PLC):
        def pre_loop(self, sleep=0.1):
                print 'DEBUG: q101 enters pre_loop'
                time.sleep(sleep)

        def main_loop(self):
                print 'DEBUG: q101 enters main_loop'
                count = 0
                psocket = PSocket(self)
                psocket.start()       

if __name__ == '__main__':
	q101 = PP101(name='q101',state=STATE,protocol=Q101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)

