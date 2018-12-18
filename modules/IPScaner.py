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
from utils.ARPMaker import ARPMaker
from utils.TCPMaker import TCPMaker
from utils.UDPMaker import UDPMaker
from utils.ICMPMaker import ICMPMaker
from utils.PacketSR import PacketSR
from IPParser import IPParser

from Timeout_Estimator import Timeout_Estimator

class IPScaner:
    timeout_torlorence_ = 0.2
    ttl_torlorence_ = 2

    ether_maker_ = EtherMaker()
    ip_maker_ = IPMaker()
    arp_maker_ = ARPMaker()
    tcp_maker_ = TCPMaker()
    udp_maker_ = UDPMaker()
    icmp_maker_ = ICMPMaker()
    packet_sr_ = PacketSR()
    parser_ = IPParser()
    timeout_estimator_ = Timeout_Estimator(torlorence=timeout_torlorence_)
    
    
    packet = None
    def __init__(self,
                src_mac=None,
                dst_mac=None, 
                src_ip=None, 
                dst_ip=None, 
                src_port=80, 
                dst_port=80, 
                seq=0, 
                protocol=None, 
                ttl=64, 
                interface=None, 
                timeout=1, 
                retry=0
                ):
        self.ether_maker_.SRC = src_mac
        self.ether_maker_.DST = dst_mac
        self.ip_maker_.SRC = src_ip
        self.ip_maker_.DST = dst_ip
        self.tcp_maker_.SRC_PORT = src_port
        self.tcp_maker_.DST_PORT = dst_port
        self.udp_maker_.SRC_PORT = src_port
        self.udp_maker_.DST_PORT = dst_port
        self.tcp_maker_.SEQ = seq
        self.icmp_maker_.SEQ = seq
        self.ip_maker_.PROTO = protocol
        self.ip_maker_.TTL = ttl
        self.packet_sr_.interface = interface
        self.packet_sr_.timeout = timeout
        self.packet_sr_.retry = retry
    
    
        
    def transmission_path_tracer(self, ip, sequential=False, depth=16, timeout=None):
        if timeout != None:
            self.set_timeout(timeout)
        if sequential:
            t_ans = []
            t_unans = []
            for i in range(depth):
                self.set_ttl(int(i))
                ans, unans = self.ping_scan(ip)
                t_ans += ans
                t_unans += unans
        else:
            self.set_ttl(range(depth))
            t_ans, t_unans = self.ping_scan(ip, use_ack=True)
        return t_ans, t_unans
       
    def port_scan(self, ip=None, port=None, use_tcp=True, use_udp=True, use_ack=None):
        if ip != None:
            self.set_dst_ip(ip)
        port = range(65535) if port == None else port
        use_ack = use_ack if use_ack != None else False if len(port) > 2 else True
        ans, unans = self.ping_scan(ip=ip, port=port, use_ack=use_ack, use_icmp=False, use_tcp=use_tcp, use_udp=use_udp, timeout=None)
        return ans, unans

    def ping_scan(self, ip, port=80, use_icmp=True, use_tcp=True, use_udp=True, use_ack=True, flags='S', timeout=None):
        if timeout != None:
            self.set_timeout(timeout)
        ping_ip = ip
        t_ans = []
        t_unans = []
        
        if use_icmp:
            icmp_ans, icmp_unans = self.icmp_ping(ping_ip)
            t_ans += icmp_ans
            t_unans += icmp_unans
            del ping_ip[:]
            for snd in icmp_unans:
                self.parser_.packet_parser(snd)
                if self.parser_.dst_ip not in ping_ip:
                    ping_ip.append(self.parser_.dst_ip)

        if use_tcp:
            tcp_ans, tcp_unans = self.tcp_ping(ip=ping_ip, port=port, use_ack=use_ack, flags=flags)
            t_ans += tcp_ans
            t_unans += tcp_unans        
            del ping_ip[:]
            for snd in tcp_unans:
                self.parser_.packet_parser(snd)
                if self.parser_.dst_ip not in ping_ip:
                    ping_ip.append(self.parser_.dst_ip)

        if use_udp:
            udp_ans, udp_unans = self.udp_ping(ip=ping_ip, port=port)
            t_ans += udp_ans
            t_unans += udp_unans
        return t_ans, t_unans
        
    def arp_ping(self, ip=None, mac="FF:FF:FF:FF:FF:FF", timeout=None):
        if timeout != None:
            self.set_timeout(timeout)
        if ip != None:
            self.set_arp_dst_ip(ip)
        self.timeout_estimator_.set_timer()
        ans, unans = self.fake_arp_request()
        self.set_timeout(self.timeout_estimator_.get_timer())
        return ans, unans
            
    def tcp_ping(self, ip=None, port=80, use_ack=True, flags=None, timeout=None):
        flags = 'S' if flags == None else flags
        use_ack = use_ack if flags == 'S' else False
        if timeout != None:
            self.set_timeout(timeout)
        if ip != None:
            self.set_dst_ip(ip)
        self.set_dst_port(port)
        self.timeout_estimator_.set_timer()
        ans, unans = self.fake_tcp_request(use_ack=use_ack, flags=flags)
        self.set_timeout(self.timeout_estimator_.get_timer())
        return ans, unans
        
    def udp_ping(self, ip=None, port=80, timeout=None):
        if timeout != None:
            self.set_timeout(timeout)
        if ip != None:
            self.set_dst_ip(ip)
        self.set_dst_port(port)
        self.timeout_estimator_.set_timer()
        ans, unans = self.fake_udp_request()
        self.set_timeout(self.timeout_estimator_.get_timer())
        return ans, unans
        
    def icmp_ping(self, ip=None, timeout=None):
        if timeout != None:
            self.set_timeout(timeout)
        if ip != None:
            self.set_dst_ip(ip)
        self.timeout_estimator_.set_timer()
        ans, unans = self.fake_icmp_request()
        self.set_timeout(self.timeout_estimator_.get_timer())
        return ans, unans

    def fake_arp_request(self):
        ans, unans = self.arp_request()
        return ans, unans
        
    def arp_request(self):
        mac = "FF:FF:FF:FF:FF:FF"
        self.set_dst_mac(mac)
        self.set_arp_dst_mac("00:00:00:00:00:00")
        self.set_arp_op(1)
        #self.packet = self.ether_maker_.make_packet() / self.arp_maker_.make_packet()
        self.packet = Ether(dst=mac) / self.arp_maker_.make_packet()
        ans, unans = self.sr2()
        return ans, unans
    
    def fake_icmp_request(self):
        self.set_protocol('icmp')
        self.packet = self.ip_maker_.make_packet() / self.icmp_maker_.make_packet()
        ans, unans = self.sr()
        return ans, unans
    
    def fake_udp_request(self):
        self.set_protocol('udp')
        self.packet = self.ip_maker_.make_packet() / self.udp_maker_.make_packet()
        ans, unans = self.sr()
        return ans, unans
        
    def fake_tcp_request(self, use_ack=True, flags='S'):
        ans, unans = self.tcp_sync_request(flags)
        if use_ack:
            ack_ip = []
            for snd, rcv in ans:
                self.parser_.packet_parser(rcv)
                if self.parser_.flags == 'SA':
                    ack_ip.append(self.parser_.src_ip)
            self.set_dst_ip(ack_ip)
            self.tcp_sync_request('A')
        return ans, unans
        
    def tcp_sync_request(self, flags='S'):
        self.set_protocol('tcp')
        self.set_flags(flags)
        self.packet = self.ip_maker_.make_packet() / self.tcp_maker_.make_packet()
        ans, unans = self.sr()
        return ans, unans
        
    def tcp_ack_request(self):
        self.set_protocol('tcp')
        self.set_flags('A')
        self.packet = self.ip_maker_.make_packet() / self.tcp_maker_.make_packet()
        ans, unans = self.sr()
        return ans, unans
        
    def sr(self):
        if self.packet == None:
            return None, None
        return self.packet_sr_.sr(self.packet)
        
    def sr2(self):
        if self.packet == None:
            return None, None
        return self.packet_sr_.sr2(self.packet)
        
    def send(self):
        if self.packet == None:
            return None
        return self.packet_sr_.send(self.packet)
        
    def send2(self):
        if self.packet == None:
            return None
        return self.packet_sr_.send2(self.packet)
    
    def set_packet(self, packet):
        self.packet = packet
    def get_packet(self, packet):
        return self.packet


    def set_arp_src_mac(self, mac):
        self.arp_maker_.HWSRC = mac
    def set_arp_src_ip(self, ip):
        self.arp_maker_.PSRC = ip
    def set_arp_dst_mac(self, mac):
        self.arp_maker_.HWDST = mac
    def set_arp_dst_ip(self, ip):
        self.arp_maker_.PDST = ip
    def set_arp_op(self, op):
        self.arp_maker_.OP = op
    def set_src_mac(self, mac):
        self.ether_maker_.SRC = mac
    def set_dst_mac(self, mac):
        self.ether_maker_.DST = mac
    def set_src_ip(self, ip):
        self.ip_maker_.SRC = ip
    def set_dst_ip(self, ip):
        self.ip_maker_.DST = ip
    def set_src_port(self, port):
        self.tcp_maker_.SRC_PORT = port
        self.udp_maker_.SRC_PORT = port
    def set_dst_port(self, port):
        self.tcp_maker_.DST_PORT = port
        self.udp_maker_.DST_PORT = port
    def set_seq(self, seq):
        self.tcp_maker_.SEQ = seq
        self.icmp_maker_.SEQ = seq
    def set_flags(self, flags):
        self.tcp_maker_.FLAGS = flags
    def set_protocol(self, protocol):
        self.ip_maker_.PROTO = protocol
    def set_ttl(self, ttl):
        self.ip_maker_.TTL = ttl
    def get_ttl(self):
        return self.ip_maker_.TTL
    def set_interface(self, interface):
        self.packet_sr_.interface = interface
    def get_interface(self):
        return self.packet_sr_.interface
    def set_timeout(self, timeout):
        self.packet_sr_.timeout = timeout
    def get_timeout(self):
        return self.packet_sr_.timeout
    def set_retry(self, retry):
        self.packet_sr_.retry = retry
    def get_retry(self):
        return self.packet_sr_.retry
    
    def set_timeout_max(self, timeout):
        self.timeout_max_ = timeout
    def set_timeout_min(self, timeout):
        self.timeout_min_ = timeout
    
    
