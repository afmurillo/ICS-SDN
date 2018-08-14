"""
simple-cps run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Controller, RemoteController

from minicps.mcps import MiniCPS

from topo import SimpleTopo

import sys

import time

from utils import IP

from mininet.link import Intf

class SimpleCPS(MiniCPS):

    """Main container used to run the simulation."""

    def __init__(self, name, net):

        self.name = name
        self.net = net


        self.net.start()

	plc1 = self.net.get('plc101')
	plc1.cmd('route add default gw 192.168.1.254 plc101-eth0  ')

        # start devices
        CLI(self.net)

        self.net.stop()

if __name__ == "__main__":

    topo = SimpleTopo()
    #controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    net = Mininet(topo=topo, controller = controller)
    dynamic_cps = SimpleCPS(name='industry',net=net)

