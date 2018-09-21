from minicps.devices import PLC
from utils import *
import random
import logging
import time


import socket 
import json 
import select


SENSOR_ADDR = IP['lit101']
LIT101 = ('LIT101', 1)
LIT102 = ('LIT102', 1)

class Lit101(PLC):
	def pre_loop(self, sleep=0.1):
		logging.basicConfig(filename=LOG_LIT101_FILE, level=logging.DEBUG)

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

	def main_loop(self):
		count = 0
		while True:
			self.level = float(self.get(LIT101))
                        self.send_message(IP['plc101'], 8754,self.level)
			time.sleep(0.0005)

if __name__ == '__main__':
	lit101 = Lit101(name='lit101',state=STATE,protocol=LIT101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)

