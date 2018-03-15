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

import subprocess

from utils import IP

from mininet.link import Intf

class SimpleCPS(MiniCPS):

    """Main container used to run the simulation."""

    def __init__(self, name, net):

        self.name = name
        self.net = net
        self.net.start()

	plc2 = self.net.get('plc201')
	plc2.cmd('route add default gw 192.168.2.254 plc201-eth0  ')

	ph201 = self.net.get('ph201')
	ph201.cmd('rm -rf ph201.log')
	ph201.cmd('python ph201.py &')

        plc201 = self.net.get('plc201')
        plc201.cmd('rm -rf plc201.log')
        plc201.cmd('python plc201.py &')

	p201 = self.net.get('p201')
        p201.cmd('rm -rf p201.log')
        p201.cmd('python p201.py &')


        # start devices
        CLI(self.net)

        self.net.stop()

if __name__ == "__main__":

    topo = SimpleTopo()
    #controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    net = Mininet(topo=topo, controller = controller)

    dynamic_cps = SimpleCPS(name='industry',net=net)

