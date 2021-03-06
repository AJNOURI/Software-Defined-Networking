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
        max_hosts = 50  
      
        # This is the interface to which miininet OpenVirtual Switch will be connected to to get to the outside world.  
        newIntf = 'eth1'  
      
        # Generating hosts and connecting them to switch s1  
        host_list = {}  
        info( '*** Add hosts\n')  
        for i in xrange(1,max_hosts+1):  
            host_list[i] = net.addHost('h'+str(i))  
            info( '*** Add links between ',host_list[i],' and s1 \r')  
            net.addLink(host_list[i], s1)  
      
      
        # Make sure the interface (eth1) connected to GNS3 device is up and no IP configured.  
        info( '*** Checking the interface ', newIntf, '\n' )  
        checkIntf( newIntf )  
        switch = net.switches[ 0 ]  
        info( '*** Adding', newIntf, 'to switch', switch.name, '\n' )   
        brintf = Intf( newIntf, node=switch )  
      
        info( '*** Starting network\n')  
        net.start()  
        
        # Configuring each host interface to get its IP inf. from DHCP  
        for i in xrange(1,max_hosts+1):  
            info( '*** setting host for dhcp ', host_list[i], '\r' )   
            host_list[i].cmd('dhclient ' + str(host_list[i]) + '-eth0 &')  
          
        CLI(net)  
        net.stop()  
      
    if __name__ == '__main__':  
        setLogLevel( 'info' )  
        myNetwork()  
