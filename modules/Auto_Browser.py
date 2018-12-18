#!/usr/bin/env python
# license removed for brevity
import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)
main_folder = os.path.join(current_folder, "..")
sys.path.append(main_folder)

import time
import random
from config.console_formatter import Console_Formatter

from bs4 import BeautifulSoup
from Web_Browser_Driver import Web_Browser_Driver
from Web_Browser_Driver_Keys import Web_Browser_Driver_Keys

class Auto_Browser:
    #PUBLIC
    version = "1.0"
    browser = None
    is_info = True


    #PRIVATE
    program_name_ = __name__
    console_formatter_  = Console_Formatter()

    def auto_page_down(self, browse_counts=4, browse_delay_min=0.5, browse_delay_max=1.5, buffer_count=3):
        if self.is_info :
            msg = "Auto page down ...";
            print(self.console_formatter_.INFO(self.program_name_, msg))
        source_pre = self.browser.get_source()
        self.browser.find_tag_name('body')
        for i in range(browse_counts):
            self.page_down()
            self.browser.wait(random.uniform(browse_delay_min, browse_delay_max))
            if source_pre == self.browser.get_source():
                buffer_count = buffer_count - 1
                if buffer_count == 0:
                    break
            else:
                source_pre = self.browser.get_source()
                buffer_count = buffer_count
        if self.is_info :
            msg = "Auto page down done !";
            print(self.console_formatter_.INFO(self.program_name_, msg))
        return

    def click(self, text, is_contact=True):
        return self.browser.click_link(text, is_contact)

    def page_down(self):
        self.browser.send_keys([Web_Browser_Driver_Keys().PAGE_DOWN])

    def get_browser(self):
        return self.browser

    def set_browser(self, browser):
        self.browser = browser

    def __init__(self, browser=None, is_notifications=False, is_window=True, is_info=True, is_debug=True, **kwargs):
        self.is_info = is_info
        if self.is_info :
            msg = "Initializing ..."
            print(self.console_formatter_.INFO(self.program_name_, msg))
        self.browser = Web_Browser_Driver(is_notifications=is_notifications,
                                          is_window=is_window, is_info=is_debug,
                                          **kwargs) if browser == None else browser

    def __del__(self):
        if self.is_info :
            msg = "Closing ..."
            print(self.console_formatter_.WARN(self.program_name_, msg))
