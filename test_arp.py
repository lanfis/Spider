#!/usr/bin/env python
# license removed for brevity
import requests
from scapy.all import *

import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)


from modules.IPParser import IPParser
from modules.IPScaner import IPScaner

print("arp starting ...")

ipscaner = IPScaner()
parser = IPParser()
ipscaner.set_dst_ip("192.168.0.106/24")
ans, unans = ipscaner.arp_ping("192.168.0.100")

print(ans)

for snd, rcv in ans:
    parser.packet_parser(snd)
    snd.show2()
