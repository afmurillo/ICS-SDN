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
        defaultIP = '192.168.1.254/24'  # IP address for r0-eth1
        router = self.addNode( 'r0', cls=LinuxRouter, ip=defaultIP )

        # Add switches
        s1, s2, s3  = [ self.addSwitch( s ) for s in ( 's1', 's2', 's3' ) ]

        self.addLink( s1, router, intfName2='r0-eth1', params2={ 'ip' : defaultIP } )  
        self.addLink( s2, router, intfName2='r0-eth2', params2={ 'ip' : '192.168.2.254/24' } )
        self.addLink( s3, router, intfName2='r0-eth3', params2={ 'ip' : '192.168.3.254/24' } )

        gateway_1 = 'via ' + defaultIP
 
        p101 = self.addHost('p101', ip=IP['p101'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")
        mv101 = self.addHost('mv101',ip=IP['mv101'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")
        lit101 = self.addHost('lit101',ip=IP['lit101'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")
        plc101 = self.addHost('plc101',ip=IP['plc101'] + NETMASK, defaultRoute=gateway_1 )
        ids101 = self.addHost('ids101',ip=IP['ids101'] + NETMASK, defaultRoute=gateway_1 )
        sim101 = self.addHost('sim101',ip=IP['sim101'] + NETMASK, defaultRoute=gateway_1 )
        plant101 = self.addHost('plant101')

        self.addLink(p101, s1)
        self.addLink(mv101, s1)
        self.addLink(lit101, s1)
        self.addLink(plc101, s1)
        self.addLink(ids101, s1)
        self.addLink(sim101, s1)

        gateway_2 = 'via ' + '192.168.2.254/24'

        fit201 = self.addHost('fit201',ip=IP['fit201'] + NETMASK, defaultRoute=gateway_2)#, defaultRoute="via 192.168.2.10")
        ph201 = self.addHost('ph201',ip=IP['ph201'] + NETMASK, defaultRoute=gateway_2)#, defaultRoute="via 192.168.2.10")
        p201 = self.addHost('p201',ip=IP['p201'] + NETMASK, defaultRoute=gateway_2)#, defaultRoute="via 192.168.2.10")
      
        plc201 = self.addHost('plc201',ip=IP['plc201'] + NETMASK, defaultRoute=gateway_2)

        self.addLink(fit201, s2)
        self.addLink(ph201, s2)
        self.addLink(p201, s2)


        self.addLink(plc201, s2)

        gateway_3 = 'via ' + '192.168.3.254/24'

        lit301 = self.addHost('lit301',ip=IP['lit301'] + NETMASK, defaultRoute=gateway_3)#, defaultRoute="via 192.168.3.10")
        p301 = self.addHost('p301',ip=IP['p301'] + NETMASK, defaultRoute=gateway_3)#, defaultRoute="via 192.168.3.10")
        plc301 = self.addHost('plc301',ip=IP['plc301'] + NETMASK, defaultRoute=gateway_3)

        self.addLink(lit301, s3)        
        self.addLink(p301, s3)                
        self.addLink(plc301, s3)      

