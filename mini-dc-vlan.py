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
    s2 = net.addSwitch('s2')
  
    
    newIntf10 = 'tap0'
    newIntf20 = 'tap1'
    #Intf( newIntf, node=s1 )

    info( '*** Add hosts\n')
    h1 = net.addHost('h1')
    info( '*** Add links\n')
    net.addLink(h1, s1)


    info( '*** Add hosts\n')
    h2 = net.addHost('h2')
    info( '*** Add links\n')
    net.addLink(h2, s2)

  
    info( '*** Checking bridge interface ', newIntf10, '\n' )
    checkIntf( newIntf10 )

    switch1 = net.switches[ 0 ]
    info( '*** Adding', newIntf10, 'to switch', switch1.name, '\n' ) 
    brintf1 = Intf( newIntf10, node=switch1 )
    #switch1.addIntf( newIntf10 )

    info( '*** Checking bridge interface ', newIntf20, '\n' )
    checkIntf( newIntf20 )

    switch2 = net.switches[ 1 ]
    info( '*** Adding', newIntf20, 'to switch', switch2.name, '\n' ) 
    brintf2 = Intf( newIntf20, node=switch2 )
    #switch2.addIntf( newIntf20 )


    
    info( '*** Starting network\n')
    net.start()

    info ( '*** Set hosts IP addresse s\n') 
    h1.setIP('192.168.10.1','24')
    h2.setIP('192.168.20.1','24')



    #h1.cmdPrint('dhclient '+h1.defaultIntf().name)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
