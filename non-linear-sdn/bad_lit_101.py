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
		self.bad_lit_flag = 1
		# Original value
 	 	self.diff_attack_value = -50e-3
 	 	#self.diff_attack_value = -20e-3
		self.abs_attack_value = 0.43
		#self.attack_time_begin = 625000
		#self.attack_time_end = 950000
		self.attack_time_begin = 200000
		self.attack_time_end = 360000

		while True:
			self.level = float(self.get(LIT101))
			if count >=  self.attack_time_begin and count <= self.attack_time_end:
				if self.bad_lit_flag == 1:
					self.level = self.level + self.diff_attack_value
                                if self.bad_lit_flag == 2:
                                        self.level = self.abs_attack_value

                        self.send_message(IP['plc101'], 8754,self.level)
			count = count + 1
			time.sleep(0.0005)

if __name__ == '__main__':
	lit101 = Lit101(name='lit101',state=STATE,protocol=LIT101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)

