#!/usr/bin/env python
# license removed for brevity
from scapy.all import *

import sys

class IPMaker:
    VERSION = 4
    IHL = None
    TOS = None
    LEN = None
    ID = 1
    FLAGS = 0
    FRAG = 0
    TTL = 64
    PROTO = 0
    CHKSUM = None
    SRC = None
    DST = None
    OPTIONS = []
    def __init__(self, 
                VERSION=4, 
                IHL=None, 
                TOS=None, 
                LEN=None, 
                ID=None, 
                FLAGS=None,     
                FRAG = 0, 
                TTL = 64, 
                PROTO = 0, 
                CHKSUM = None, 
                SRC = None, 
                DST = None, 
                OPTIONS = []
                ):
        self.VERSION = VERSION
        self.IHL = IHL
        self.TOS = TOS
        self.LEN = LEN
        self.ID = ID
        self.FLAGS = FLAGS
        self.FRAG = FRAG
        self.TTL = TTL
        self.PROTO = PROTO
        self.CHKSUM = CHKSUM
        self.SRC = SRC
        self.DST = DST
        self.OPTIONS = OPTIONS
    
    def make_packet(self):
        return IP(
                version=self.VERSION,
                ihl=self.IHL,
                tos=self.TOS,
                len=self.LEN,
                id=self.ID,
                flags=self.FLAGS,
                frag=self.FRAG,
                ttl=self.TTL,
                proto=self.PROTO,
                chksum=self.CHKSUM,
                src=self.SRC,
                dst=self.DST,
                options=self.OPTIONS
                )
    def parse_version(self, ip):
        return ip.version
    def parse_ihl(self, ip):
        return ip.ihl
    def parse_tos(self, ip):
        return ip.tos
    def parse_len(self, ip):
        return ip.len
    def parse_id(self, ip):
        return ip.id
    def parse_flags(self, ip):
        return ip.flags
    def parse_frag(self, ip):
        return ip.frag
    def parse_ttl(self, ip):
        return ip.ttl
    def parse_proto(self, ip):
        return ip.proto
    def parse_chksum(self, ip):
        return ip.chksum
    def parse_src(self, ip):
        return ip.src
    def parse_dst(self, ip):
        return ip.dst
    def parse_options(self, ip):
        return ip.options
    def show(self, ip):
        return ip.show2()
