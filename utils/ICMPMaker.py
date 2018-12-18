#!/usr/bin/env python
# license removed for brevity
from scapy.all import *

import sys

class ICMPMaker:
    TYPE = 8
    CODE = 0
    CHKSUM = None
    ID = 0
    SEQ = 0
    TIMESTAMP_ORI = 60025165
    TIMESTAMP_RX = 60025165
    TIMESTAMP_TX = 60025165
    GATEWAY = '0.0.0.0'
    PTR = 0
    RESERVED = 0
    LEN = 0
    MASK = '0.0.0.0'
    NEXTHOPMTU = 0
    def __init__(self,
                TYPE=8, 
                CODE=0, 
                CHKSUM=None, 
                ID=0, 
                SEQ=0, 
                TIMESTAMP_ORI=60025165, 
                TIMESTAMP_RX=60025165, 
                TIMESTAMP_TX=60025165, 
                GATEWAY='0.0.0.0', 
                PTR=0, 
                RESERVED=0, 
                LEN=0, 
                MASK='0.0.0.0', 
                NEXTHOPMTU=0
                ):
        self.TYPE = TYPE
        self.CODE = CODE
        self.CHKSUM = CHKSUM
        self.ID = ID
        self.SEQ = SEQ
        self.TIMESTAMP_ORI = TIMESTAMP_ORI
        self.TIMESTAMP_RX = TIMESTAMP_RX
        self.TIMESTAMP_TX = TIMESTAMP_TX
        self.GATEWAY = GATEWAY
        self.PTR = PTR
        self.RESERVED = RESERVED
        self.LEN = LEN
        self.MASK = MASK
        self.NEXTHOPMTU = NEXTHOPMTU
    
    def make_packet(self):
        return ICMP(
                type=self.TYPE,
                code=self.CODE,
                chksum=self.CHKSUM,
                id=self.ID,
                seq=self.SEQ,
                ts_ori=self.TIMESTAMP_ORI,
                ts_rx=self.TIMESTAMP_RX,
                ts_tx=self.TIMESTAMP_TX,
                gw=self.GATEWAY,
                ptr=self.PTR,
                reserved=self.RESERVED,
                length=self.LEN,
                addr_mask=self.MASK,
                nexthopmtu=self.NEXTHOPMTU
                )
    def parse_type(self, icmp):
        return icmp.type
    def parse_code(self, icmp):
        return icmp.code
    def parse_chksum(self, icmp):
        return icmp.chksum
    def parse_id(self, icmp):
        return icmp.id
    def parse_seq(self, icmp):
        return icmp.seq
    def parse_ts_ori(self, icmp):
        return icmp.ts_ori
    def parse_ts_rx(self, icmp):
        return icmp.ts_rx
    def parse_ts_tx(self, icmp):
        return icmp.ts_tx
    def parse_gw(self, icmp):
        return icmp.gw
    def parse_ptr(self, icmp):
        return icmp.ptr
    def parse_reserved(self, icmp):
        return icmp.reserved
    def parse_len(self, icmp):
        return icmp.length
    def parse_mask(self, icmp):
        return icmp.addr_mask
    def parse_nexthopmtu(self, icmp):
        return icmp.nexthopmtu
    
    def show(self, icmp):
        return icmp.show2()
