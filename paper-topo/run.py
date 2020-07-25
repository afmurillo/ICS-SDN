"""
simple-cps run.py
"""
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Controller, RemoteController

from minicps.mcps import MiniCPS

from topo import SimpleTopo
import signal
import subprocess
import shlex
import time
import sys
from utils import IP

automatic = True

class SimpleCPS(MiniCPS):

    """Main container used to run the simulation."""
    def do_forward(self, node):
        # Pre experiment configuration, prepare routing path
        node.cmd('sysctl net.ipv4.ip_forward=1')
        node.waitOutput()

    def add_default_gateway(self, node, gw_ip):
        node.cmd('route add default gw ' + gw_ip)
        node.waitOutput()

    def setup_network(self):
        self.add_default_gateway(net.get('lit101'), IP['plc101'])
        self.add_default_gateway(net.get('p101'), IP['plc101'])
        self.add_default_gateway(net.get('ids101'), IP['plc101'])
        self.do_forward(net.get('plc101'))

        self.add_default_gateway(net.get('lit301'), IP['plc301'])
        self.add_default_gateway(net.get('p301'), IP['plc301'])
        self.do_forward(net.get('plc301'))

    def __init__(self, name, net):

        signal.signal(signal.SIGINT, self.interrupt)
        signal.signal(signal.SIGTERM, self.interrupt)
        self.create_log_files()

        net.start()
        self.setup_network()

        if automatic:
            self.automatic_start()
        else:
            CLI(net)
        net.stop()


    def interrupt(self, sig, frame):
        self.finish()
        sys.exit(0)

    def automatic_start(self):
        self.plc101 = net.get('plc101')
        self.plc101_output = open("output/plc1.log", 'r+')
        self.plc101.cmd('route add -net 192.168.3.0 netmask 255.255.255.0 dev plc101-eth2')
        self.plc101.waitOutput()

        #plc2 = net.get('plc201')
        #plc2_output = open("output/plc2.log", 'r+')

        self.plc301 = net.get('plc301')
        self.plc301_output = open("output/plc3.log", 'r+')
        self.plc301.cmd('route add -net 192.168.1.0 netmask 255.255.255.0 dev plc301-eth2')
        self.plc301.waitOutput()

        self.lit101 = net.get('lit101')
        self.lit101_output = open("output/lit101.log", 'r+')

        self.lit301 = net.get('lit301')
        self.lit301_output = open("output/lit301.log", 'r+')

        self.p101 = net.get('p101')
        self.p101_output = open("output/p101.log", 'r+')

        self.mv101 = net.get('mv101')
        self.mv101_output = open("output/mv101.log", 'r+')

        self.p301 = net.get('p301')
        self.p301_output = open("output/p301.log", 'r+')

        self.plant = net.get('plant101')
        self.plant_output = open("output/plant.log", 'r+')

        # Automatically start the nodes
        print "Launching the LIT sensors"
        self.lit101_process = self.lit101.popen(sys.executable, "lit101.py", stderr=sys.stdout,stdout=self.lit101_output)
        self.lit301_process = self.lit301.popen(sys.executable, "lit301.py", stderr=sys.stdout, stdout=self.lit301_output)

        print "LIT sensors launched"
        print "Launching PLC1 network"
        self.p101_process = self.p101.popen(sys.executable, "p101.py", stderr=sys.stdout, stdout=self.p101_output)
        self.plc101_process = self.plc101.popen(sys.executable, "plc101.py", stderr=sys.stdout, stdout=self.plc101_output)
        self.mv101_process = self.mv101.popen(sys.executable, "mv101.py", stderr=sys.stdout, stdout=self.mv101_output)

        print "PLC1 network launched"
        print "Launching PLC3 network"
        self.plc301_process = self.plc301.popen(sys.executable, "plc301.py", stderr=sys.stdout, stdout=self.plc301_output)
        time.sleep(0.3)

        self.p301_process = self.p301.popen(sys.executable, "p301.py", stderr=sys.stdout, stdout=self.p301_output)

        print "PLC3 network launched"
        print "Launching Simulation"
        self.simulation = self.plant.popen(sys.executable, "physical_process.py", stderr=sys.stdout, stdout=self.plant_output)

        while self.simulation.poll() is None:
            pass
        self.finish()


    def end_process(self, process):
        process.send_signal(signal.SIGINT)
        process.wait()
        if process.poll() is None:
            process.terminate()
        if process.poll() is None:
            process.kill()

    def finish(self):
        print "Simulation finished"
        self.end_process(self.p301_process)
        self.end_process(self.plc301_process)

        self.end_process(self.mv101_process)
        self.end_process(self.plc101_process)
        self.end_process(self.p101_process)

        self.end_process(self.lit301_process)
        self.end_process(self.lit101_process)

        if self.simulation:
            self.simulation.terminate()

        cmd = shlex.split("./kill_cppo.sh")
        subprocess.call(cmd)
        net.stop()
        sys.exit(0)


    def create_log_files(self):
        subprocess.call("./create_log_files.sh")

if __name__ == "__main__":
    topo = SimpleTopo()
    controller = RemoteController('c0', ip='127.0.0.1', port=6633)
    net = Mininet(topo=topo, controller=controller)
    dynamic_cps = SimpleCPS(name='industry', net=net)