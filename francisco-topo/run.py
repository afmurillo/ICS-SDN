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
        #lit101.cmd('python lit101.py &')

	    #plc1 = self.net.get('plc101')    
	    #plc1.cmd('route add default gw 192.168.2.254 plc101-eth0  ')
        #plc1.cmd('python plc101.py &')

        lit102 = self.net.get('lit102')
        lit102.cmd('rm -rf lit102.log')
        #lit102.cmd('python lit102.py &')

        lit103 = self.net.get('lit103')
        lit103.cmd('rm -rf lit103.log')
        #lit103.cmd('python lit103.py &')


	plant = self.net.get('plant101')
	plant.cmd('rm -rf plant.log')
	plant.cmd('python physical_process.py &')

        # start devices
        CLI(self.net)

        self.net.stop()

if __name__ == "__main__":

    topo = SimpleTopo()
    #controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    net = Mininet(topo=topo, controller = controller)

    dynamic_cps = SimpleCPS(name='industry',net=net)

