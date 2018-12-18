#!/usr/bin/env python
# license removed for brevity
from scapy.all import *

import sys

class EtherMaker:
    SRC = None
    DST = None
    TYPE = 36864
    def __init__(self, 
                SRC=None, 
                DST=None, 
                TYPE=36864, 
                ):
        self.SRC = SRC
        self.DST = DST
        self.TYPE = TYPE
    
    def make_packet(self):
        return Ether(
                src=self.SRC,
                dst=self.DST,
                type=self.TYPE
                )
    def parse_src(self, ether):
        return ether.src
    def parse_dst(self, ether):
        return ether.dst
    def parse_options(self, ether):
        return ether.type
    def show(self, ether):
        return ether.show2()
