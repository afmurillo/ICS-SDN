"""
switchFlow.py: Basic l2_learning switch that switches flows between a real sensor and a simulation
Topology used: linuxrouter.py
Status: Incomplete. 
"""


from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.recoco import Timer
from pox.lib.util import dpid_to_str
from pox.lib.addresses import IPAddr, IPAddr6, EthAddr  # used for flow_mod matching
from pox.lib.revent import Event, EventMixin, EventHalt
from pox.lib.packet.ethernet import ethernet

from pprint import pformat
import time

from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
from pox.openflow.of_json import *
#from oslo.config import cfg

from threading import Thread


import json
import select
import socket


#from controller_utils import *
from utils import *

log = core.getLogger()

class ControllerSocket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, report_object):
        Thread.__init__(self)
        self.report_object = report_object    
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # Create a socket object

    def run(self):
        print 'DEBUG listening on port', int(PORTS['controller_ids_port'])
        self.sock.bind((IP['controller'] , int(PORTS['controller_ids_port'])))
        self.sock.listen(5)

        while True:
            try:
                client, addr = self.sock.accept()
                data = client.recv(14336)                                                # Get data from the client
                #print 'Message from', addr                                              # Print a message confirming
                if data:
                    data_treatment = HandleMessage(self.report_object, data)    # Call the thread to work with the data received
                    data_treatment.setDaemon(True)                                  # Set the thread as a demond
                    data_treatment.start()                                                  # Start the thread
            except KeyboardInterrupt:
                print "\nCtrl+C was hitten, stopping server"
                client.close()
                break

    def close_connection(self):
        #self.socket_flag = False
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

class HandleMessage(Thread):

    """ Class that process the message and calls appropiate handling method """
    def __init__(self, report_object, received):
        Thread.__init__(self)
        self.received = received
        self.report_object = report_object

    def run(self):
        self.report_object.received_message(self.received)

class DynamicController(object):

    def __init__(self):

        #self.connection = connection
	self.connections = []
        self.transparent = False

        # Our table
        self.macToPort = {}

        # We just use this to know when to log a helpful message
        self.hold_down_expired = 0
        self.controller_socket = ControllerSocket(self)
        self.controller_socket.start()
        self.attack_detected = False
	self.compromised_sensor = False
	self.compromised_plc = False 
        self.start_control_time = 0
	self.stop_control_time = 0
	self.control_time = 0

    def add_connection_object(self, connection):
	self.connections.append(connection)
	connection.addListeners(self)

    def close_connection(self):
        self.controller_socket.close_connection()

    def received_message(self, message):
        """ Handles the message received"""
        print "DEBUG: in recieved_message"
	self.start_control_time = time.time()
        message_dict = eval(json.loads(message))
        print "Message received: " + str(message_dict)
        if message_dict['Type'] == "Command":
            self.process_command(message_dict)

    def process_command(self, message):    

        # Switch to simulator
        if message['Variable'] == 'Switch_flow':
            #self.switch_flow('lit101','ids101',10,of.OFP_FLOW_PERMANENT, True)
            self.simple_switch_flow()
	    self.compromised_sensor = True

        if message['Variable'] == 'Switch_plc':
            self.simple_switch_flow()
	    #self.compromised_plc = True
		

    def simple_switch_flow(self):
        # Simple switch just deletes all flow entries, triggering packet_in events.
        # In packet in, we simply don't create an entry for the attacker
        # Yes, this could be done in a thousand better ways :D
        self.attack_detected = True       
        msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
        msg.priority = 65535
        for connection in self.connections:
	    connection.send(msg)                

	self.stop_control_time = time.time()
	self.control_time = self.stop_control_time - self.start_control_time
	print "Control Time: ", self.control_time


    def switch_flow(self, old_host, new_host, idle_timeout, hard_timeout, drop):

        log.debug("Switching flows")

        if drop == True:
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match(in_port = int(DPCTL_PORTS[old_host]), dl_type = 0x800, nw_src=IP[old_host], nw_dst=IP['plc101'])            
            msg.idle_timeout = idle_timeout
            msg.hard_timeout = hard_timeout
            msg.priority = 30000         

	    for connection in self.connections:
            	connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match(in_port = int(DPCTL_PORTS[new_host]), dl_type = 0x800, nw_src=IP[new_host], nw_dst=IP['plc101'])
        msg.idle_timeout = idle_timeout
        msg.hard_timeout = hard_timeout
        msg.priority = 30000
        action = of.ofp_action_output(port=int(DPCTL_PORTS['plc101']))
        msg.actions.append(action)

	for connection in self.connections:
      		connection.send(msg)
       
    def _handle_PacketIn(self, event):
        """
        Manage PacketIn events sent by event,connection datapaths.

        """
        packet = event.parsed
        log.debug("Incoming packet from port: %i", event.port)
        #print "From connection: ", str(event.dpid)

        in_port = event.port
	if (self.attack_detected):

                a_msg = of.ofp_flow_mod()
                a_msg.match = of.ofp_match.from_packet(packet, event.port)
		nw_src = a_msg.match.nw_src
		print "Nw src: ", nw_src

	        if (in_port == 4) and (nw_src == "192.168.1.10") and (self.compromised_sensor):
			log.debug("Dropping packets from malicious sensor!")
		        return

	        #if (in_port == 4) and (nw_src == "192.168.3.30") and (self.compromised_plc):
                #log.debug("Dropping packets from malicious PLC!")
                #return


        def flood(message=None):
            """
            create a packet_out with flood rule
            waiting _flood_delay sec before sending the instruction to the switch

            :message: optional log.debug message

            """
            log.debug("Entering flood")
            msg = of.ofp_packet_out()  # create of_packet_out
            action = of.ofp_action_output(port=of.OFPP_FLOOD)
            msg.actions.append(action)
            msg.data = event.ofp
            msg.in_port = event.port
            log.debug(message)
	    for connection in self.connections:
            	connection.send(msg)


        def drop(duration=None):
            """TODO: Docstring for drop.

            """
            if duration is not None:
                if not isinstance(duration, tuple):  # idle_timeout, hard_timeout
                    duration = (duration, duration)
                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match.from_packet(packet)
                msg.idle_timeout = duration[0]
                msg.hard_timeout = duration[1]
                msg.buffer_id = event.ofp.buffer_id
                msg.in_port = event.port
                log.debug("Warning dropping!")
		for connection in self.connections:
            		connection.send(msg)
                #self.connection.send(msg)
            elif event.ofp.buffer_id is not None:
                msg = of.ofp_packet_out()
                msg.buffer_id = event.ofp.buffer_id
                msg.in_port = event.port
                log.debug("Warning dropping!")
		for connection in self.connections:
            		connection.send(msg)
  	        #self.connection.send(msg)


        self.macToPort[packet.src] = event.port

        if not self.transparent:
            if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
                drop()
                return

        if packet.dst.is_multicast:
            flood()
        else:
            if packet.dst not in self.macToPort:
                flood("Port from %s unknown -- flooding" % (packet.dst))
            else:
                port = self.macToPort[packet.dst]
                if port == event.port:
                    log.warning("Same port for packet from %s -> %s on %s.%s.  Drop."
                            % (packet.src, packet.dst, dpid_to_str(event.dpid), port))
                    drop(10)
                    return
                log.debug("installing flow for %s.%i -> %s.%i"
                    % (packet.src, event.port, packet.dst, port))
                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match.from_packet(packet, event.port)
                msg.match.dl_src = None
                msg.match.dl_dst = None
                msg.match.dl_vlan = None
                msg.match.dl_vlan_pcp = None
                msg.match.nw_tos = None
                msg.match.nw_proto = None
                msg.match.tp_src = None
                msg.match.tp_dst = None
                msg.idle_timeout = 10
                msg.hard_timeout = 30
                msg.priority = 10000
                action = of.ofp_action_output(port=port)
                msg.actions.append(action)
                msg.data = event.ofp
		for connection in self.connections:
            		connection.send(msg)
                #self.connection.send(msg)

class CentralComponent(object):

    def __init__(self):    
        core.openflow.addListeners(self)
        #self.dynamic = DynamicController(event.connection)
	self.dynamic = DynamicController()

    def _handle_ConnectionUp(self, event):
        log.debug("Connection %s" % (event.connection))
	self.dynamic.add_connection_object(event.connection)

    def _handle_ConnectionDown(self,event):
        self.dynamic.close_connection()

def launch ():
  """
  Starts an L2 learning switch.
  """  
  core.registerNew(CentralComponent)


  #core.openflow.addListenerByName("ConnectionUp", _init_datapath, priority=2, once=False)
