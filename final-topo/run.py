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

	plc101 = self.net.get('plc101')
	plc201 = self.net.get('plc201')
	plc301 = self.net.get('plc301')

	ids = self.net.get('ids101')
	_intf = Intf( 'eth2', node=ids )
	ids.cmd('ifconfig eth2 192.168.56.101')

	mv101 = self.net.get('mv101')
	p101 = self.net.get('p101')
	lit101 = self.net.get('lit101')
	plant101 = self.net.get('plant101')
	
	p201 = self.net.get('p201')
	ph201 = self.net.get('ph201')

	lit301 = self.net.get('lit301')
	p301 = self.net.get('p301')

	#plc2.cmd(sys.executable + ' plc2.py &')



	plc101.cmd('route add default gw 192.168.1.254 plc101-eth0  ')
	plc201.cmd('route add default gw 192.168.2.254 plc201-eth0  ')
	plc301.cmd('route add default gw 192.168.3.254 plc301-eth0  ')	

	

        # start devices
        CLI(self.net)

        self.net.stop()

if __name__ == "__main__":

    topo = SimpleTopo()
    #controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    net = Mininet(topo=topo, controller = controller)

    dynamic_cps = SimpleCPS(name='industry',net=net)
