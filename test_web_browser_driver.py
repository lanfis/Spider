#!/usr/bin/env python
# license removed for brevity
import requests
from bs4 import BeautifulSoup

import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)
import time

from modules.Web_Browser_Driver import Web_Browser_Driver

wb = Web_Browser_Driver(is_window=True, is_info=True)

#wb.access_website("https://shopping.pchome.com.tw/")
wb.access_website("file:///home/adel/Dropbox/Github/Spider/test.html")
#wb.search("iPad")
#wb.find_xpath("//input[@type='email']")
wb.find_tag_name("button")
wb.click()
if wb.switch_alert():
    wb.alert_text("FUCK YOU")
    wb.alert_accept()
    wb.alert_accept()
#wb.send_keys([account])
#wb.keyboard_enter()
#wb.click_link("we", is_contact=True)
#print(wb.get_source())

#ws = Web_Browser_Driver(is_window=True, is_info=True)
#ws.access_website("http://www.python.org")
#ws.click_link("About", is_contact=False)

for i in range(3):
    #print(wb.get_url())
    time.sleep(1)

