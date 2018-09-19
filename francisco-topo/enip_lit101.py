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
		while True:
			self.level = float(self.get(LIT101))
			self.send(LIT101, self.level, SENSOR_ADDR)

if __name__ == '__main__':
	lit101 = Lit101(name='lit101',state=STATE,protocol=LIT101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)

