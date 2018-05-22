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
        defaultIP ='192.168.1.14/24'

        # Add switches
	s1 = self.addSwitch('s1')

        gateway_1 = 'via ' + defaultIP
 
        h1 = self.addNode('h1',ip=IP['h1'] + NETMASK, cls=LinuxRouter)
        self.addLink( s1, h1, intfName2='h1-eth1', params2={ 'ip' : defaultIP } )  

        h2 = self.addHost('h2', ip=IP['h2'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")
        h3 = self.addHost('h3',ip=IP['h3'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")
        h4 = self.addHost('h4',ip=IP['h4'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s1)