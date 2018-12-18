#!/usr/bin/env python
# license removed for brevity
import requests
from scapy.all import *

import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)
import numpy as np

from modules.IPScaner import IPScaner
from modules.IPParser import IPParser


print("program starting ...")

parser = IPParser()

ip_scaner = IPScaner()
ip_scaner.set_protocol('tcp')
ip_scaner.set_src_port(80)
use_icmp = False
use_tcp = True
use_udp = False

ip1_start = 10
ip1_end = 11
ip2_start = 12
ip2_end = 13
ip3_start = 0
ip3_end = 1
ip4_start = 0
ip4_end = 20
scan_ports = range(20, 24, 1)
#ip_scaner.set_dst_ip("www.google.com")
'''
a = range(1, 1024, 1)
ans, unans = ip_scaner.port_scan(ip=['www.drjh.ylc.edu.tw'], port=a)
'''
i = 0
scan_ips = []
for ip1 in range(ip1_start, ip1_end, 1):
    for ip2 in range(ip2_start, ip2_end, 1):
        for ip3 in range(ip3_start, ip3_end, 1):
            for ip4 in range(ip4_start, ip4_end, 1):
                scan_ips = np.append(scan_ips, ["{}.{}.{}.{}".format(ip1, ip2, ip3, ip4)])
                
ans, unans = ip_scaner.ping_scan(ip=scan_ips, port=scan_ports, use_icmp=use_icmp, use_tcp=use_tcp, use_udp=use_udp)
for snd, rcv in ans:
    parser.packet_parser(rcv)
    print("{} : {}  {} {}".format(i, parser.src_ip, parser.src_port, parser.flags))
    i += 1


