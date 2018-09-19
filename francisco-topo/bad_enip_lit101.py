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

	def main_loop(self):
                bad_lit_flag = 2
                diff_attack_value = -20e-3
                abs_attack_value = 0.43
                attack_time_begin = 625000
                attack_time_end = 950000
		count = 0

		while True:
			self.level = float(self.get(LIT101))
			if count >= attack_time_begin and count <= attack_time_end:
				if bad_lit_flag == 1:
					self.level = self.level + diff_attack_value
				if bad_lit_flag == 2:
					self.level = abs_attack_value

			self.send(LIT101, self.level, SENSOR_ADDR)
			count = count + 1

if __name__ == '__main__':
	lit101 = Lit101(name='lit101',state=STATE,protocol=LIT101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)

