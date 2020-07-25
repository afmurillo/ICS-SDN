"""
PLC 2
"""

from minicps.devices import PLC
from threading import Thread
from utils import *
import socket
import time
import sys
import signal

PH201 = ('PH201', 2)
P201 = ('P201', 2)

PH201_ADDR = IP['ph201']

class HMISocket(Thread):
    """ Class that responds to the POLL command from HMI """
    def __init__(self, plc_object):
        Thread.__init__(self)
        self.plc = plc_object
        self.ph201 = 0.0

    def run(self):
        print "DEBUG entering socket thread run"
        self.sock = socket.socket()
        self.sock.connect((IP['HMI'], int(PORTS['hmi_poll_port'])))
        data = ''
        while True:
            while data=='':
                data = self.sock.recv(100)
                time.sleep(1)
                if data == "POLL":
                    self.sock.send("PH201: "+str(self.ph201))
                data = ''
    def setPH201(self, val):
        self.ph201 = val

# TODO: real value tag where to read/write flow sensor
class PLC201(PLC):

    def sigint_handler(self, sig, frame):
        print "I received a SIGINT!"
        sys.exit(0)

    def pre_loop(self, sleep=0.1):
        signal.signal(signal.SIGINT, self.sigint_handler)
        signal.signal(signal.SIGTERM, self.sigint_handler)

    def main_loop(self):
        """plc1 main loop.

            - reads sensors value
            - drives actuators according to the control strategy
            - updates its enip server
        """

        print 'DEBUG: swat-s1 plc1 enters main_loop.'
        print

        hmi = HMISocket(self)
        hmi.start()
        count = 0

        while count <= PLC_SAMPLES:
            ph201 = float(self.receive(PH201, PH201_ADDR))
            print 'DEBUG plc2 ph201: %.5f' % ph201

            # We only apply PH stabilizer if there's flow
            if ph201 >= PH_201_M['HH']:
                self.send(P201, 0, IP['plc201'])
            elif ph201 >= PH_201_M['H']:
                self.send(P201, 0, IP['plc201'])
            elif ph201 <= PH_201_M['LL']:
                self.send(P201, 1, IP['plc201'])
            elif ph201 <= PH_201_M['L']:
                self.send(P201, 1, IP['plc201'])
                hmi.setPH201(ph201)

if __name__ == "__main__":

    plc201 = PLC201(name='plc201',state=STATE,protocol=PLC201_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
