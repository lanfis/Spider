#!/usr/bin/env python
# license removed for brevity
import requests
from scapy.all import *

import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)


from modules.IPParser import IPParser
from modules.Sniffer import Sniffer

print("sniffer starting ...")

sniffer = Sniffer(count=-1, filter="arp", use_show=True, use_logger=False)#, filter="arp")#, filter="tcp and ( port 80 or port 443 )")

pkts = sniffer.run()

