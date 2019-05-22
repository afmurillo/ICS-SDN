from minicps.devices import PLC
from utils import *
import random
import time
import logging

SENSOR_ADDR = IP['lit301']

LIT301 = ('LIT301', 3)

class Lit301(PLC):
	def pre_loop(self, sleep=0.1):
		time.sleep(sleep)

	def main_loop(self):
		count = 0
		gaussian_noise_experiment = 0
		noise_level = 0.03
		logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='replay_attack/lit301.log')
		while True:
			self.level = float(self.get(LIT301))
			if gaussian_noise_experiment == 1:
				self.level = self.level + random.gauss(0, noise_level)
				if self.level > 1.0:
					self.level = 1.0
				if self.level <0:
					self.level = 0.0
			self.send(LIT301, self.level, IP['lit301'])
			logging.info('LIT301: %f', self.level)
			time.sleep(PLC_PERIOD_SEC)


if __name__ == '__main__':
	lit301 = Lit301(name='lit301',state=STATE,protocol=LIT301_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)


