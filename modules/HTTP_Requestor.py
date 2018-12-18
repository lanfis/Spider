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

import requests
from config.console_formatter import Console_Formatter


class HTTP_Requestor:
    ##PUBLIC
    version = "1.0"
    url = None
    agent_header = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    request_url = None
    request_text = None
    request_encoding = None
    
    use_info = True
    timeout = 2
    max_retries = 4
    
    ##PRIVATE
    console_formatter_ = Console_Formatter()
    program_name_ = __name__
    def __init__(self, url=None, use_info=True, agent_header=None):
        self.url = url
        self.use_info = use_info
        self.agent_header = agent_header if agent_header != None else self.agent_header
    
    def get(self, url=None, payload=None, use_parse=True, stream=False):
        if url != None:    self.url = url
        if self.use_info : 
            msg = "GET URL : {}".format(self.url)
            print(self.console_formatter_.INFO(self.program_name_, msg))
        sess = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
        sess.mount('http://', adapter)
        r = sess.get(self.url, data=payload, headers=self.agent_header, timeout=self.timeout, stream=stream)
        #r = requests.get(self.url, data=payload, headers=self.agent_header, timeout=self.timeout, stream=stream)
        if r.status_code == requests.codes.ok:   
            self.request_content_parse(r)
            return r
        else :
            if self.use_info : 
                msg = "GET URL : {} FAIL ! CODE : {}".format(self.url, r.status_code)
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return None
        return r
    '''Below Undone !'''
    def post(self, url=None, payload=None, use_parse=True):
        if url != None:    self.url = url
        if self.use_info : 
            msg = "POST URL : {}".format(self.url)
            print(self.console_formatter_.INFO(self.program_name_, msg))
        r = requests.post(self.url, data=payload, headers=self.agent_header, timeout=self.timeout)
        if r.status_code == requests.codes.ok:  
            self.request_content_parse(r)
            return r
        else :
            if self.use_info : 
                msg = "POST URL : {} FAIL ! CODE : {}".format(self.url, r.status_code)
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return None
        return r
        
    def put(self, url=None, payload=None, use_parse=True):
        if url != None:    self.url = url
        if self.use_info : 
            msg = "PUT URL : {}".format(self.url)
            print(self.console_formatter_.INFO(self.program_name_, msg))
        r = requests.put(self.url, data=payload, headers=self.agent_header, timeout=self.timeout)
        if r.status_code == requests.codes.ok:  
            self.request_content_parse(r)
            return r
        else :
            if self.use_info : 
                msg = "PUT URL : {} FAIL ! CODE : {}".format(self.url, r.status_code)
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return None
        return r
        
    def delete(self, url=None, payload=None, use_parse=True):
        if url != None:    self.url = url
        if self.use_info : 
            msg = "DELETE URL : {}".format(self.url)
            print(self.console_formatter_.INFO(self.program_name_, msg))
        r = requests.delete(self.url, data=payload, headers=self.agent_header, timeout=self.timeout)
        if r.status_code == requests.codes.ok:  
            self.request_content_parse(r)
            return r
        else :
            if self.use_info : 
                msg = "DELETE URL : {} FAIL ! CODE : {}".format(self.url, r.status_code)
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return None
        return r
        
    def head(self, url=None, payload=None, use_parse=True):
        if url != None:    self.url = url
        if self.use_info : 
            msg = "HEAD URL : {}".format(self.url)
            print(self.console_formatter_.INFO(self.program_name_, msg))
        r = requests.head(self.url, data=payload, headers=self.agent_header, timeout=self.timeout)
        if r.status_code == requests.codes.ok:  
            self.request_content_parse(r)
            return r
        else :
            if self.use_info : 
                msg = "HEAD URL : {} FAIL ! CODE : {}".format(self.url, r.status_code)
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return None
        return r
        
    def options(self, url=None, payload=None, use_parse=True):
        if url != None:    self.url = url
        if self.use_info : 
            msg = "OPTIONS URL : {}".format(self.url)
            print(self.console_formatter_.INFO(self.program_name_, msg))
        r = requests.options(self.url, data=payload, headers=self.agent_header, timeout=self.timeout)
        if r.status_code == requests.codes.ok:  
            self.request_content_parse(r)
            return r
        else :
            if self.use_info : 
                msg = "OPTIONS URL : {} FAIL ! CODE : {}".format(self.url, r.status_code)
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return None
        return r
        
    def request_content_parse(self, request_data):
        self.request_url = request_data.url
        self.request_text = request_data.text
        self.request_encoding = request_data.encoding
