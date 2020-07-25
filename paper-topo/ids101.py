from minicps.devices import PLC
from utils import *

from threading import Thread

import sys
import time
import socket
import json
import select

import logging
import signal
import sys

SENSOR_ADDR = IP['lit101']
PLC101_ADDR = IP['plc101']
IDS_ADDR = IP['ids101']
LIT301_ADDR = IP['lit301']

MV101 = ('MV101', 1)
P101 = ('P101', 1)
LIT101 = ('LIT101', 1)

CUSTOM_PUMP_FLOWRATE_IN = 3.0

class Ids101(PLC):

	def switch_component(self, controller_ip, controller_port, component):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((controller_ip, int(controller_port)))
		msg_dict = dict.fromkeys(['Type', 'Variable'])
		msg_dict['Type'] = "Command"
		msg_dict['Variable'] = component
		message = json.dumps(str(msg_dict))
		try:
			ready_to_read, ready_to_write, in_error = select.select([sock, ], [sock, ], [], 5)
			self.stop_defense_time = time.time()
			self.defense_time = self.stop_defense_time - self.start_defense_time

		except socket.error, exc:
			return

		if(ready_to_write > 0):
			sock.send(message)
			sock.close()

	
	def notifyPLCOfIntrustion(self, intrussion):
		self.send_message(IP['plc101'], 4234, intrussion, "Intrussion")
	
	def calculate_controls(self, variable):
		estimated = 1

		if variable >= LIT_101_M['HH'] :
			estimated = 0
		elif variable >= LIT_101_M['H'] :
			estimated = 0
		elif variable <= LIT_101_M['L']:
			estimated = 1
		elif variable <= LIT_101_M['LL']:
			estimated = 1

		if variable > LIT_101_M['L'] and variable < LIT_101_M['H']:
			if self.filling:
				estimated = 1
			else:
				estimated = 0
		return estimated

	def sigint_handler(self, sig, frame):
		print "I received a SIGINT!"
		sys.exit(0)

	def pre_loop(self, sleep=0.1):
		signal.signal(signal.SIGINT, self.sigint_handler)
		signal.signal(signal.SIGTERM, self.sigint_handler)
		# Estimated values
		self.section = TANK_SECTION	

	def main_loop(self):
		logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='output/ids101.log')
		count = 0
		
		# Water level reported by LIT101
		self.received_level = 0.0
		
		# Water level estimated by the observer
		self.estimated_level = 0.4
		
		# Water level estimated when an intrusion is detected
		self.intrusion_level = 0.0
		
		# Counter that indicates for how long the sensor is not compromised, after an attack
		self.good_values_counter = 0
			
		# Threshold to assume the sensor is not compromised
		self.good_threshold = 10

		# The values are for a 0.2 period, we calculate every 1.0 period
		inflow = float( (CUSTOM_PUMP_FLOWRATE_IN * PP_PERIOD_HOURS * 2 )  / self.section )
		outflow = float( (PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS * 2  ) / self.section )

		self.controller_port = PORTS['controller_ids_port']
		self.controller_ip = IP['controller']
		self.threshold = 0.1
		self.sensor_intrusion = False		
		self.plc_intrusion = False	
		self.plc_count = 0
		self.filling = False
		self.wait_time = PLC_PERIOD_SEC
		self.start_defense_time = 0
		self.stop_defense_time = 0
		self.defense_time = 0

		while count <= PP_SAMPLES:

			mv101 = int(self.get(MV101))
			p101 = int(self.get(P101))

			if count == 0:
				self.new_estimated_level = float(self.receive(LIT101, SENSOR_ADDR))
				self.estimated_level = self.new_estimated_level

			else:
				if self.sensor_intrusion == False:

					try:
						self.received_level = float(self.receive(LIT101, SENSOR_ADDR))
						self.start_defense_time = time.time()
					except:
						continue

					#  x(t+1)                =        x(t)          +              u(t)            +  L (      y(t)           -     x(t)            )
					self.new_estimated_level = self.estimated_level + inflow*mv101 - outflow*p101  + 1.0*(self.received_level - self.estimated_level)
					delta =  abs(self.estimated_level - self.received_level)
					logging.info('IDS101: NORMAL %f', self.received_level )

					if (delta > self.threshold):
						self.sensor_intrusion = True
						self.notifyPLCOfIntrustion(self.sensor_intrusion)
						self.send_message(IP['plc101'], 4234, self.new_estimated_level, "Report")
						continue

					self.estimated_level = self.new_estimated_level

				else:
					# We still need to receive the sensor information to see if the attack has stopped
					try:
						self.received_level = float(self.receive(LIT101, SENSOR_ADDR))
						self.start_defense_time = time.time()
					except:
						continue

					# Calculate the estimated level, without the compromised sensor data
					self.new_estimated_level = self.estimated_level + inflow*mv101 - outflow*p101
					delta = abs(self.estimated_level - self.received_level )

					if (delta < self.threshold):
						self.sensor_intrusion = False
						self.notifyPLCOfIntrustion(self.sensor_intrusion)
						self.send_message(IP['plc101'], 4234, self.new_estimated_level, "Report")
						logging.info('IDS101: NORMAL %f', self.received_level )
					else:
						self.send_message(IP['plc101'], 4234, self.new_estimated_level, "Report")
						logging.info('IDS101: ATTACK : %f', self.new_estimated_level )

					self.estimated_level = self.new_estimated_level

			self.wait_time = PLC_PERIOD_SEC
			count += 1
			time.sleep(self.wait_time)

	def send_message(self, ipaddr, port, message, message_type):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((ipaddr, port))

		msg_dict = dict.fromkeys(['Type', 'Variable'])
		msg_dict['Type'] = message_type
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

if __name__ == '__main__':
	ids101 = Ids101(name='ids101',state=STATE,protocol=IDS101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
