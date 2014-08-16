__author__ = 'ajn'

from netaddr import *

import pprint
'''
ip = IPAddress('192.0.2.1')

ip.str(ip)
print '%s' % ip
ip.int(ip)
ip.hex(ip)
ip.ip.bin
ip.ip.bits()
ip.ip.version

net = IPNetwork('192.168.4.1/22')

net.ip
net.network
ip.broadcast
net.netmask
net.hostmask
net.size
net.prefixlen = 24
net.netmask
net.cidr
net.ip.bits()
net.network.bits()
net.netmask.bits()
net.broadcast.bits()
net.version

'''

net = '192.168.8.0/22'
sublen = 24

def subnetting(netstr, subnetlen):
    ip = IPNetwork(netstr)
    seq = ip.subnet(subnetlen)

    subnetslist = []

    try:
        while True:
            subnetslist.append(seq.next())
        return subnetslist
    except StopIteration:
        pass
        return subnetslist

mylist = subnetting(net, sublen)
print mylist

#======================
'''
#http://anandology.com/python-practice-book/iterators.html

def take(n, seq):
    """Returns first n values from the given sequence."""
    seq = iter(seq)
    result = []
    try:
        for i in range(n):
            result.append(seq.next())
    except StopIteration:
        pass
    return result

print take(5, squares()) # prints [1, 4, 9, 16, 25]

'''
