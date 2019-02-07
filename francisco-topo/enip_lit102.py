from minicps.devices import PLC
from utils import *
import random
import logging
import time


import socket
import json
import select


SENSOR_ADDR = IP['lit102']
LIT101 = ('LIT101', 1)
LIT102 = ('LIT102', 1)
LIT103 = ('LIT103', 1)


class Lit102(PLC):
	def pre_loop(self, sleep=0.1):
		logging.basicConfig(filename=LOG_LIT102_FILE, level=logging.DEBUG)

	def main_loop(self):
		count = 0
		while True:
			self.level = float(self.get(LIT102))
			self.send(LIT102, self.level, SENSOR_ADDR)
			time.sleep(0.0005)

if __name__ == '__main__':
	lit102 = Lit102(name='lit102',state=STATE,protocol=LIT102_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)

