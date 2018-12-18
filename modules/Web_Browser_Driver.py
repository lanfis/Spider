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
from config.console_formatter import Console_Formatter

#from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support.ui import Select
#import Web_Browser_Driver_Keys as WBD_Keys


class Web_Browser_Driver:
    ##PUBLIC
    version = "1.0"
    agent_header = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    
    im_timeout = 3
    ex_timeout = 3
    is_info = True
    ##PRIVATE
    console_formatter_  = Console_Formatter()
    program_name_ = __name__
    
    web_browser = None
    element = None
    select = None
    waiter  = None
    alert = None
    
    def access_website(self, url, timeout=10):
        if self.web_browser == None:
            return
        
        if self.is_info : 
            msg = "Accessing website : {} ...".format(url)
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.web_browser.get(url)
        if self.is_info : 
            msg = "--Current website : {}".format(self.get_url())
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        
    def search(self, keyword):
        if self.find_name('q'):
            if self.is_info : 
                msg = "Searching keywords : {} ...".format(keyword)
                print(self.console_formatter_.DEBUG(self.program_name_, msg))
            self.send_keys([keyword, Keys.RETURN])
            return True
        else:
            if self.is_info : 
                msg = "Cannot find search bar !"
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return False
        
    def click_link(self, text,  is_contact=True):
        if self.find_link_text(text, is_contact):
            self.click()
            return True
        else:
            return False
        
    def submit(self):
        if self.find_id("submit"):
            self.click()
            return True
        else:
            return False
        
    def keyboard_enter(self):
        self.send_keys([Keys.RETURN])
        
    def execute_js(self, js):
        self.web_browser.execute_script(js)
        
    def get_select_option(self):
        self.select = Select(self.element)
        return self.select.options
        
    def select_by_index(self, select_content):
        for s in select_content:
            self.select.select_by_index(s)
        all_selected_options = self.select.all_selected_options
        if self.is_info : 
            msg = "Selecting : {} ...".format(all_selected_options)
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        
    def select_by_visible_text(self, select_content):
        for s in select_content:
            self.select.select_by_visible_text(s)
        all_selected_options = self.select.all_selected_options
        if self.is_info : 
            msg = "Selecting : {} ...".format(all_selected_options)
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        
    def select_by_value(self, select_content):
        for s in select_content:
            self.select.select_by_value(s)    
        all_selected_options = self.select.all_selected_options  
        if self.is_info : 
            msg = "Selecting : {} ...".format(all_selected_options)
            print(self.console_formatter_.DEBUG(self.program_name_, msg))  
        
    def find_element(self, element_type, element_content, multi=False):
        try:
            if self.is_info : 
                msg = "Finding element : {} ...".format(element_content)
                print(self.console_formatter_.DEBUG(self.program_name_, msg)) 
            self.explicitly_wait(self.ex_timeout, self.ec_element_locate_callback(element_type, element_content))
        except TimeoutException:
            if self.is_info : 
                msg = "Element : {} not found !".format(element_content)
                print(self.console_formatter_.WARN(self.program_name_, msg)) 
            return False
        try:
            self.element = self.web_browser.find_element(element_type, element_content) if not multi else self.web_browser.find_elements(element_type, element_content)
            return True
        except NoSuchElementException:
            return False
        
    def find_id(self, id, multi=False):
        return self.find_element(By.ID, id)
        
    def find_name(self, name, multi=False):
        return self.find_element(By.NAME, name)
    
    def find_xpath(self, xpath, multi=False):
        return self.find_element(By.XPATH, xpath)
    
    def find_link_text(self, text,  is_contact=True, multi=False):
        if is_contact:
            return self.find_element(By.LINK_TEXT, text)
        else:
            return self.find_element(By.PARTIAL_LINK_TEXT, text)
        
    def find_tag_name(self, tag, multi=False):
        return self.find_element(By.TAG_NAME, tag)
        
    def find_class_name(self, class_name, multi=False):
        return self.find_element(By.CLASS_NAME, class_name)
        
    def find_css_selector(self, css_selector, multi=False):
        return self.find_element(By.CSS_SELECTOR, css_selector)
    
    def element_clear(self):
        self.element.clear()
        
    def get_element(self):
        return self.element
    
    def click(self):
        if self.element == None:
            return False
        if self.is_info : 
            msg = "Clicking link : {} ...".format(self.element.text)
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.element.click()
        return True
    
    def get_attribute(self, attribute_name):
        if self.element == None:
            return None
        return self.element.get_attribute(attribute_name)
        
    def switch_alert(self):
        try:
            self.alert = self.web_browser.switch_to.alert
            return True
        except NoAlertPresentException:
            return False
        
    def alert_accept(self):
        if self.is_info : 
            msg = "Alert accept !"
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.alert.accept()
        
    def alert_dismiss(self):
        if self.is_info : 
            msg = "Alert dismiss !"
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.alert.dismiss()
        
    def alert_text(self, text):
        self.alert.send_keys(text)
        
    def get_alert_text(self):
        return self.alert.text
        
    def forward(self):
        if self.is_info : 
            msg = "Website forwading ..."
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.web_browser.forward()
        
    def backward(self):
        if self.is_info : 
            msg = "Website backwarding ..."
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.web_browser.back()
        
    def refresh(self):
        if self.is_info : 
            msg = "Website refreshing ..."
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.web_browser.refresh()
        
    def send_keys(self, keys):
        if self.is_info : 
            msg = "Sending keys : {} ...".format(keys)
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        for k in keys:
            self.element.send_keys(k)
        
    def screenshot(self, file_name):
        if self.is_info : 
            msg = "Screenshot processing ..."
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.web_browser.get_screenshot_as_file(file_name)
        
    def wait(self,  tm):
        time.sleep(tm)
        
    def implicitly_wait(self, tm):
        if self.is_info : 
            msg = "--Setting implicitly timeout : {} secs".format(tm)
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.web_browser.implicitly_wait(tm)
        
    def explicitly_wait(self, tm, ec_callback=None):
        if self.is_info : 
            msg = "--Setting explicitly timeout : {} secs".format(tm)
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.waiter = WebDriverWait(self.web_browser, tm) if ec_callback == None else WebDriverWait(self.web_browser, tm).until(ec_callback)
        return self.waiter
        
    def ec_element_locate_callback(self, element_type, element_content):
        return EC.presence_of_element_located((element_type, element_content))
        
    def ec_element_stalness_callback(self, element=None):
        element = self.element if element == None else element
        return EC.staleness_of(element)
        
    def ec_alert_callback(self):
        return EC.alert_is_present()
        
    def add_cookie(self, cookie):
        self.web_browser.add_cookie(cookie)
        
    def get_cookies(self):
        return self.web_browser.get_cookies()
    
    def delete_cookie(self, name):
        self.web_browser.delete_cookie(name)
        
    def delete_all_cookies(self):
        self.web_browser.delete_all_cookies()
        
    def switch_to_frame(self, id_or_name):
        self.web_browser.switch_to_frame(id_or_name)
        
    def switch_to_parent_content(self):
        self.web_browser.switch_to.parent_content()
        
    def switch_to_default_content(self):
        self.web_browser.switch_to.default_content()
        
    def get_source(self):
        return self.web_browser.page_source
        
    def get_title(self):
        return self.web_browser.title
        
    def get_url(self):
        return self.web_browser.current_url
    
    def get_agent_header(self):
        return self.agent_header
    
    def set_window_position(self, x, y):
        if self.is_info : 
            msg = "--Setting window position : ({}, {}) ...".format(x, y)
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.web_browser.set_window_position(x, y) 
        
    def get_window_position(self):
        return self.web_browser.get_window_position()
        
    def set_window_size(self, width, height):
        if self.is_info : 
            msg = "--Setting window size : {} x {} ...".format(width, height)
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.web_browser.set_window_size(width, height)  
        
    def get_window_size(self):
        return self.web_browser.get_window_size()
        
    def set_window_maximum(self):
        if self.is_info : 
            msg = "--Setting window fullscreen ..."
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.web_browser.maximize_window()
        
    def close(self):
        if self.web_browser != None:
            if self.is_info : 
                msg = "Closing ..."
                print(self.console_formatter_.WARN(self.program_name_, msg))
            self.web_browser.close()
            self.web_browser    = None
        
    def quit(self):
        if self.web_browser != None:
            if self.is_info : 
                msg = "Quitting ..."
                print(self.console_formatter_.WARN(self.program_name_, msg))
            self.web_browser.quit()
            self.web_browser    = None
    
    def __init__(self,  use_browser="Chrome", 
                        agent_header=None,
                        position_x=0, position_y=0, 
                        width=960, height=540, 
                        set_fullscreen=False, 
                        is_cookies_clear=True, 
                        is_notifications=False,
                        im_timeout=3, ex_timeout=3, 
                        is_window=True, is_gpu=True, is_info=True, 
                        **kwargs):
        self.is_info = is_info
        self.im_timeout = im_timeout
        self.ex_timeout = ex_timeout
        if self.is_info : 
            msg = "Initializing ..."
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
            msg = "--Using browser : {}".format(use_browser)
            print(self.console_formatter_.DEBUG(self.program_name_, msg))
        self.agent_header = agent_header if agent_header != None else self.agent_header
        
        if use_browser ==   "Firefox":
            self.web_browser    = webdriver.Firefox()
        else:
            options = webdriver.ChromeOptions()               
            options.add_argument('user-agent={}'.format(self.agent_header))
            if not is_window:
                options.add_argument('--headless')
            if not is_gpu:
                options.add_argument('--disable-gpu')
            if not is_notifications:
                options.add_argument("--disable-notifications")
            self.web_browser    = webdriver.Chrome(chrome_options=options)
            
        self.implicitly_wait(im_timeout)
        #self.explicitly_wait(ex_timeout)
        self.set_window_position(position_x, position_y)
        self.set_window_size(width, height)
        if set_fullscreen:
            self.set_window_maximum()
        if is_cookies_clear:
            self.delete_all_cookies()
    
    def __del__(self):
        self.quit()
        
def main(**kwargs):
    wb  = Web_Browser_Driver(**kwargs)

    wb.access_website("http://www.cwb.gov.tw")
    wb.find_link_text("天氣預報", is_contact=False)
    #wb.access_website("https://world.taobao.com/product/%E6%B7%98%E5%AF%B6%E5%A4%A7%E9%99%B8.htm")
    #wb.find_link_text("淘寶網首頁", is_contact=False)
    wb.click()
    
    #print(wb.get_source())
    time.sleep(3)

if __name__ == "__main__":
    args =  sys.argv[1:]
    kwargs  = {}
    for i in range(0, len(args),2):
        kwargs[args[i]] = args[i+1]
    main(**kwargs)
