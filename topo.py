#!/usr/bin/python
#Topologia QoS SDN

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from mininet.util import dumpNodeConnections
from subprocess import call
import os

def myNetwork():

    info( '*** Stopping Network Manager\n')
    os.system("stop network-manager")

    net = Mininet( topo=None,
                   build=False,
		   autoSetMacs=True,
		   #autoStaticArp=True,
		   host=CPULimitedHost,
		   link=TCLink)

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Adding switches\n')
    r1 = net.addSwitch('r1', cls=OVSKernelSwitch)
    r2 = net.addSwitch('r2', cls=OVSKernelSwitch)
    r3 = net.addSwitch('r3', cls=OVSKernelSwitch)

    info( '*** Adding hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.1/24')
    h2 = net.addHost('h2', cls=Host, ip='10.0.1.2/24')
    srv1 = net.addHost('srv1', cls=Host, ip='10.0.11.1/24')   
    srv2 = net.addHost('srv2', cls=Host, ip='10.0.11.2/24')

    info( '*** Adding links\n')
    net.addLink(h1, r1, 1, 1)
    net.addLink(h2, r1, 1, 2)
    net.addLink(srv1, r2, 1, 1)
    net.addLink(srv2, r2, 1, 2)
    net.addLink(r1, r3, 3, 1)
    net.addLink(r2, r3, 3, 2)

    info( '*** Starting network\n')
    net.build()

    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    for switch in net.switches:
	switch.start([c0])

    info( '*** Setting routes\n')
    h1.cmd('route add default dev h1-eth1')
    h2.cmd('route add default dev h2-eth1')
    srv1.cmd('route add default dev srv1-eth1')
    srv2.cmd('route add default dev srv2-eth1')

    info( '*** Post configure switches and hosts\n')
    dumpNodeConnections(net.hosts)

    CLI(net)
    net.stop()

    info( '*** Starting Network Manager\n')
    os.system("start network-manager")


if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
