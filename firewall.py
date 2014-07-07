'''
oursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
import csv

''' Add your imports here ... '''



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''

class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug('Enabling Firewall Module __init__')
        self.mac_pair = []
        file =  open('firewall-policies.csv','rb')
        reader = csv.DictReader(file)
        for row in reader:
            self.mac_pair.append((row['mac_0'], row['mac_1']))
            self.mac_pair.append((row['mac_1'], row['mac_0']))

        log.debug('Firewall policies loaded successfully')

    def _handle_ConnectionUp (self, event):
        log.debug('_handle_ConnectionUp')
        ''' Add your logic here ... '''
        
        #dl_src = '00:00:00:00:00:03'
        #for (mac_src,mac_dst) in self.mac_pair:
        #    if mac_src == dl_src:
        #        print 'mac_src ',mac_src,' : mac_dst ',mac_dst
        #        break

        for (mac_src, mac_dst) in self.mac_pair:
            match = of.ofp_match()  # obj describing packet header fields & input port to match on
            match.dl_src = EthAddr(mac_src)
            match.dl_dst = EthAddr(mac_dst)
            msg = of.ofp_flow_mod()   # create packet out message
            msg.match = match
            msg.actions.append(of.ofp_action_output(port = of.OFPP_NONE))
            event.connection.send(msg) 
    
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall) 