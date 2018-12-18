#!/usr/bin/env python
# license removed for brevity
import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)
main_folder = os.path.join(current_folder, "..")
sys.path.append(main_folder)
'''
utils_folder = os.path.join(current_folder, "..", "utils")
sys.path.append(utils_folder)
config_folder = os.path.join(current_folder, "..", "config")
sys.path.append(config_folder)
'''
import time

from bs4 import BeautifulSoup
from config.console_formatter import Console_Formatter


class HTTP_Parser:
    ##PUBLIC
    version = "1.0"
    html_data = None
    
    is_info = True
    
    ##PRIVATE
    program_name_ = __name__
    soup_ = None
    console_formatter_ = Console_Formatter()
    
    def __init__(self, html_data=None, is_info=True):
        self.html_data = html_data
        self.is_info = is_info
        
    def set_html_data(self, html_data):
        self.html_data = html_data
       
    def meta_finder(self, html_data):
        return self.tag_finder('meta')
 
    def image_finder(self):
        return self.tag_finder('img')
        
    def link_finder(self):
        return self.tag_finder('a')
    
    def tag_finder(self, tag, recursive=True):
        if self.html_data == None:
            if self.is_info : 
                msg = "HTML data empty !"
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return None
        self.soup_ = BeautifulSoup(self.html_data, 'lxml')
        tags = self.soup_.find_all(tag, recursive)
        
        if self.is_info : 
            if len(tags) != 0:
                msg = "HTML tags \"{}\" found !".format(tag)
                print(self.console_formatter_.INFO(self.program_name_, msg))
            else:
                msg = "HTML tags \"{}\" empty !".format(tag)
                print(self.console_formatter_.WARN(self.program_name_, msg))
        return tags
