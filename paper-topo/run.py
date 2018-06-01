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
	plc2 = self.net.get('plc201')
	plc3 = self.net.get('plc301')

        ids101 = self.net.get('ids101')
        _intf = Intf( 'eth2', node=ids101 )
        ids101.cmd('ifconfig eth2 192.168.56.101')

	ids301 = self.net.get('ids301')
	ids301.cmd('route add -net 192.168.1.0 netmask 255.255.255.0 dev ids301-eth3')

	_intf = Intf( 'eth3', node=ids301 )
        ids301.cmd('ifconfig eth3 192.168.56.103')



	plc1.cmd('route add default gw 192.168.1.254 plc101-eth0  ')
	plc2.cmd('route add default gw 192.168.2.254 plc201-eth0  ')
	plc3.cmd('route add default gw 192.168.3.254 plc301-eth0  ')	

	plc1.cmd('route add -net 192.168.3.0 netmask 255.255.255.0 dev plc101-eth2')
	plc3.cmd('route add -net 192.168.1.0 netmask 255.255.255.0 dev plc301-eth2')

        # start devices
        CLI(self.net)

        self.net.stop()

if __name__ == "__main__":

    topo = SimpleTopo()
    #controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    net = Mininet(topo=topo, controller = controller)

    dynamic_cps = SimpleCPS(name='industry',net=net)

