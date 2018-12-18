#!/usr/bin/env python
# license removed for brevity
from scapy.all import *

import sys

class PacketSR:
    interface = None
    timeout = 2
    retry = 0
    def __init__(self, iface=None):
        self.interface = iface
    
    def sr(self, packet):#Layer 3
        ans, unans = sr(packet, timeout=self.timeout, retry=self.retry)
        return ans, unans
        
    def sr2(self, packet):#Layer 2
        ans, unans = srp(packet, timeout=self.timeout, retry=self.retry)
        return ans, unans
        
    def send(self, packet, return_packets=True):#Layer 3
        return send(packet, return_packets, iface=self.interface)
    
    def send2(self, packet, return_packets=True):#Layer 2
        return sendp(packet, return_packets, iface=self.interface)
    
