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
LIT103 = ('LIT103', 1)


class Lit103(PLC):
	def pre_loop(self, sleep=0.1):
		logging.basicConfig(filename=LOG_LIT103_FILE, level=logging.DEBUG)

	def main_loop(self):
		count = 0
		while True:
			self.level = float(self.get(LIT103))
			self.send(LIT103, self.level, SENSOR_ADDR)

if __name__ == '__main__':
	lit103 = Lit103(name='lit103',state=STATE,protocol=LIT103_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)

