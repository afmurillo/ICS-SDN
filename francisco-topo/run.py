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

    lit101 = self.net.get('lit101')
    lit101.cmd('rm -rf lit101.log')
    lit101.cmd('python lit101.py &')

	plc1 = self.net.get('plc101')    
	plc1.cmd('route add default gw 192.168.2.254 plc101-eth0  ')
    plc1.cmd('rm -rf plc101.log')
    plc1.cmd('python plc101.py &')

    lit301 = self.net.get('lit301')
    lit301.cmd('rm -rf lit301.log')
    lit301.cmd('python lit301.py &')

    plc3 = self.net.get('plc301')
    plc3.cmd('route add default gw 192.168.2.254 plc301-eth0  ')
    plc3.cmd('rm -rf plc301.log')
    plc3.cmd('python plc301.py &')

        # start devices
        CLI(self.net)

        self.net.stop()

if __name__ == "__main__":

    topo = SimpleTopo()
    #controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    net = Mininet(topo=topo, controller = controller)

    dynamic_cps = SimpleCPS(name='industry',net=net)

