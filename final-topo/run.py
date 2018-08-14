
        ids = self.net.get('ids101')
        _intf = Intf( 'eth2', node=ids )
        ids.cmd('ifconfig eth2 192.168.56.101')
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

	#ph201.cmd(sys.executable + ' ph201.py &')
	#time.sleep(0.03)

	#plc201.cmd(sys.executable + ' plc201.py &')
	#time.sleep(0.03)	
	#p201.cmd(sys.executable + ' p201.py &')

	#lit301.cmd(sys.executable + ' lit301.py &')
	#lit101.cmd(sys.executable + ' lit101.py &')
	#time.sleep(0.03)

	#plc101.cmd(sys.executable + ' plc101.py &')
	#time.sleep(0.03)

	#plc301.cmd(sys.executable + ' plc301.py &')
	#time.sleep(0.03)

	#p101.cmd(sys.executable + ' p101.py &')
	#mv101.cmd(sys.executable + ' mv101.py &')
	#p301.cmd(sys.executable + ' p301.py &')

	plant101.cmd(sys.executable + ' physical_process.py > test_2.txt &')		

        # start devices
        CLI(self.net)

        self.net.stop()

if __name__ == "__main__":

    topo = SimpleTopo()
    #controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    net = Mininet(topo=topo, controller = controller)

    dynamic_cps = SimpleCPS(name='industry',net=net)
