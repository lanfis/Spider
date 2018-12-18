#!/usr/bin/env python
# license removed for brevity
from scapy.all import *

import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)
main_folder = os.path.join(current_folder, "..")
sys.path.append(main_folder)
'''
utils_folder = os.path.join(current_folder, "..", "utils")
sys.path.append(utils_folder)
'''

from IPParser import IPParser


class Sniffer:
    interface_ = None
    count_ = -1
    filter_ = None
    store_ = 0
    
    use_show = True
    use_logger = True
    folder_logger = os.path.join(current_folder, "sniffer_log")
    logger_filename = "sniffer_record.txt"
    logger_raw_filename = "sniffer_raw.txt"
    
    parser_ = IPParser()

    def __init__(self, interface=None, count=-1, filter=None, store=0, use_show=True, use_logger=True):#filter="tcp and ( port 80 or port 443 )"
        self.interface_ = interface
        self.count_ = count
        self.filter_ = filter
        self.store_ = store
        self.use_show = use_show
        self.use_logger = use_logger
    
    def run(self):
        pkts = sniff(iface=self.interface_, prn=self.callback, count=self.count_, filter=self.filter_, store=self.store_)
        return pkts
    
    def sniff_analyze(self, pkts):
        src_ether = "" if self.parser_.parser_src_ether(pkts) == None else self.parser_.parser_src_ether(pkts)
        src_ip = "" if self.parser_.parser_src_ip(pkts) == None else self.parser_.parser_src_ip(pkts)
        src_port = "" if self.parser_.parser_src_port(pkts) == None else self.parser_.parser_src_port(pkts)
        dst_ether = "" if self.parser_.parser_dst_ether(pkts) == None else self.parser_.parser_dst_ether(pkts)
        dst_ip = "" if self.parser_.parser_dst_ip(pkts) == None else self.parser_.parser_dst_ip(pkts)
        dst_port = "" if self.parser_.parser_dst_port(pkts) == None else self.parser_.parser_dst_port(pkts)
        protocol = "" if self.parser_.parser_proto(pkts) == None else self.parser_.parser_proto(pkts)
        result = "Ether = {} / IP = {:<15s}:{:<7s} >>>> Ether = {} / IP = {:<15s}:{:<5s}  Proto:{:<7s}".format(src_ether, src_ip, src_port, dst_ether, dst_ip, dst_port, protocol)
        
        if protocol == 'tcp':
            flags = self.parser_.parser_flags(pkts)
            result = "{} Flags:{}".format(result, flags)

        tm =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        result = "{} {}".format(tm, result)
        return result
        
    def callback(self, pkts):
        self.show(pkts)
        self.logger(pkts)
        
    def logger(self, pkts):
        if not self.use_logger: return
        if not os.path.exists(self.folder_logger):
            os.makedirs(self.folder_logger)  
        with open(os.path.join(self.folder_logger, self.logger_raw_filename), 'a') as fid:
            fid.write("{}\n".format(pkts))
        with open(os.path.join(self.folder_logger, self.logger_filename), 'a') as fid:
            fid.write("{}\n".format(self.sniff_analyze(pkts)))
        
    def show(self, pkts):
        if not self.use_show: return
        print(self.sniff_analyze(pkts))
        
