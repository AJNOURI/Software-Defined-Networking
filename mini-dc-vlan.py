#!/usr/bin/python

import re
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info, error
from mininet.util import quietRun

def checkIntf( intf ):
    "Make sure intf exists and is not configured."
    if ( ' %s:' % intf ) not in quietRun( 'ip link show' ):
        error( 'Error:', intf, 'does not exist!\n' )
        exit( 1 )
    ips = re.findall( r'\d+\.\d+\.\d+\.\d+', quietRun( 'ifconfig ' + intf ) )
    if ips:
        error( 'Error:', intf, 'has an IP address and is probably in use!\n' )
        exit( 1 )


def myNetwork():

    net = Mininet( topo=None,
                   build=False)

    info( '*** Adding controller\n' )
    net.addController(name='c0')

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1')


    newIntf = 'eth1'
    #Intf( newIntf, node=s1 )

    info( '*** Add hosts\n')
    
    h1 = net.addHost('h1')
    #h1 = net.addHost('h1', ip='192.168.3.101/24')
   

    h1.cmd('ip a a 192.168.4.1/24 dev h1-eth0')
    info( '*** Add links\n')
    net.addLink(h1, s1)

    
    info( '*** Checking', newIntf, '\n' )
    checkIntf( newIntf )

    switch = net.switches[ 0 ]
    info( '*** Adding', newIntf, 'to switch', switch.name, '\n' ) 
    #switch.addIntf('eth1')

    brintf = Intf( newIntf, node=switch )
    
    info( '*** Starting network\n')
    net.start()
    #h1.cmdPrint('dhclient '+h1.defaultIntf().name)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

