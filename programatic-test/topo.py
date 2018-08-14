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
        #defaultIP = '192.168.1.254/24'  # IP address for r0-eth1
	#router = self.addNode( 'r0', cls=LinuxRouter, ip=defaultIP )
        # Add switches
        s2 = self.addSwitch( 's2' )
        gateway_2 = 'via ' + IP['plc201'] + NETMASK#'192.168.2.254/24'

        fit201 = self.addHost('fit201',ip=IP['fit201'] + NETMASK, defaultRoute=gateway_2)#, defaultRoute="via 192.168.2.10")
        ph201 = self.addHost('ph201',ip=IP['ph201'] + NETMASK, defaultRoute=gateway_2)#, defaultRoute="via 192.168.2.10")
        p201 = self.addHost('p201',ip=IP['p201'] + NETMASK, defaultRoute=gateway_2)#, defaultRoute="via 192.168.2.10")
      
        plc201 = self.addHost('plc201',ip=IP['plc201'] + NETMASK, cls=LinuxRouter)
        self.addLink( s2, plc201, intfName2='plc201-eth1', params2={ 'ip' : '192.168.2.254/24' } )

        self.addLink(fit201, s2)
        self.addLink(ph201, s2)
        self.addLink(p201, s2)

