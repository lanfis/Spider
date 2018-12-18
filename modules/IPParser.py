#!/usr/bin/env python
# license removed for brevity
from scapy.all import *

import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)
main_folder = os.path.join(current_folder, "..")
sys.path.append(main_folder)
'''
utils_folder = os.path.join(current_folder, "..", "utils")
sys.path.append(utils_folder)
'''
import time

from utils.EtherMaker import EtherMaker
from utils.IPMaker import IPMaker
from utils.TCPMaker import TCPMaker
from utils.UDPMaker import UDPMaker
from utils.ICMPMaker import ICMPMaker

class IPParser:
    ether_maker_ = EtherMaker()
    ip_maker_ = IPMaker()
    tcp_maker_ = TCPMaker()
    udp_maker_ = UDPMaker()
    icmp_maker_ = ICMPMaker()
    
    src_ether = None
    dst_ether = None
    src_ip = None
    dst_ip = None
    ttl = None
    protocol = None
    src_port = None
    dst_port = None
    seq = None
    flags = None
    type = None
    
    def __init__(self):
        pass
    def packet_parser(self, packet):
        self.src_ether = self.parser_src_ether(packet)
        self.dst_ether = self.parser_dst_ether(packet)
        self.src_ip = self.parser_src_ip(packet)
        self.dst_ip = self.parser_dst_ip(packet)
        self.ttl = self.parser_ttl(packet)
        self.protocol = self.parser_proto(packet)
        self.src_port = self.parser_src_port(packet)
        self.dst_port = self.parser_dst_port(packet)
        self.seq = self.parser_seq(packet)
        self.flags = self.parser_flags(packet)
        self.type = self.parser_type(packet)
        
    def parser_src_ether(self, packet):
        return packet.sprintf("%Ether.src%")
        
    def parser_dst_ether(self, packet):
        return packet.sprintf("%Ether.dst%")
        
    def parser_src_ip(self, packet):
        return packet.sprintf("%IP.src%")
    def parser_dst_ip(self, packet):
        return packet.sprintf("%IP.dst%")
    def parser_ttl(self, packet):
        return packet.sprintf("%IP.ttl%")
    def parser_proto(self, packet):
        return packet.sprintf("%IP.proto%")
        
    def parser_src_port(self, packet):
        if self.parser_proto(packet) == 'tcp' or self.parser_proto(packet) == 6:
            return packet.sprintf("%TCP.sport%")
        elif self.parser_proto(packet) == 'udp' or self.parser_proto(packet) == 17:
            return packet.sprintf("%UDP.sport%")
        else:
            return None
    def parser_dst_port(self, packet):
        if self.parser_proto(packet) == 'tcp' or self.parser_proto(packet) == 6:
            return packet.sprintf("%TCP.dport%")
        elif self.parser_proto(packet) == 'udp' or self.parser_proto(packet) == 17:
            return packet.sprintf("%UDP.dport%")
        else:
            return None
            
    def parser_flags(self, packet):
        if self.parser_proto(packet) == 'tcp' or self.parser_proto(packet) == 6:
            return packet.sprintf("%TCP.flags%")
        else:
            return None
            
    def parser_seq(self, packet):
        if self.parser_proto(packet) == 'tcp' or self.parser_proto(packet) == 6:
            return packet.sprintf("%TCP.seq%")
        elif self.parser_proto(packet) == 'icmp' or self.parser_proto(packet) == 1:
            return packet.sprintf("%ICMP.seq%")
        else:
            return None

    def parser_type(self, packet):
        if self.parser_proto(packet) == 'icmp' or self.parser_proto(packet) == 1:
            return packet.sprintf("%ICMP.type%")
        else:
            return None
        
