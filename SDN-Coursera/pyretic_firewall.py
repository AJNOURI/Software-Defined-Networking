'''
    Coursera:
    - Software Defined Networking (SDN) course
    -- Module 6 Programming Assignment

    Professor: Nick Feamster
    Teaching Assistant: Arpit Gupta
'''

################################################################################
# The Pyretic Project                                                          #
# frenetic-lang.org/pyretic                                                    #
# author: Joshua Reich (jreich@cs.princeton.edu)                               #
################################################################################
# Licensed to the Pyretic Project by one or more contributors. See the         #
# NOTICES file distributed with this work for additional information           #
# regarding copyright and ownership. The Pyretic Project licenses this         #
# file to you under the following license.                                     #
#                                                                              #
# Redistribution and use in source and binary forms, with or without           #
# modification, are permitted provided the following conditions are met:       #
# - Redistributions of source code must retain the above copyright             #
#   notice, this list of conditions and the following disclaimer.              #
# - Redistributions in binary form must reproduce the above copyright          #
#   notice, this list of conditions and the following disclaimer in            #
#   the documentation or other materials provided with the distribution.       #
# - The names of the copyright holds and contributors may not be used to       #
#   endorse or promote products derived from this work without specific        #
#   prior written permission.                                                  #
#                                                                              #
# Unless required by applicable law or agreed to in writing, software          #
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT    #
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the     #
# LICENSE file distributed with this work for specific language governing      #
# permissions and limitations under the License.                               #
################################################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.modules.mac_learner import mac_learner
import os
from pox.lib.addresses import EthAddr

# insert the name of the module and policy you want to import
import csv

policy_file = "%s/pyretic/pyretic/examples/firewall-policies.csv" % os.environ[ 'HOME' ]

def main():
    # Copy the code you used to read firewall-policies.csv from the Pox Firewall assignment
    # start with a policy that doesn't match any packets
    not_allowed = none
    allowed = none

    acl = []
    with open(policy_file, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            element = [MAC(row['mac_0']),MAC(row['mac_1'])]
            inv_element = [MAC(row['mac_1']),MAC(row['mac_0'])]
            acl.append(element)
            acl.append(inv_element)

    for [i, j] in acl:
        print [i,j]
        not_allowed = not_allowed | (match(srcmac=i) & match(dstmac=j) | match(srcmac=j) & match(dstmac=i))

# express allowed traffic in terms of not_allowed - hint use '~'
    allowed = ~not_allowed

    # and only send allowed traffic to the mac learning (act_like_switch) logic
    #return mac_learner()
    return allowed >> mac_learner()