#!/bin/bash

istap0 = `ip a | grep tap0`
istap1 = `ip a | grep tap1`

if [ -n istap0 ]; then
  echo "Configuring tap interfaces"
  ip tuntap add dev tap0 mode tap #user $(whoami)
  ifconfig tap0 up
fi
if [ -n istap1 ]; then
  echo "Configuring tap interfaces"
  ip tuntap add dev tap1 mode tap #user $(whoami)
  ifconfig tap1 up
fi

isbr0 = `ip a | grep br0`

if [ -n isbr0 ]; then
  echo "Configuring bridge interface and assign interfaces to VLANs"
  ovs-vsctl add-br br0
fi

ovs-vsctl add-port br0 eth1 trunks=10,20
ovs-vsctl add-port br0 tap0 tag=10
ovs-vsctl add-port br0 tap1 tag=20

echo 'Bring interfaces up'
ip link set eth1 up
ip link set br0 up
ip link set tap0 up
ip link set tap1 up
