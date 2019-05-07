from minicps.devices import PLC
from utils import *
import random
import time

SENSOR_ADDR = IP['lit301']

LIT301 = ('LIT301', 3)

class Lit301(PLC):
	def pre_loop(self, sleep=0.1):
		time.sleep(sleep)

	def main_loop(self):
		count = 0
		gaussian_noise_experiment = 1
		noise_level = 0.1
		start=time.time()
		while count<=PLC_SAMPLES:
			self.level = float(self.get(LIT301))
			if gaussian_noise_experiment == 1:
				self.level = self.level + random.gauss(0, noise_level)
				if self.level > 1.0:
					self.level = 1.0
				if self.level <0:
					self.level = 0.0
			self.send(LIT301, self.level, IP['lit301'])
			end = time.time()
			sample_time = end-start
			print '\n lit301: time: ',sample_time, 'value: ', self.level, '\n'
			time.sleep(PLC_PERIOD_SEC)


if __name__ == '__main__':
	lit301 = Lit301(name='lit301',state=STATE,protocol=LIT301_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
			

