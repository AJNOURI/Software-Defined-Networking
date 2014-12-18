from mininet.net import Mininet
from mininet.topo import LinearTopo
import mininet.util #import all #createLink
#1) Define an object for a pre-fefined type of topology
#Linear = LinearTopo(k=4)

#2) Define an object for the network
#network = Mininet(topo=Linear)

#3)Create a class for your totpology
# that create the networking device (switches) and loops to connect
# hosts to switches
# ex: Full mesh switches
# mix of topologies (how switches are connected)

#4) linker procedure
#receives list of pair list and links all pairs
# Add possibility to define BW characteristics for each pai


net = Mininet()


# Creating nodes
c0 = net.addController()
h3 = net.addHost('h3')
h4 = net.addHost('h4')
h5 = net.addHost('h5')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')

# Creating links between nodes
net.addLink(h3,s1)
net.addLink(h4,s1)
net.addLink(s1,s2)
net.addLink(h5,s2)

# INterface IP address configuration
h3.setIP('10.0.1.2','24')
h4.setIP('10.0.1.4','24')
h5.setIP('10.0.2.5','24')
s1.setIP('10.0.1.1','24')
s2.setIP('10.0.2.1','24')

# Setting default gateways on hosts
h3.cmd('route add default gw 10.0.1.1')
h4.cmd('route add default gw 10.0.1.1')
h5.cmd('route add default gw 10.0.2.1')


# network Launching & control
net.start()
net.pingAll()

# Call ineractive CLI
mininet.cli.CLI(net)
net.stop()
