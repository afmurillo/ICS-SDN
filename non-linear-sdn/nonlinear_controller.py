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
import pox.lib.packet as pkt


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

class DynamicController(object):

    def __init__(self):

        #self.connection = connection
	self.connections = []
        self.transparent = False

        # Our table
        self.macToPort = {}

        # We just use this to know when to log a helpful message
        self.hold_down_expired = 0
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

    def mirror_traffic(self, event):
        """ 
    	Mirrors traffic from LIT101 to the IDS101
	    """
	    packet=event.parsed
        #port = self.macToPort[packet.dst]
        if packet.type == ethernet.IP_TYPE:
            ip_packet=packet.payload
            print ip_packet.srcip
            if ip_packet.srcip == '192.168.1.10' and ip_packet.dstip=='192.168.1.14':
                print "this needs to be mirrored"
                msg.match = of.ofp_match.from_packet(packet, event.port)
                msg.idle_timeout = 10
                msg.hard_timeout = 30                                
                action = of.ofp_action_output(port=self.ids_port)
                msg.actions.append(action)
                msg.data = event.ofp

            else:
                return
        else:
            return

        



    def _handle_PacketIn(self, event):
        """
        Manage PacketIn events sent by event,connection datapaths.

        """
        packet = event.parsed
        log.debug("Incoming packet from port: %i", event.port)
        #print "From connection: ", str(event.dpid)

        in_port = event.port
        if ip_packet.srcip == '192.168.1.15':
                print "ids packet"
                self.ids_mac = packet.src
                self.ids_port=event.port


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
                msg.idle_timeout = 10
                msg.hard_timeout = 30                                
                action = of.ofp_action_output(port=port)
                msg.actions.append(action)
                msg.data = event.ofp

		for connection in self.connections:
            		connection.send(msg)

                mirror_traffic(event)

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
