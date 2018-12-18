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
'''
import time
import json
from config.console_formatter import Console_Formatter

from bs4 import BeautifulSoup
from Web_Browser_Driver import Web_Browser_Driver
import Web_Browser_Driver_Keys as WBD_Keys
#from HTTP_Parser import HTTP_Parser


class Login_Breaker:
    ##PUBLIC
    version = "1.0"
    browser = None
    
    is_info = True
    
    ##PRIVATE
    program_name_ = __name__
    console_formatter_  = Console_Formatter()
    #parser_  = HTTP_Parser(is_info=False)
    parser_ = None
    
    is_info = True
    is_login = False
    
    def login(self, account, passwd, seperate=False, wait_time=5):
        if self.is_info : 
            msg = "Starting login ..."
            print(self.console_formatter_.NOTIFY(self.program_name_, msg))
        if not self.login_(account, passwd, seperate, wait_time=wait_time):
            return False
        
        if self.is_info : 
            msg = "Checking login ..."
            print(self.console_formatter_.NOTIFY(self.program_name_, msg))
        if self.check_login() : 
            if self.is_info : 
                msg = "Login successfully !"
                print(self.console_formatter_.NOTIFY(self.program_name_, msg))
            return True
        else:
            if self.is_info : 
                msg = "Login fail !"
                print(self.console_formatter_.FATAL(self.program_name_, msg))
                #msg = "Returning back ..."
                #print(self.console_formatter_.FATAL(self.program_name_, msg))
                #self.browser.backward()    
            return False        
        
    def login_(self, username, passwd, seperate, wait_time=5):
        if self.is_info : 
            msg = "--Searching & typing username : {} ...".format(username)
            print(self.console_formatter_.NOTIFY(self.program_name_, msg))
        if not self.login_username(username, input_method=None):
            if self.is_info : 
                msg = "--Searching & typing username fail !".format(username)
                print(self.console_formatter_.FATAL(self.program_name_, msg))
            return False
        
        if seperate:
            element = self.browser.get_element()
            self.browser.keyboard_enter()
            if not self.browser.explicitly_wait(wait_time, self.browser.ec_element_stalness_callback(element)):
                return False
        
        if self.is_info : 
            msg = "--Searching & typing passwd : {} ...".format(passwd)
            print(self.console_formatter_.NOTIFY(self.program_name_, msg))
        if not self.login_passwd(passwd, input_method=None):
            if self.is_info : 
                msg = "--Searching & typing passwd passwd fail !".format(username)
                print(self.console_formatter_.FATAL(self.program_name_, msg))
            return False
        element = self.browser.get_element()
        self.browser.explicitly_wait(wait_time, self.browser.ec_element_stalness_callback(element))
        return True
        
    def check_login(self):
        self.parser_ = BeautifulSoup(self.browser.get_source(), "lxml")
        input_methods = self.parser_.find_all('input')
        for method in input_methods:
            if method.get('type') == 'password':
                self.is_login = False
                return self.is_login
        self.is_login = True
        return self.is_login
        
    def login_username(self, username, input_method=None):
        #is_enter_to_next_passwd_page = True
        input_method_found = False
        if input_method == None:
            self.parser_ = BeautifulSoup(self.browser.get_source(), "lxml")
            input_methods = self.parser_.find_all('input')
            for method in input_methods:
                if method.get('type') == 'email':
                    input_method = "//input[@type='email']"
                    input_method_found = True
                #if method.get('type') == 'password':
                    #is_enter_to_next_passwd_page = False
        if not input_method_found:
            return False
        if not self.browser.find_xpath(input_method):
            return False
        self.browser.element_clear()
        self.browser.send_keys([username])
        #if is_enter_to_next_passwd_page:
            #self.browser.keyboard_enter()     
        return True
        
    def login_passwd(self, passwd, input_method=None):
        input_method_found = False
        if input_method == None:
            self.parser_ = BeautifulSoup(self.browser.get_source(), "lxml")
            input_methods = self.parser_.find_all('input')
            for method in input_methods:
                if method.get('type') == 'password':
                    input_method = "//input[@type='password']"
                    input_method_found = True
        if not input_method_found:
            return False
        if not self.browser.find_xpath(input_method):
            return False
        self.browser.element_clear()
        self.browser.send_keys([passwd])
        self.browser.keyboard_enter()   
        return True
        
    def keyboard_enter(self):
        self.browser.keyboard_enter()
    
    def set_browser(self, browser):
        self.browser = browser
    
    def get_browser(self):
        return self.browser
    
    def check_path(self, path):
        return os.path.exists(path)
    
    def __call__(self, account, passwd, seperate=False, wait_time=5):
        return self.login(account, passwd, seperate, wait_time)
    
    def __init__(self, browser, is_info=True, **kwargs):
        self.is_info = is_info
        if self.is_info : 
            msg = "Initializing ..."
            print(self.console_formatter_.INFO(self.program_name_, msg))
        self.browser = browser
    
    def __del__(self):
        if self.is_info : 
            msg = "Closing ..."
            print(self.console_formatter_.WARN(self.program_name_, msg))
    
        
def main(**kwargs):
    wb  = Web_Browser_Driver(is_cookies_clear=False, is_info=True, **kwargs)
    wb.access_website("http://www.facebook.com")
    #wb.access_website("https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1543668443&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26RpsCsrfState%3d62dc5a5a-be73-4466-d5ac-d96fab54cc67&id=292841&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=90015")
    lb = Login_Breaker(wb)
    lb.login("wer", "sadf", seperate=False)
    lb.login("navida2341@gmail.com", "f2mPqDDG")

if __name__ == "__main__":
    args =  sys.argv[1:]
    kwargs  = {}
    for i in range(0, len(args),2):
        kwargs[args[i]] =   args[i+1]
    main(**kwargs)
