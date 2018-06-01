from mininet.node import Node
from mininet.topo import Topo
from utils import IP, NETMASK

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class SimpleTopo(Topo):
    """
        dynamic-reconf topology
    """ 

    def build(self):

        # Add router
        defaultIP = IP['plc101']+NETMASK


        # Add switches
	s1 = self.addSwitch('s1')

        gateway_1 = 'via ' + defaultIP
 
        plc101 = self.addNode('plc101',ip=IP['plc101'] + NETMASK, cls=LinuxRouter)
        self.addLink( s1, plc101, intfName2='plc101-eth1', params2={ 'ip' : defaultIP } )  

        q101 = self.addHost('q101', ip=IP['q101'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")
        q102 = self.addHost('q102',ip=IP['q102'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")

        lit101 = self.addHost('lit101',ip=IP['lit101'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")
        lit102 = self.addHost('lit102',ip=IP['lit102'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")
        lit103 = self.addHost('lit103',ip=IP['lit103'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")

        ids101 = self.addHost('ids101',ip=IP['ids101'] + NETMASK, defaultRoute=gateway_1 )
        sim101 = self.addHost('sim101',ip=IP['sim101'] + NETMASK, defaultRoute=gateway_1 )
        plant101 = self.addHost('plant101')

        self.addLink(q101, s1)
        self.addLink(lit101, s1)
        self.addLink(lit102, s1)
        self.addLink(lit103, s1)
        self.addLink(q102, s1)
    
        self.addLink(ids101, s1)
        self.addLink(sim101, s1)
      
