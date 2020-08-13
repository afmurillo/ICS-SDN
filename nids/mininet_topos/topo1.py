#!/usr/bin/env python3
'''
Main topology used during the SDN tests
'''

from os import system
from time import sleep
from copy import deepcopy
import json
import requests
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import Host
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Intf

CONT_IP = '192.168.56.50'
REST_PORT = 8181
REST_USER = 'onos'
REST_PASS = 'rocks'

def create_switch_groups(rauth: requests.auth.HTTPBasicAuth):
    '''
    Create/Replace SDN groups in each switch within the topology
    '''
    uri = 'http://{0:s}:{1:d}/onos/v1/groups/of:0000000000000001'.format(CONT_IP, REST_PORT)
    # Groups for switch 1
    grp = {'type': 'ALL', 'appId': 'org.onosproject.fwd', 'buckets': []}
    grp['appCookie'] = '0x00000101'
    grp['groupId'] = '1'
    bkt = {'treatment': {}}
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '3'}]
    grp['buckets'].append(deepcopy(bkt))
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '4'}]
    grp['buckets'].append(deepcopy(bkt))
    payload = json.dumps(grp)
    requests.request('POST', uri, auth=rauth, data=payload)
    grp['buckets'] = []
    grp['appCookie'] = '0x0000010a'
    grp['groupId'] = '10'
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '3'}]
    grp['buckets'].append(deepcopy(bkt))
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '5'}]
    grp['buckets'].append(deepcopy(bkt))
    payload = json.dumps(grp)
    requests.request('POST', uri, auth=rauth, data=payload)
    grp['buckets'] = []
    grp['appCookie'] = '0x0000010b'
    grp['groupId'] = '11'
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '3'}]
    grp['buckets'].append(deepcopy(bkt))
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '6'}]
    grp['buckets'].append(deepcopy(bkt))
    payload = json.dumps(grp)
    requests.request('POST', uri, auth=rauth, data=payload)
    # Groups for switch 2
    uri = 'http://{0:s}:{1:d}/onos/v1/groups/of:0000000000000002'.format(CONT_IP, REST_PORT)
    grp['buckets'] = []
    grp['appCookie'] = '0x0000020c'
    grp['groupId'] = '12'
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '3'}]
    grp['buckets'].append(deepcopy(bkt))
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '4'}]
    grp['buckets'].append(deepcopy(bkt))
    payload = json.dumps(grp)
    requests.request('POST', uri, auth=rauth, data=payload)
    grp['buckets'] = []
    grp['appCookie'] = '0x0000020e'
    grp['groupId'] = '14'
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '3'}]
    grp['buckets'].append(deepcopy(bkt))
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '5'}]
    grp['buckets'].append(deepcopy(bkt))
    payload = json.dumps(grp)
    requests.request('POST', uri, auth=rauth, data=payload)
    grp['buckets'] = []
    grp['appCookie'] = '0x00000264'
    grp['groupId'] = '100'
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '3'}]
    grp['buckets'].append(deepcopy(bkt))
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '6'}]
    grp['buckets'].append(deepcopy(bkt))
    payload = json.dumps(grp)
    requests.request('POST', uri, auth=rauth, data=payload)
    # Groups for switch 3
    uri = 'http://{0:s}:{1:d}/onos/v1/groups/of:0000000000000003'.format(CONT_IP, REST_PORT)
    grp['buckets'] = []
    grp['appCookie'] = '0x0000030a'
    grp['groupId'] = '10'
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '3'}]
    grp['buckets'].append(deepcopy(bkt))
    bkt['treatment']['instructions'] = [{'type': 'L2MODIFICATION', 'subtype': 'ETH_DST', 'mac': '00:16:17:FE:BB:21'}, {'type': 'OUTPUT', 'port': '4'}]
    grp['buckets'].append(deepcopy(bkt))
    payload = json.dumps(grp)
    requests.request('POST', uri, auth=rauth, data=payload)
    grp['buckets'] = []
    grp['appCookie'] = '0x0000030b'
    grp['groupId'] = '11'
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '3'}]
    grp['buckets'].append(deepcopy(bkt))
    bkt['treatment']['instructions'] = [{'type': 'L2MODIFICATION', 'subtype': 'ETH_DST', 'mac': 'E4:90:69:43:CD:A2'}, {'type': 'OUTPUT', 'port': '5'}]
    grp['buckets'].append(deepcopy(bkt))
    payload = json.dumps(grp)
    requests.request('POST', uri, auth=rauth, data=payload)
    # Groups for switch 4
    uri = 'http://{0:s}:{1:d}/onos/v1/groups/of:0000000000000004'.format(CONT_IP, REST_PORT)
    grp['buckets'] = []
    grp['appCookie'] = '0x0000040c'
    grp['groupId'] = '12'
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '3'}]
    grp['buckets'].append(deepcopy(bkt))
    bkt['treatment']['instructions'] = [{'type': 'L2MODIFICATION', 'subtype': 'ETH_DST', 'mac': '00:90:E8:6F:DE:B9'}, {'type': 'OUTPUT', 'port': '4'}]
    grp['buckets'].append(deepcopy(bkt))
    payload = json.dumps(grp)
    requests.request('POST', uri, auth=rauth, data=payload)
    grp['buckets'] = []
    grp['appCookie'] = '0x0000040e'
    grp['groupId'] = '14'
    bkt['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '3'}]
    grp['buckets'].append(deepcopy(bkt))
    bkt['treatment']['instructions'] = [{'type': 'L2MODIFICATION', 'subtype': 'ETH_DST', 'mac': '08:00:06:DB:C0:1F'}, {'type': 'OUTPUT', 'port': '5'}]
    grp['buckets'].append(deepcopy(bkt))
    payload = json.dumps(grp)
    requests.request('POST', uri, auth=rauth, data=payload)

def add_bridge_flows(uri: str, rauth: requests.auth.HTTPBasicAuth):
    '''
    Add the initial flows to the bridge switch between the field network and the honeypot.
    '''
    # Initial bridge flows
    flows = {'flows': []}
    flow = {'priority': 40010, 'timeout': 0, 'isPermanent': True, 'appId': 'org.onosproject.fwd', 'deviceId': 'of:00000000000000ff'}
    # ignore all incoming traffic
    flow['treatment'] = {'instructions': [{'type': 'NOACTION'}], 'clearDeferred': True}
    flow['selector'] = {'criteria': [{'type': 'IN_PORT', 'port': '1'}]}
    flows['flows'].append(deepcopy(flow))
    flow['treatment']['instructions'] = [{'type': 'NOACTION'}]
    flow['selector'] = {'criteria': [{'type': 'IN_PORT', 'port': '2'}]}
    flows['flows'].append(deepcopy(flow))
    flow['treatment']['instructions'] = [{'type': 'NOACTION'}]
    flow['selector'] = {'criteria': [{'type': 'IN_PORT', 'port': '3'}]}
    flows['flows'].append(deepcopy(flow))
    flow['treatment']['instructions'] = [{'type': 'NOACTION'}]
    flow['selector'] = {'criteria': [{'type': 'IN_PORT', 'port': '4'}]}
    flows['flows'].append(deepcopy(flow))
    flow['priority'] = 40050
    # outbound flows to honeypot
    flow['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '3'}]
    flow['selector'] = {'criteria': [{'type': 'ETH_TYPE', 'ethType': '0x0800'}, {'type': 'IPV4_DST', 'ip': '192.168.1.10/32'}]}
    flows['flows'].append(deepcopy(flow))
    flow['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '3'}]
    flow['selector'] = {'criteria': [{'type': 'ETH_TYPE', 'ethType': '0x0800'}, {'type': 'IPV4_DST', 'ip': '192.168.1.11/32'}]}
    flows['flows'].append(deepcopy(flow))
    flow['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '4'}]
    flow['selector'] = {'criteria': [{'type': 'ETH_TYPE', 'ethType': '0x0800'}, {'type': 'IPV4_DST', 'ip': '192.168.1.12/32'}]}
    flows['flows'].append(deepcopy(flow))
    flow['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '4'}]
    flow['selector'] = {'criteria': [{'type': 'ETH_TYPE', 'ethType': '0x0800'}, {'type': 'IPV4_DST', 'ip': '192.168.1.14/32'}]}
    flows['flows'].append(deepcopy(flow))
    # outbound flow to router
    flow['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '1'}]
    flow['selector'] = {'criteria': [{'type': 'ETH_DST', 'mac': '00:01:42:a5:34:c0'}]}
    flows['flows'].append(deepcopy(flow))
    payload = json.dumps(flows)
    resp = requests.request('POST', uri, auth=rauth, data=payload)
    print(resp.text)
    sleep(0.5)

def add_mirror_flows(uri: str, rauth: requests.auth.HTTPBasicAuth):
    '''
    Add the required flows in the mirror switch to redirect all the traffic to the IDS interface.
    '''
    flows = {'flows': []}
    flow = {'priority': 40050, 'timeout': 0, 'isPermanent': True, 'appId': 'org.onosproject.fwd', 'deviceId': 'of:00000800272d1636'}
    flow['treatment'] = {'instructions': [{'type': 'OUTPUT', 'port': '1'}], 'clearDeferred': True}
    flow['selector'] = {'criteria': [{'type': 'ETH_TYPE', 'ethType': '0x0800'}]} # IPv4
    flows['flows'].append(deepcopy(flow))
    flow['selector'] = {'criteria': [{'type': 'ETH_TYPE', 'ethType': '0x0806'}]} # ARP
    flows['flows'].append(deepcopy(flow))
    flow['treatment']['instructions'] = [{'type': 'NOACTION'}]
    flow['priority'] = 40100
    flow['selector'] = {'criteria': [{'type': 'ETH_TYPE', 'ethType': '0x88cc'}]} # LLDP
    flows['flows'].append(deepcopy(flow))
    flow['selector'] = {'criteria': [{'type': 'ETH_TYPE', 'ethType': '0x8942'}]} # BDDP
    flows['flows'].append(deepcopy(flow))
    payload = json.dumps(flows)
    resp = requests.request('POST', uri, auth=rauth, data=payload)
    print(resp.text)
    sleep(0.5)

def mirror_field_switches(uri: str, rauth: requests.auth.HTTPBasicAuth):
    '''
    Add the required flows to mirror the traffic from every field switch to the mirror switch using the SDN groups.
    '''
    flows = {'flows': []}
    flow = {'priority': 40050, 'timeout': 0, 'isPermanent': True, 'appId': 'org.onosproject.fwd', 'deviceId': 'of:0000000000000001'}
    flow['treatment'] = {'instructions': [{'type': 'GROUP', 'groupId': '1'}], 'clearDeferred': True}
    flow['selector'] = {'criteria': [{'type': 'ETH_DST', 'mac': '00:01:42:A5:34:C0'}]}
    flows['flows'].append(deepcopy(flow))
    flow['treatment']['instructions'] = [{'type': 'GROUP', 'groupId': '10'}]
    flow['selector'] = {'criteria': [{'type': 'ETH_DST', 'mac': '00:16:17:FE:BA:22'}]}
    flows['flows'].append(deepcopy(flow))
    flow['treatment']['instructions'] = [{'type': 'GROUP', 'groupId': '11'}]
    flow['selector'] = {'criteria': [{'type': 'ETH_DST', 'mac': 'E4:90:69:22:CE:D7'}]}
    flows['flows'].append(deepcopy(flow))
    flow['deviceId'] = 'of:0000000000000002'
    flow['treatment']['instructions'] = [{'type': 'GROUP', 'groupId': '12'}]
    flow['selector'] = {'criteria': [{'type': 'ETH_DST', 'mac': '00:90:E8:88:1E:53'}]}
    flows['flows'].append(deepcopy(flow))
    flow['treatment']['instructions'] = [{'type': 'GROUP', 'groupId': '14'}]
    flow['selector'] = {'criteria': [{'type': 'ETH_DST', 'mac': '08:00:06:67:AE:C4'}]}
    flows['flows'].append(deepcopy(flow))
    flow['treatment']['instructions'] = [{'type': 'GROUP', 'groupId': '100'}]
    flow['selector'] = {'criteria': [{'type': 'ETH_DST', 'mac': '00:01:6C:22:4C:A5'}]}
    flows['flows'].append(deepcopy(flow))
    payload = json.dumps(flows)
    resp = requests.request('POST', uri, auth=rauth, data=payload)
    print(resp.text)
    sleep(0.5)

def mirror_honeypot_switches(uri: str, rauth: requests.auth.HTTPBasicAuth):
    '''
    Add the required flows to mirror the traffic from every honeypot switch to the mirror switch using the SDN groups.
    '''
    flows = {'flows': []}
    flow = {'priority': 40050, 'timeout': 0, 'isPermanent': True, 'appId': 'org.onosproject.fwd', 'deviceId': 'of:0000000000000003'}
    flow['treatment'] = {'instructions': [{'type': 'GROUP', 'groupId': '10'}], 'clearDeferred': True}
    flow['selector'] = {'criteria': [{'type': 'ETH_TYPE', 'ethType': '0x0800'}, {'type': 'IPV4_DST', 'ip': '192.168.1.10/32'}]}
    flows['flows'].append(deepcopy(flow))
    flow['treatment']['instructions'] = [{'type': 'GROUP', 'groupId': '11'}]
    flow['selector'] = {'criteria': [{'type': 'ETH_TYPE', 'ethType': '0x0800'}, {'type': 'IPV4_DST', 'ip': '192.168.1.11/32'}]}
    flows['flows'].append(deepcopy(flow))
    flow['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '2'}]
    flow['selector'] = {'criteria': [{'type': 'ETH_DST', 'mac': '00:01:42:a5:34:c0'}]}
    flows['flows'].append(deepcopy(flow))
    flow['deviceId'] = 'of:0000000000000004'
    flow['treatment']['instructions'] = [{'type': 'GROUP', 'groupId': '12'}]
    flow['selector'] = {'criteria': [{'type': 'ETH_TYPE', 'ethType': '0x0800'}, {'type': 'IPV4_DST', 'ip': '192.168.1.12/32'}]}
    flows['flows'].append(deepcopy(flow))
    flow['treatment']['instructions'] = [{'type': 'GROUP', 'groupId': '14'}]
    flow['selector'] = {'criteria': [{'type': 'ETH_TYPE', 'ethType': '0x0800'}, {'type': 'IPV4_DST', 'ip': '192.168.1.14/32'}]}
    flows['flows'].append(deepcopy(flow))
    flow['treatment']['instructions'] = [{'type': 'OUTPUT', 'port': '2'}]
    flow['selector'] = {'criteria': [{'type': 'ETH_DST', 'mac': '00:01:42:a5:34:c0'}]}
    flows['flows'].append(deepcopy(flow))
    payload = json.dumps(flows)
    resp = requests.request('POST', uri, auth=rauth, data=payload)
    print(resp.text)
    sleep(0.5)

def main(): # pylint: disable=R0914,R0915
    '''main'''

    net = Mininet(topo=None, build=False, autoSetMacs=False)

    info('*** Adding controller\n')
    cont0 = net.addController(name='c0', controller=RemoteController, ip=CONT_IP, protocol='tcp', port=6633)

    info('*** Add switches\n')
    sw_1 = net.addSwitch('s1', dpid='0000000000000001', cls=OVSKernelSwitch)
    sw_2 = net.addSwitch('s2', dpid='0000000000000002', cls=OVSKernelSwitch)
    sw_3 = net.addSwitch('s3', dpid='0000000000000003', cls=OVSKernelSwitch)
    sw_4 = net.addSwitch('s4', dpid='0000000000000004', cls=OVSKernelSwitch)
    sw_5 = net.addSwitch('s5', dpid='0000000000000101', cls=OVSKernelSwitch)
    sw_b = net.addSwitch('sbr', dpid='00000000000000ff', cls=OVSKernelSwitch)
    sw_sp = net.addSwitch('span', dpid='00000800272d1636', cls=OVSKernelSwitch)
    Intf('eth2', node=sw_sp) # Physical SPAN iface

    info('*** Add hosts\n')
    #cisco              00:01:42:
    #foxconn		    00:01:6c:
    #msi		        00:16:17:
    #siemens		    00:1f:f8:
    #moxa		        00:90:e8:
    #broadcom	        d4:01:29:
    #rockwell	        e4:90:69:
    hst_1 = net.addHost('h1', cls=Host, ip='192.168.1.10', mac='00:16:17:fe:ba:22', defaultRoute='via 192.168.1.1') # LIT101
    hst_2 = net.addHost('h2', cls=Host, ip='192.168.1.11', mac='e4:90:69:22:ce:d7', defaultRoute='via 192.168.1.1') # MV101
    hst_3 = net.addHost('h3', cls=Host, ip='192.168.1.12', mac='00:90:e8:88:1e:53', defaultRoute='via 192.168.1.1') # P101
    hst_4 = net.addHost('h4', cls=Host, ip='192.168.1.14', mac='08:00:06:67:ae:c4', defaultRoute='via 192.168.1.1') # PLC101
    atk_1 = net.addHost('a1', cls=Host, ip='192.168.1.100', mac='00:01:6c:22:4c:a5', defaultRoute='via 192.168.1.1')
    hst_5 = net.addHost('h5', cls=Host, ip='192.168.1.10', mac='00:16:17:fe:bb:21', defaultRoute='via 192.168.1.1') # LIT101    honeypot
    hst_6 = net.addHost('h6', cls=Host, ip='192.168.1.11', mac='e4:90:69:43:cd:a2', defaultRoute='via 192.168.1.1') # MV101     honeypot
    hst_7 = net.addHost('h7', cls=Host, ip='192.168.1.12', mac='00:90:e8:6f:de:b9', defaultRoute='via 192.168.1.1') # P101      honeypot
    hst_8 = net.addHost('h8', cls=Host, ip='192.168.1.14', mac='08:00:06:db:c0:1f', defaultRoute='via 192.168.1.1') # PLC101    honeypot
    hst_9 = net.addHost('h9', cls=Host, ip='10.0.0.10/24', mac='00:01:6c:55:a7:cb', defaultRoute='via 10.0.0.1')
    hst_10 = net.addHost('h10', cls=Host, ip='10.0.0.11/24', mac='00:01:6c:3a:da:f2', defaultRoute='via 10.0.0.1')
    # Router to corporate
    rt_0 = net.addHost('r0', cls=Host, ip='192.168.1.1/24', defaultRoute=None)
    rt_0.cmd('sysctl net.ipv4.ip_forward=1')

    info('*** Add links\n')
    # Field
    net.addLink(sw_1, sw_2)
    # Honey
    net.addLink(sw_4, sw_3)
    # Bridge
    net.addLink(sw_1, sw_b)
    net.addLink(sw_2, sw_b)
    net.addLink(sw_3, sw_b)
    net.addLink(sw_4, sw_b)
    # SPAN
    net.addLink(sw_1, sw_sp)
    net.addLink(sw_2, sw_sp)
    net.addLink(sw_3, sw_sp)
    net.addLink(sw_4, sw_sp)
    # Router
    net.addLink(sw_1, rt_0, intfName2='r0-eth1', addr2='00:01:42:a5:34:c0')
    net.addLink(sw_5, rt_0, intfName2='r0-eth2', addr2='00:01:42:a5:34:c1')
    rt_0.cmd('ifconfig r0-eth1 192.168.1.1/24 up')
    rt_0.cmd('ifconfig r0-eth2 10.0.0.1/24 up')
    # Hosts
    net.addLink(hst_1, sw_1)
    net.addLink(hst_2, sw_1)
    net.addLink(hst_3, sw_2)
    net.addLink(hst_4, sw_2)
    net.addLink(atk_1, sw_2)
    net.addLink(hst_5, sw_3)
    net.addLink(hst_6, sw_3)
    net.addLink(hst_7, sw_4)
    net.addLink(hst_8, sw_4)
    net.addLink(hst_9, sw_5)
    net.addLink(hst_10, sw_5)

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('span').start([cont0])
    net.get('sbr').start([cont0])
    net.get('s1').start([cont0])
    net.get('s2').start([cont0])
    net.get('s3').start([cont0])
    net.get('s4').start([cont0])
    net.get('s5').start([cont0])

    info('*** Post configure switches and hosts\n')

    # Gateway static ARP for the honeypot
    hst_5.cmd('arp -s 192.168.1.1 00:01:42:a5:34:c0')
    hst_6.cmd('arp -s 192.168.1.1 00:01:42:a5:34:c0')
    hst_7.cmd('arp -s 192.168.1.1 00:01:42:a5:34:c0')
    hst_8.cmd('arp -s 192.168.1.1 00:01:42:a5:34:c0')

    info('*** Add required SDN configurations\n')
    rauth = requests.auth.HTTPBasicAuth(REST_USER, REST_PASS) # REST API authentication
    # SDN switch groups
    create_switch_groups(rauth)

    # Flows
    uri = 'http://{0:s}:{1:d}/onos/v1/flows?appId=org.onosproject.fwd'.format(CONT_IP, REST_PORT)

    # Basic bridge flows
    add_bridge_flows(uri, rauth) # Upon startup, the bridge sould ignore all the traffic and establish some basic flows towards the gateway and honeypot.

    # Mirror flows
    add_mirror_flows(uri, rauth) # Basic flows in the mirror switch: Ignore incoming flows and redirect all traffic to mirror port (NIC in IDS)

    # Field network mirroring
    mirror_field_switches(uri, rauth) # Mirror all traffic in the field switches toward the mirror switch via the SDN groups.

    # Honeypot mirroring
    mirror_honeypot_switches(uri, rauth) # Mirror all traffic in the honeypot switches toward the mirror switch via the SDN groups.

    net.pingAll()

    info('*** Start ICS processes\n')
    icscwd = '/home/mininet/topoics/'
    hnycwd = '/home/mininet/topohny/'
    hst_1_proc = hst_1.popen('python2 lit101.py &', cwd=icscwd)
    hst_5_proc = hst_5.popen('python2 lit101.py &', cwd=hnycwd)
    sleep(0.333)
    hst_4_proc = hst_4.popen('python2 plc101.py &', cwd=icscwd)
    hst_8_proc = hst_8.popen('python2 plc101.py &', cwd=hnycwd)
    sleep(0.333)
    hst_3_proc = hst_3.popen('python2 p101.py &', cwd=icscwd)
    hst_7_proc = hst_7.popen('python2 p101.py &', cwd=hnycwd)
    sleep(0.333)
    hst_2_proc = hst_2.popen('python2 mv101.py &', cwd=icscwd)
    hst_6_proc = hst_6.popen('python2 mv101.py &', cwd=hnycwd)

    CLI(net)

    # Cleanup flows
    i = 3
    while i > 0:
        uri = 'http://{0:s}:{1:d}/onos/v1/flows/application/org.onosproject.fwd'.format(CONT_IP, REST_PORT)
        requests.request('DELETE', uri, auth=rauth)
        uri = 'http://{0:s}:{1:d}/onos/v1/flows/application/org.onosproject.rest'.format(CONT_IP, REST_PORT)
        requests.request('DELETE', uri, auth=rauth)
        sleep(0.3333)
        i -= 1

    hst_1_proc.terminate()
    hst_2_proc.terminate()
    hst_3_proc.terminate()
    hst_4_proc.terminate()
    hst_5_proc.terminate()
    hst_6_proc.terminate()
    hst_7_proc.terminate()
    hst_8_proc.terminate()

    net.stop()

    rt_0.cmd('sysctl net.ipv4.ip_forward=0')

    system('mn -c')

if __name__ == '__main__':
    setLogLevel('info')
    main()
