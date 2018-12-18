#!/usr/bin/env python
# license removed for brevity
from scapy.all import *

import sys

class TCPMaker:
    SRC_PORT = 20
    DST_PORT = 80
    SEQ = 0
    ACK = 0
    DATAOFS = None
    RESERVED = 0
    FLAGS = 2
    WINDOW = 8192
    CHKSUM = None
    URGPTR = 0
    OPTIONS = []
    def __init__(self, 
                SRC_PORT=20, 
                DST_PORT=80, 
                SEQ=0, 
                ACK=0, 
                DATAOFS=None, 
                RESERVED=0, 
                FLAGS=2, 
                WINDOW=8192, 
                CHKSUM=None, 
                URGPTR=0, 
                OPTIONS=[]
                ):
        self.SRC_PORT = SRC_PORT
        self.DST_PORT = DST_PORT
        self.SEQ = SEQ
        self.ACK = ACK
        self.DATAOFS = DATAOFS
        self.RESERVED = RESERVED
        self.FLAGS = FLAGS#Uergent, Ack, Push function, Reset, Sync, No more
        self.WINDOW = WINDOW
        self.CHKSUM = CHKSUM
        self.URGPTR = URGPTR
        self.OPTIONS = OPTIONS
    
    def make_packet(self):
        return TCP(
                sport=self.SRC_PORT,
                dport=self.DST_PORT,
                seq=self.SEQ,
                ack=self.ACK,
                dataofs=self.DATAOFS,
                reserved=self.RESERVED,
                flags=self.FLAGS,
                window=self.WINDOW,
                chksum=self.CHKSUM,
                urgptr=self.URGPTR,
                options=self.OPTIONS                
                )
    def parse_src_port(self, tcp):
        return tcp.sport
    def parse_dst_port(self, tcp):
        return tcp.dport
    def parse_seq(self, tcp):
        return tcp.seq
    def parse_ack(self, tcp):
        return tcp.ack
    def parse_dataofs(self, tcp):
        return tcp.dataofs
    def parse_reserved(self, tcp):
        return tcp.reserved
    def parse_flags(self, tcp):
        return tcp.flags
    def parse_window(self, tcp):
        return tcp.window
    def parse_chksum(self, tcp):
        return tcp.chksum
    def parse_urgptr(self, tcp):
        return tcp.urgptr
    def parse_options(self, tcp):
        return tcp.options
    def show(self, tcp):
        return tcp.show2()
