#!/usr/bin/env python
# license removed for brevity
from scapy.all import *

import sys

class UDPMaker:
    SRC_PORT = 53
    DST_PORT = 53
    LEN = None
    CHKSUM = None
    def __init__(self,                 
                SRC_PORT=53, 
                DST_PORT=53, 
                LEN=None, 
                CHKSUM=None
                ):
        self.SRC_PORT = SRC_PORT
        self.DST_PORT = DST_PORT
        self.LEN = LEN
        self.CHKSUM = CHKSUM
    
    def make_packet(self):
        return UDP(
                sport=self.SRC_PORT,
                dport=self.DST_PORT,
                len=self.LEN,
                chksum=self.CHKSUM,            
                )
    def parse_src_port(self, udp):
        return udp.sport
    def parse_dst_port(self, udp):
        return udp.dport
    def parse_len(self, udp):
        return udp.len
    def parse_chksum(self, udp):
        return udp.chksum
    def show(self, udp):
        return udp.show2()
