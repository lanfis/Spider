#!/usr/bin/env python
# license removed for brevity
import sys
import os
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import time
import threading
from multiprocessing import Queue

from config.console_formatter import Console_Formatter
from modules.HTTP_Requestor import HTTP_Requestor
from modules.HTTP_Parser import HTTP_Parser


class Spider:
    url = None
    saving_directory = os.path.join(current_folder, "Spider_Fetch_Data")

    http_requestor_ = HTTP_Requestor(use_info=True)
    http_parser_ = HTTP_Parser(use_info=True)
    console_formatter_ = Console_Formatter()
    program_name_ = __name__
    
    def __init__(self, url=None, use_info=True, encoding='utf-8'):
        #self.set_encoding(encoding) #only for python2.x
        self.url = url
        self.use_info = use_info
        
    def init(self):
        if not os.path.exists(self.saving_directory):
            os.mkdir(self.saving_directory)
    '''
    def test(self, url):
        r = self.url_downloader(url, "temp.html")
        self.http_parser_.set_html_data(r.text)
        links = self.http_parser_.link_finder()
        for link in links:
            print(link.attrs.items()[0][1])
    '''        
    def set_encoding(self, encoding='utf-8'):
        reload(sys)
        sys.setdefaultencoding(encoding)
    
    def image_downloader(self, url, file_name=None):
        r = self.http_requestor_.get(url=url, payload=None, use_parse=False, stream=False)
        self.http_parser_.set_html_data(r.text)
        imgs = self.http_parser_.image_finder()
        if imgs == None:    return False
        
        for img in imgs:
            for key in img.attrs.keys():
                if key.find('src') > 0:
                    img_url = img.get(key)
                    break
            
            self.http_requestor_.use_info = False
            r = self.http_requestor_.get(url=img_url, use_parse=False, stream=False)
            if r == None:
                if self.use_info : 
                    msg = "Downloading image : {} fail !".format(img_url)
                    print(self.console_formatter_.WARN(self.program_name_, msg))
            else:
                image_file = os.path.join(self.saving_directory, img_url.split('/')[-1] if file_name == None else file_name)
                with open(image_file, 'wb') as fid:
                    fid.write(r.content)
                    fid.close()
                if self.use_info : 
                    msg = "Downloading image : {} >> {}".format(img_url, image_file)
                    print(self.console_formatter_.INFO(self.program_name_, msg))
            
    def url_downloader(self, url, file_name=None, stream=True):
        r = self.http_requestor_.get(url=url, payload=None, use_parse=False, stream=stream)
        if r == None:
            if self.use_info : 
                msg = "Downloading url : {} fail !".format(url)
                print(self.console_formatter_.WARN(self.program_name_, msg))
            return None
        else:
            url_file = os.path.join(self.saving_directory, file_name)
            with open(url_file, 'w') as fid:
                fid.write(r.text)
                fid.close()
            if self.use_info : 
                msg = "Downloading url : {} >> {}".format(url, url_file)
                print(self.console_formatter_.INFO(self.program_name_, msg))
            return r
