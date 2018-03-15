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
        s1, s2, s3  = [ self.addSwitch( s ) for s in ('s1', 's2', 's3') ]

        gateway_1 = 'via ' + defaultIP
 
        plc101 = self.addNode('plc101',ip=IP['plc101'] + NETMASK, cls=LinuxRouter)
        self.addLink( s1, plc101, intfName2='plc101-eth1', params2={ 'ip' : defaultIP } )  

        p101 = self.addHost('p101', ip=IP['p101'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")
        mv101 = self.addHost('mv101',ip=IP['mv101'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")
        lit101 = self.addHost('lit101',ip=IP['lit101'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")
        ids101 = self.addHost('ids101',ip=IP['ids101'] + NETMASK, defaultRoute=gateway_1 )
        sim101 = self.addHost('sim101',ip=IP['sim101'] + NETMASK, defaultRoute=gateway_1 )
        plant101 = self.addHost('plant101')

        self.addLink(p101, s1)
        self.addLink(mv101, s1)
        self.addLink(lit101, s1)
    
        self.addLink(ids101, s1)
        self.addLink(sim101, s1)
      
        gateway_3 = 'via ' + IP['plc301'] + NETMASK#'192.168.3.254/24'

        plc301 = self.addNode('plc301',ip=IP['plc301'] + NETMASK, cls=LinuxRouter)
        self.addLink( s3, plc301, intfName2='plc301-eth1', params2={ 'ip' : '192.168.3.254/24' } )

        lit301 = self.addHost('lit301',ip=IP['lit301'] + NETMASK, defaultRoute=gateway_3)#, defaultRoute="via 192.168.3.10")
        p301 = self.addHost('p301',ip=IP['p301'] + NETMASK, defaultRoute=gateway_3)#, defaultRoute="via 192.168.3.10")

        self.addLink(lit301, s3)        
        self.addLink(p301, s3)                
