#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink

class CustLinear(object):
    "Linear topology of k switches, with one host per switch."
    def __init__(self, net, s=3, h=3, **link ):
        """Init.
        s: number of switches
        h: number of hosts per swcitch
        hconf: host configuration options
        lconf: link configuration options"""
        self.h = h
        self.s = s
        self.net = net
        self.c0 = self.net.addController()
        self.switch = {}
        
        for sn in xrange(1, self.s):
            self.switch[sn] = self.net.addSwitch('s%s' % sn, cpu=.5/sn)
            self.host = {}
            for hn in xrange(1, self.h):
                self.host[hn] = self.net.addHost('h'+str(hn)+str(sn))
                self.net.addLink(self.host[hn], self.switch[sn], **link)
     
    def start(self):
        print 'Starting the network...'
        self.net.start()

    def stop (self):
        print 'Stopping the network'
        self.net.stop()

    def simpletest(self):
        "Create and test a simple network"
        print "Dumping host connections"
        dumpNodeConnections(self.net.hosts)
        print "Testing network connectivity"
        self.net.pingAll()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    linkopts = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    mytop = CustLinear(Mininet(host=CPULimitedHost, link=TCLink), **linkopts)
    mytop.start()
    mytop.simpletest()
    CLI(mytop.net)
    mytop.stop()
