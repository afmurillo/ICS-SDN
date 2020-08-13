#!/usr/bin/env python3
'''
Simple module which provides a class to sniff traffic and extract data from Ethernet/IP packets.
An additional class that provides some basic CLI is also implemented.
'''

from struct import unpack
from binascii import hexlify
from os import geteuid
from threading import Thread, Event
from collections import deque, OrderedDict
from sys import stdout
from cmd import Cmd
from json import load, loads
from scapy.all import sniff, Packet
from scapy.data import IP_PROTOS
from scapy.layers.inet import IP, TCP, UDP
import requests
from requests.auth import HTTPBasicAuth
from enipcip.enip_tcp import ENIP_TCP, ENIP_SendRRData
from enipcip.enip_udp import ENIP_UDP
from enipcip.cip import CIP # pylint: disable=W0611

CONTROLLER_IP = '192.168.56.50'
CONTROLLER_PORT = 6633
REST_PORT = 8181
REST_USER = 'onos'
REST_PASS = 'rocks'
LOCAL_PROTOS = {}

for k in IP_PROTOS.keys():
    LOCAL_PROTOS[IP_PROTOS[k]] = str(k).upper()

class ICSSniffer(Thread):
    '''This class executes as a separate thread and is intended to read up to 65536 Ethernet/IP messages.

    Upon execution, this class will start a network sniffer using Scapy and it will capture every 'SendRRData'
    message, extracting the data being sent and storing the message in a buffer.'''

    ENIP_COMMANDS = {
        0x0000: 'NOP',
        0x0004: 'List Services',
        0x0063: 'List Identity',
        0x0064: 'List Interfaces',
        0x0065: 'Register Session',
        0x0066: 'Unregister Session',
        0x006f: 'Send RR data',
        0x0070: 'Send Unit data',
        0x0072: 'Indicate status',
        0x0073: 'Cancel',
    }

    ENIP_STATUS = {
        0x0000: 'Success',
        0x0001: 'Invalid/Unsupported command',
        0x0002: 'Insufficient memory in the receiver',
        0x0003: 'Incorrect data',
        0x0064: 'Invalid session handle',
        0x0065: 'Invalid length',
        0x0069: 'Unsupported protocol',
    }

    CIP_ITEM_ID = {
        0x0000: 'Null',
        0x000c: 'List Identity response',
        0x00a1: 'Connection-based',
        0x00b1: 'Connected transport packet',
        0x00b2: 'Unconnected message',
        0x0100: 'List Services response',
        0x8000: 'Sockaddr Info, originator -> target',
        0x8001: 'Sockaddr Info, target -> originator',
        0x8002: 'Sequenced Address item'
    }

    def __init__(self, interface: str):
        Thread.__init__(self)
        self.setName('sniffer')                                 # Thread name
        self.should_stop = Event()                              # Interrupt event
        self.__iface = interface                                # The network interface in which the sniffer will be started
        self.__messages = deque(iterable=[], maxlen=65536)      # Message queue
        self.__packet_stats = {}                                # IP traffic statistics

    @staticmethod
    def read_cip_tag(tagtype: int, tagdata: bytes) -> dict:
        '''Convert a given CIP tag type and raw value into the corresponding representation.

        Keyword arguments:
        tagtype -- The data type as specified by the CIP
                    0xC1 :: Boolean (1 byte)
                    0xC2 :: Signed small integer        (1 byte)
                    0xC3 :: Signed integer              (2 bytes)
                    0xC4 :: Signed Double integer       (4 bytes)
                    0xC5 :: Signed long integer         (8 bytes)
                    0xC6 :: Unsigned small integer      (1 byte)
                    0xC7 :: Unsigned integer            (2 bytes)
                    0xC8 :: Unsigned double integer     (4 bytes)
                    0xC9 :: Unsigned long integer       (8 bytes)
                    0xCA :: Real [float]                (4 bytes)
                    0xCB :: Long real [double]          (8 bytes)
        tagdata -- The raw bytes representing the value'''
        ttype = (tagtype & 0xff)
        if not ttype ^ 0xc1: # BOOL (1 byte)
            data = unpack('B', tagdata)[0]
            pos = int((tagtype & 0x0f00) / 0x0100)
            return {'type': 'bool', 'value': bool(data & 2 ** pos)}
        elif not ttype ^ 0xc2: # SINT (1 byte)
            return {'type': 'sint', 'value': unpack('b', tagdata)[0]}
        elif not ttype ^ 0xc3: # INT (2 bytes)
            return {'type': 'int', 'value': unpack('<h', tagdata)[0]}
        elif not ttype ^ 0xc4: # DINT (4 bytes)
            return {'type': 'dint', 'value': unpack('<i', tagdata)[0]}
        elif not ttype ^ 0xc5: # LINT (8 bytes)
            return {'type': 'lint', 'value': unpack('<q', tagdata)[0]}
        elif not ttype ^ 0xc6: # USINT (1 byte)
            return {'type': 'usint', 'value': unpack('B', tagdata)[0]}
        elif not ttype ^ 0xc7: # UINT (2 bytes)
            return {'type': 'uint', 'value': unpack('<H', tagdata)[0]}
        elif not ttype ^ 0xc8: # UDINT (4 bytes)
            return {'type': 'udint', 'value': unpack('<I', tagdata)[0]}
        elif not ttype ^ 0xc9: # ULINT (8 bytes)
            return {'type': 'ulint', 'value': unpack('<Q', tagdata)[0]}
        elif not ttype ^ 0xca: # REAL (4 bytes)
            return {'type': 'real', 'value': unpack('<f', tagdata)[0]}
        elif not ttype ^ 0xcb: # LREAL (8 bytes)
            return {'type': 'lreal', 'value': unpack('<d', tagdata)[0]}
        else:
            return None

    @staticmethod
    def str_cip_tag(ciptag: dict) -> str:
        '''
        Obtain a string representation of the value in a CIP tag.

        Keyword arguments:
        ciptag -- Dictionary as returned by the read_cip_tag method.
        '''
        if ciptag is None or 'type' not in ciptag.keys() or 'value' not in ciptag.keys():
            return 'NULL'
        elif ciptag['type'] in ['real', 'lreal']:
            return '{0:f}'.format(ciptag['value'])
        elif ciptag['type'] is 'bool':
            return str(ciptag['value'])
        else:
            return '{0:d}'.format(ciptag['value'])

    def __handle_pkt(self, packet: Packet) -> str:
        '''Callback method to be executed by Scapy for every sniffed packet.'''
        stat_key = None
        message = {}
        message['is_enip'] = packet.haslayer(ENIP_TCP) or packet.haslayer(ENIP_UDP)
        if packet.haslayer(ENIP_SendRRData) and packet['ENIP_SendRRData'].items[1]['CIP'].direction == 1: # Response
            message['src'] = {}
            message['dst'] = {}
            message['src']['MAC'] = str.upper(packet['Ethernet'].src)
            message['dst']['MAC'] = str.upper(packet['Ethernet'].dst)
            message['src']['IP'] = packet['IP'].src
            message['dst']['IP'] = packet['IP'].dst
            message['rawdata'] = bytes(packet['ENIP_SendRRData'].items[1]['Raw'])
            message['data'] = self.read_cip_tag(message['rawdata'][0], message['rawdata'][2:])
            message['rawdata'] = hexlify(message['rawdata']).decode('utf-8')
            if packet.haslayer(TCP):
                stat_key = '{0:s}:{1:d}/{2:s}:{3:d}/TCP'.format(
                    packet['IP'].src,
                    packet['TCP'].sport,
                    packet['IP'].dst,
                    packet['TCP'].dport
                )
            elif packet.haslayer(UDP):
                stat_key = '{0:s}:{1:d}/{2:s}:{3:d}/UDP'.format(
                    packet['IP'].src,
                    packet['UDP'].sport,
                    packet['IP'].dst,
                    packet['UDP'].dport
                )
            self.__messages.append(message)
        elif packet.haslayer(IP):
            message['src'] = {}
            message['dst'] = {}
            message['src']['MAC'] = str.upper(packet['Ethernet'].src)
            message['dst']['MAC'] = str.upper(packet['Ethernet'].dst)
            message['src']['IP'] = packet['IP'].src
            message['dst']['IP'] = packet['IP'].dst
            message['rawippayload'] = packet['IP'].payload
            if packet.haslayer('TCP'):
                stat_key = '{0:s}:{1:d}/{2:s}:{3:d}/TCP'.format(
                    packet['IP'].src,
                    packet['TCP'].sport,
                    packet['IP'].dst,
                    packet['TCP'].dport
                )
            elif packet.haslayer('UDP'):
                stat_key = '{0:s}:{1:d}/{2:s}:{3:d}/UDP'.format(
                    packet['IP'].src,
                    packet['UDP'].sport,
                    packet['IP'].dst,
                    packet['UDP'].dport
                )
            else:
                stat_key = '{0:s}/{1:s}/{2:s}'.format(
                    packet['IP'].src,
                    packet['IP'].dst,
                    LOCAL_PROTOS[packet['IP'].proto]
                )
            self.__messages.append(message)
        if stat_key is not None:
            if stat_key in self.__packet_stats.keys():
                self.__packet_stats[stat_key] += 1
            else:
                self.__packet_stats[stat_key] = 1
        return None

    def get_stats(self) -> OrderedDict:
        '''
        Get a sorted dictionary containing the amount of sniffed packets per second, using the timestamp as the key.
        '''
        pkts = self.__packet_stats.items()
        self.__packet_stats = {}
        stats = OrderedDict(sorted(pkts, key=lambda x: x[1], reverse=True))
        return stats

    def pop(self):
        '''Pop the next message in queue'''
        try:
            value = self.__messages.popleft()
            return value
        except IndexError:
            return None

    def size(self):
        '''Get the current length of the message queue.'''
        return len(self.__messages)

    def run(self):
        '''Override from Thread'''
        sniff(iface=self.__iface, count=0, store=0, prn=self.__handle_pkt, stop_filter=lambda p: self.should_stop.is_set())

class IDSPrompt(Cmd):
    '''Crude command line interface for the IDS. Meant as a testbed.'''

    def __init__(self, iface: str):
        Cmd.__init__(self)
        self.prompt = 'ICS SDN> '                                                                   # Prompt
        self.__iface = iface                                                                        # Network interface to be used by the sniffer
        self.__backend = None                                                                       # Sniffer
        self.__config = None                                                                        # Configuration dictionary (When loaded)
        self.__rest_auth = HTTPBasicAuth(REST_USER, REST_PASS)                                      # ONOS REST API authentication
        self.__rest_hdr = {'Accept': 'application/json'}                                          # ONOS REST API headers
        self.__rest_uri = 'http://{0:s}:{1:d}/onos/v1'.format(CONTROLLER_IP, REST_PORT)             # ONOS REST API URL
        self.__locations = {}                                                                       # SDN host locations cache

    def do_load(self, line):
        '''Load configuration variables'''
        if self.__config is not None:
            print('Discarding previous configuration ...')
        with open(line) as conf_file:
            self.__config = load(conf_file)
            print('Configuration loaded!')
            print(self.__config)

    def do_next(self, line): # pylint: disable=W0613
        '''Get the next EtherNet/IP message from the buffer'''
        if self.__backend is not None:
            msg = self.__backend.pop()
            if msg is not None:
                if 'src' in msg.keys() and 'IP' in msg['src'].keys():
                    if msg['src']['IP'] not in self.__locations.keys():             # Insert a new host within the locations cache
                        rsp = requests.get(self.__rest_uri + '/hosts/' + msg['src']['MAC'] + '/None', auth=self.__rest_auth, headers=self.__rest_hdr)
                        rsp = loads(rsp.text)
                        self.__locations[msg['src']['IP']] = rsp['locations'][0]
                    msg['src']['location'] = self.__locations[msg['src']['IP']]     # Fetch the source's location from the cache
                    if self.__config is not None:
                        for key in self.__config['IP'].keys():                        # Fetch the source's name based upon the configuration, if any
                            if msg['src']['IP'] == self.__config['IP'][key]:
                                msg['src']['name'] = key
                                break
                if 'dst' in msg.keys() and 'IP' in msg['dst'].keys():
                    if msg['dst']['IP'] not in self.__locations.keys():             # Insert a new host within the locations cache
                        rsp = requests.get(self.__rest_uri + '/hosts/' + msg['dst']['MAC'] + '/None', auth=self.__rest_auth, headers=self.__rest_hdr)
                        rsp = loads(rsp.text)
                        self.__locations[msg['dst']['IP']] = rsp['locations'][0]
                    msg['dst']['location'] = self.__locations[msg['dst']['IP']]     # Fetch the destination's location from the cache
                    if self.__config is not None:
                        for key in self.__config['IP'].keys():                        # Fetch the destination's name based upon the configuration, if any
                            if msg['dst']['IP'] == self.__config['IP'][key]:
                                msg['dst']['name'] = key
                                break
                print(msg)
            else:
                print('Empty message queue')

    def do_flush(self, line): # pylint: disable=W0613
        '''Flush all received messages'''
        queue_size = self.__backend.size()
        while queue_size > 0:                       # Empty the message queue
            self.do_next(None)
            queue_size -= 1

    def do_size(self, line): # pylint: disable=W0613
        '''Get the current size of the message buffer'''
        if self.__backend is not None:
            print(self.__backend.size())    # Display the current queue size
        else:
            print('No message queue')

    def do_start(self, arg): # pylint: disable=W0613
        '''Start the network sniffer'''
        if self.__backend is not None and self.__backend.is_alive():    # The sniffer is up and running, no need to start it again
            print('Sniffer is already running.')
        else:
            try:                                                        # Attempt to start a new instance of a sniffer class
                if self.__backend is not None:
                    self.__backend = None
                self.__backend = ICSSniffer(self.__iface)               # Initialize the sniffer with the interface
                self.__backend.start()
            except RuntimeError:
                pass

    def do_stop(self, arg): # pylint: disable=W0613
        '''Stop the sniffer'''
        if self.__backend is not None and self.__backend.is_alive():
            self.__backend.should_stop.set()                            # Set the interrupt event in the sniffer
            while True:                                                 # Wait while the sniffer finishes its execution
                self.__backend.join(2)
                if self.__backend.is_alive():
                    print('Sniffer is still running ...')
                else:
                    break
        else:
            print('Sniffer is not running.')

    def do_exit(self, arg):
        '''Terminate the process'''
        if self.__backend is not None and self.__backend.is_alive():
            self.do_stop(arg)
        return True

    def do_EOF(self, arg): # pylint: disable=W0613,C0103
        '''Handle Ctrl + D (EOF)'''
        stdout.write('\r\n')
        if self.__backend is not None and self.__backend.is_alive():
            self.do_stop(arg)
        return True

    def default(self, line):
        print('Command unknown: {0:s}'.format(line))

    def emptyline(self):
        stdout.write('\x00')

def main():
    '''Testbed execution.

    A single instance of the IDSPrompt is started in order to interact with the user.

    By default, it uses the 'vboxnet1' interface as a sniffing device.'''
    prompt = IDSPrompt('vboxnet1')
    try:
        prompt.cmdloop()
    except KeyboardInterrupt:
        stdout.write('\r\n')
        prompt.do_stop(arg='')

if __name__ == '__main__':
    if geteuid() != 0:
        print('SDN IDS requires root privileges')
    else:
        main()
