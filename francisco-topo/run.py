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

        lit103 = self.net.get('lit103')
        lit103.cmd('rm -rf lit103.log')
        lit103.cmd('python lit103.py &')

        q101 = self.net.get('q101')
        q101.cmd('python q101.py &')

        q102 = self.net.get('q102')
        q102.cmd('python q102.py &')

        # start devices
        CLI(self.net)

        self.net.stop()

if __name__ == "__main__":

    topo = SimpleTopo()
    #controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    net = Mininet(topo=topo, controller = controller)

    dynamic_cps = SimpleCPS(name='industry',net=net)

