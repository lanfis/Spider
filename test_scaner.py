#!/usr/bin/env python
# license removed for brevity
import requests
from scapy.all import *

import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)


from modules.IPScaner import IPScaner
from modules.IPParser import IPParser


print("program starting ...")

parser = IPParser()

ip_scaner = IPScaner()
ip_scaner.set_dst_ip("www.google.com")
ip_scaner.set_protocol('tcp')
ip_scaner.set_src_port(80)

a = range(1, 1024, 1)
ans, unans = ip_scaner.port_scan(ip=['www.drjh.ylc.edu.tw'], port=a)
#ip_scaner.transmission_time_estimator()

#ip_scaner.set_ttl(4)
t1 = time.time()
#ans, unans = ip_scaner.ping_scan(ip=["lanfis.ddns.net", "rosmaster.ddns.net"], port=[22, 80])
#ans, unans = ip_scaner.transmission_path_tracer(ip=["www.google.com"], depth=8, sequential=True)
#ip_scaner.ipscan(ip='rosmaster.ddns.net', port=80, protocol='tcp')
t2 = time.time()
dt = t2 - t1

i = 1
for snd, rcv in ans:
    parser.packet_parser(rcv)
    print("{} : {}  {} {}".format(i, parser.src_ip, parser.src_port, parser.flags))
    i += 1
    #rcv.show2()
print("using %.2f secs" %(dt))


