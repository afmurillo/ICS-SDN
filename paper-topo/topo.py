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
        defaultIP = IP['plc101']+NETMASK
	#router = self.addNode( 'r0', cls=LinuxRouter, ip=defaultIP )
        host = self.addHost('hmi', ip='192.168.4.4/24')

        # Add switches
        s1, s2, s3, s4  = [ self.addSwitch( s ) for s in ('s1', 's2', 's3', 's4') ]
        self.addLink(host, s4)

        gateway_1 = 'via ' + defaultIP
 
        plc101 = self.addNode('plc101',ip=IP['plc101'] + NETMASK, cls=LinuxRouter)
        self.addLink( s1, plc101, intfName2='plc101-eth1', params2={ 'ip' : defaultIP } )  
        self.addLink( s4, plc101, intfName2='plc101-eth2', params2={ 'ip' : '192.168.4.1/24' } )

        p101 = self.addHost('p101', ip=IP['p101'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")
        mv101 = self.addHost('mv101',ip=IP['mv101'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")
        lit101 = self.addHost('lit101',ip=IP['lit101'] + NETMASK, defaultRoute=gateway_1 )#, defaultRoute="via 192.168.1.11")
        ids101 = self.addHost('ids101',ip=IP['ids101'] + NETMASK, defaultRoute=gateway_1 )
        sim101 = self.addHost('sim101',ip=IP['sim101'] + NETMASK, defaultRoute=gateway_1 )
        plant101 = self.addHost('plant101')

        self.addLink(p101, s1)
        self.addLink(mv101, s1)
        self.addLink(lit101, s1)
        #self.addLink(plc101, s1)
        self.addLink(ids101, s1)
        self.addLink(sim101, s1)
        #self.addLink(plc1, sdns)

        gateway_2 = 'via ' + IP['plc201'] + NETMASK#'192.168.2.254/24'

        fit201 = self.addHost('fit201',ip=IP['fit201'] + NETMASK, defaultRoute=gateway_2)#, defaultRoute="via 192.168.2.10")
        ph201 = self.addHost('ph201',ip=IP['ph201'] + NETMASK, defaultRoute=gateway_2)#, defaultRoute="via 192.168.2.10")
        p201 = self.addHost('p201',ip=IP['p201'] + NETMASK, defaultRoute=gateway_2)#, defaultRoute="via 192.168.2.10")
        #ids201 = self.addHost('ids201',ip=IP['ids201'] + NETMASK, defaultRoute=gateway_2)#, defaultRoute="via 192.168.2.10")
        #sim201 = self.addHost('sim201',ip=IP['sim201'] + NETMASK, defaultRoute=gateway_2)#, defaultRoute="via 192.168.2.10")
      
        plc201 = self.addHost('plc201',ip=IP['plc201'] + NETMASK, cls=LinuxRouter)
        self.addLink( s2, plc201, intfName2='plc201-eth1', params2={ 'ip' : '192.168.2.254/24' } )
        self.addLink( s4, plc201, intfName2='plc201-eth2', params2={ 'ip' : '192.168.4.2/24' } )
        #plant201 = self.addHost('plant201')

        self.addLink(fit201, s2)
        self.addLink(ph201, s2)
        self.addLink(p201, s2)
        #self.addLink(ids201, s2)
        #self.addLink(sim201, s2)

        #self.addLink(plc201, s2)
        #self.addLink(plc2, sdns)

        gateway_3 = 'via ' + IP['plc301'] + NETMASK#'192.168.3.254/24'

        plc301 = self.addNode('plc301',ip=IP['plc301'] + NETMASK, cls=LinuxRouter)
        self.addLink( s3, plc301, intfName2='plc301-eth1', params2={ 'ip' : '192.168.3.254/24' } )
        self.addLink( s4, plc301, intfName2='plc301-eth2', params2={ 'ip' : '192.168.4.3/24' } )

        lit301 = self.addHost('lit301',ip=IP['lit301'] + NETMASK, defaultRoute=gateway_3)#, defaultRoute="via 192.168.3.10")
        p301 = self.addHost('p301',ip=IP['p301'] + NETMASK, defaultRoute=gateway_3)#, defaultRoute="via 192.168.3.10")
        ids301 = self.addHost('ids301',ip=IP['ids301'] + NETMASK, defaultRoute=gateway_2)#, defaultRoute="via 192.168.2.10")
        #sim301 = self.addHost('sim301',ip=IP['sim301'] + NETMASK, defaultRoute=gateway_2)#, defaultRoute="via 192.168.2.10")
        #plant301 = self.addHost('plant301')


        self.addLink(lit301, s3)        
        self.addLink(p301, s3)                
        #self.addLink(plc301, s3)      
        self.addLink(ids301, s3)        
        #self.addLink(sim301, s3)

	self.addLink( s4, ids301, intfName2='ids301-eth3', params2={ 'ip' : '192.168.4.20/24' } )

