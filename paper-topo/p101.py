from minicps.devices import PLC
from utils import *

import time
from threading import Thread

import socket
import json
import select
import logging

PLC101_ADDR = IP['plc101']

P101 = ('P101', 1)

class PSocket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, plc_object):        
        Thread.__init__(self)
        self.plc = plc_object

    def run(self):
        print "DEBUG entering socket thread run"
	logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='diogo_replay/p101.log')
        self.sock = socket.socket()     # Create a socket object    
        self.sock.bind((IP['p101'] , 7842 ))
        self.sock.listen(5)
	end=0

        while True:
            try:
                client, addr = self.sock.accept()
                data = client.recv(4096)                                                # Get data from the client
                message_dict = eval(json.loads(data))
                p101 = int(message_dict['Variable'])

		logging.info('P101: %f', p101)
		self.plc.set(P101, p101)

            except KeyboardInterrupt:
                print "\nCtrl+C was hitten, stopping server"
                client.close()
                break

class PP101(PLC):
        def pre_loop(self, sleep=0.1):
                print 'DEBUG: p101 enters pre_loop'
                time.sleep(sleep)

        def main_loop(self):
                print 'DEBUG: p101 enters main_loop'
                count = 0
                psocket = PSocket(self)
                psocket.start()

if __name__ == '__main__':
	p101 = PP101(name='p101',state=STATE,protocol=P101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)

