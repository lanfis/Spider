#!/usr/bin/env python
# license removed for brevity
from scapy.all import *

import sys

class ARPMaker:
    HWTYPE = 1#XShortField
    PTYPE = 2048#XShortEnumField
    HWLEN = 6#ByteField
    PLEN = 4#ByteField
    OP = 1#ShortEnumField
    HWSRC = None#ARPSourceMacField
    PSRC = None#SourceIPField
    HWDST = '00:00:00:00:00:00'#MacField
    PDST = '0.0.0.0'#IPField
    def __init__(self, 
                HWTYPE = 1,
                PTYPE = 2048,
                HWLEN = 6,
                PLEN = 4,
                OP = 1,
                HWSRC = None,
                PSRC = None,
                HWDST = '00:00:00:00:00:00',
                PDST = '0.0.0.0'
                ):
        self.HWTYPE = HWTYPE
        self.PTYPE = PTYPE
        self.HWLEN = HWLEN
        self.PLEN = PLEN
        self.OP = OP
        self.HWSRC = HWSRC
        self.PSRC = PSRC
        self.HWDST = HWDST
        self.PDST = PDST
    
    def make_packet(self):
        return ARP(
                hwtype=self.HWTYPE,
                ptype=self.PTYPE,
                hwlen=self.HWLEN,
                plen=self.PLEN,
                op=self.OP,
                hwsrc=self.HWSRC,
                psrc=self.PSRC,
                hwdst=self.HWDST,
                pdst=self.PDST
                )
    def parse_hwtype(self, arp):
        return arp.hwtype
    def parse_ptype(self, arp):
        return arp.ptype
    def parse_hwlen(self, arp):
        return arp.hwlen
    def parse_plen(self, arp):
        return arp.plen
    def parse_op(self, arp):
        return arp.op
    def parse_hwsrc(self, arp):
        return arp.hwsrc
    def parse_psrc(self, arp):
        return arp.psrc
    def parse_hwdst(self, arp):
        return arp.hwdst
    def parse_pdst(self, arp):
        return arp.pdst
    def show(self, arp):
        return arp.show2()
